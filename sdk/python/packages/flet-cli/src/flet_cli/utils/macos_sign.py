"""macOS code signing and notarization for built .app bundles.

Signs every Mach-O binary in a bundle "inside out" (nested code first, the
bundle itself last) as required by Apple for distribution-signed code, then
optionally submits the result to the Apple notary service and staples the
ticket. `codesign --deep` is deprecated for signing and misses Mach-O files
in resource bundles (where the embedded Python stdlib and site-packages
live), which is why binaries are discovered and signed individually.
"""

import contextlib
import json
import os
import plistlib
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Union

# Ad-hoc signing pseudo-identity understood by codesign.
ADHOC_IDENTITY = "-"

# Mach-O magic numbers: thin (32/64-bit) big-endian and byte-swapped
# (little-endian file) forms, and fat headers.
MACH_O_MAGICS_BE = {b"\xfe\xed\xfa\xce", b"\xfe\xed\xfa\xcf"}  # MH_MAGIC(_64)
MACH_O_MAGICS_LE = {b"\xce\xfa\xed\xfe", b"\xcf\xfa\xed\xfe"}  # MH_CIGAM(_64)
MACH_O_MAGICS = MACH_O_MAGICS_BE | MACH_O_MAGICS_LE
FAT_MAGIC = b"\xca\xfe\xba\xbe"  # FAT_MAGIC (also the Java class file magic)
FAT_CIGAM = b"\xbe\xba\xfe\xca"

# Mach-O header filetype value for standalone executables.
MH_EXECUTE = 0x2

# Directories treated as nested code bundles that receive their own
# signature (sealing their resources) after their inner binaries are signed.
NESTED_BUNDLE_SUFFIXES = {".framework", ".app", ".appex", ".xpc"}


class MacOSSigningError(Exception):
    """Raised when signing, verification, or notarization fails."""


@dataclass
class SigningIdentity:
    """A codesigning identity resolved from the keychain."""

    sha1: str
    name: str

    @property
    def is_adhoc(self) -> bool:
        return self.sha1 == ADHOC_IDENTITY

    @property
    def description(self) -> str:
        return self.name if not self.is_adhoc else "ad-hoc"


ADHOC = SigningIdentity(sha1=ADHOC_IDENTITY, name=ADHOC_IDENTITY)


@dataclass
class NotaryCredentials:
    """Credentials for the Apple notary service.

    Either a notarytool keychain profile name (created with
    `xcrun notarytool store-credentials`) or an App Store Connect API key
    triple (key file path, key ID, issuer ID).
    """

    keychain_profile: Optional[str] = None
    api_key: Optional[str] = None
    api_key_id: Optional[str] = None
    api_issuer: Optional[str] = None

    def as_args(self) -> list[str]:
        if self.keychain_profile:
            return ["--keychain-profile", self.keychain_profile]
        assert self.api_key and self.api_key_id and self.api_issuer
        return [
            "--key",
            self.api_key,
            "--key-id",
            self.api_key_id,
            "--issuer",
            self.api_issuer,
        ]


def _run(args: list[str], timeout: Optional[int] = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def resolve_identity(identity: str) -> SigningIdentity:
    """Resolve a user-provided identity against the keychain.

    Accepts `-` (ad-hoc), a 40-hex SHA-1 fingerprint, the full certificate
    name, or a unique substring of it. Fails fast — with the list of
    available identities — instead of letting codesign silently no-op later.
    """

    identity = identity.strip()
    if identity == ADHOC_IDENTITY:
        return ADHOC

    result = _run(["security", "find-identity", "-v", "-p", "codesigning"])
    if result.returncode != 0:
        raise MacOSSigningError(
            f"Unable to list codesigning identities in the keychain:\n{result.stderr}"
        )

    # Lines look like: `  1) <40-hex SHA-1> "Developer ID Application: ... (TEAMID)"`
    # A certificate present in several keychains (e.g. login and System) is
    # listed once per keychain — deduplicate by fingerprint so the same
    # certificate is never treated as an ambiguous match.
    seen: dict[str, SigningIdentity] = {}
    for m in re.finditer(r"([0-9A-Fa-f]{40})\s+\"([^\"]+)\"", result.stdout):
        seen.setdefault(
            m.group(1).lower(), SigningIdentity(sha1=m.group(1), name=m.group(2))
        )
    available = list(seen.values())

    if re.fullmatch(r"[0-9A-Fa-f]{40}", identity):
        matches = [i for i in available if i.sha1.lower() == identity.lower()]
    else:
        matches = [i for i in available if i.name == identity]
        if not matches:
            matches = [i for i in available if identity in i.name]

    if len(matches) == 1:
        return matches[0]

    listing = (
        "\n".join(f'  {i.sha1} "{i.name}"' for i in available)
        if available
        else "  (no valid codesigning identities found)"
    )
    problem = (
        "matches multiple identities" if matches else "does not match any identity"
    )
    raise MacOSSigningError(
        f'Signing identity "{identity}" {problem} in the keychain. '
        f"Valid codesigning identities:\n{listing}\n"
        "Pass the exact certificate name, its SHA-1 fingerprint, "
        'or "-" for ad-hoc signing.'
    )


def is_mach_o(path: Path) -> bool:
    """Check whether a file is a Mach-O binary by its magic number."""

    try:
        with open(path, "rb") as f:
            header = f.read(8)
    except OSError:
        return False
    if len(header) < 8:
        return False
    magic = header[:4]
    if magic in MACH_O_MAGICS:
        return True
    # The fat magic is shared with Java class files; a fat header follows
    # with nfat_arch (a small integer), a class file with its format version
    # (minimum 45, far above any real architecture count).
    if magic == FAT_MAGIC:
        return int.from_bytes(header[4:8], "big") < 45
    if magic == FAT_CIGAM:
        return int.from_bytes(header[4:8], "little") < 45
    return False


def find_mach_o_files(app_path: Path) -> list[Path]:
    """Find all Mach-O files in a bundle, real files only (symlinks skipped).

    Every file is checked by content — extension or executable-bit filters
    would miss binaries like versioned libraries (`libfoo.so.3`) that Python
    wheels ship, and one unsigned Mach-O fails notarization.
    """

    mach_o_files = []
    for root, _dirs, files in os.walk(app_path):
        root_path = Path(root)
        for name in files:
            path = root_path / name
            if not path.is_symlink() and is_mach_o(path):
                mach_o_files.append(path)
    return mach_o_files


def mach_o_filetype(path: Path) -> Optional[int]:
    """Return the Mach-O header filetype (e.g. MH_EXECUTE), if readable.

    For fat binaries, the first architecture slice is inspected (all slices
    of a real universal binary share one filetype).
    """

    def thin_filetype(header: bytes) -> Optional[int]:
        if len(header) < 16:
            return None
        magic = header[:4]
        if magic in MACH_O_MAGICS_BE:
            return int.from_bytes(header[12:16], "big")
        if magic in MACH_O_MAGICS_LE:
            return int.from_bytes(header[12:16], "little")
        return None

    try:
        with open(path, "rb") as f:
            header = f.read(20)
            magic = header[:4]
            if magic in {FAT_MAGIC, FAT_CIGAM} and len(header) >= 20:
                # fat_header (magic, nfat_arch) is followed by fat_arch
                # entries (cputype, cpusubtype, offset, size, align), all
                # big-endian for FAT_MAGIC.
                endianness = "big" if magic == FAT_MAGIC else "little"
                slice_offset = int.from_bytes(header[16:20], endianness)
                f.seek(slice_offset)
                return thin_filetype(f.read(16))
            return thin_filetype(header)
    except OSError:
        return None


def find_nested_bundles(app_path: Path) -> list[Path]:
    """Find nested code bundles (frameworks, helper apps) inside a bundle."""

    bundles = []
    for root, dirs, _files in os.walk(app_path):
        root_path = Path(root)
        for name in dirs:
            path = root_path / name
            if path.suffix.lower() in NESTED_BUNDLE_SUFFIXES and not path.is_symlink():
                bundles.append(path)
    return bundles


def _main_executable(app_path: Path) -> Optional[Path]:
    """Return the app's main executable per CFBundleExecutable."""

    try:
        with open(app_path / "Contents" / "Info.plist", "rb") as f:
            executable = plistlib.load(f).get("CFBundleExecutable")
    except (OSError, plistlib.InvalidFileException):
        executable = None
    return (app_path / "Contents" / "MacOS" / executable) if executable else None


def _is_bundle_main_binary(
    path: Path, app_path: Path, main_executable: Optional[Path]
) -> bool:
    """Check if a Mach-O is the main binary of the app or of a nested bundle.

    Those files are signed as part of signing their enclosing bundle; signing
    them individually first would be redundant. Any other executable — helper
    tools included — must be signed individually, because sealing a bundle
    does not sign extra Mach-O files inside it.
    """

    # <App>.app/Contents/MacOS/<CFBundleExecutable>
    if main_executable is not None and path == main_executable:
        return True
    # <Name>.framework/Versions/<V>/<Name> or <Name>.framework/<Name>
    for ancestor in path.parents:
        if ancestor == app_path:
            break
        if ancestor.suffix.lower() == ".framework":
            framework_name = ancestor.stem
            if path.name == framework_name and (
                path.parent == ancestor or path.parent.parent.name == "Versions"
            ):
                return True
    return False


def _normalized_entitlements(entitlements: Path, tmp_dir: str) -> Path:
    """Rewrite an entitlements plist in canonical form for codesign.

    codesign embeds the file verbatim and the kernel's AMFI parser is far
    stricter than CoreFoundation — e.g. it rejects self-closing tags written
    with a space (`<true />`), which plutil and Xcode accept. Round-tripping
    through plistlib guarantees a canonical file and validates it early.
    """

    try:
        with open(entitlements, "rb") as f:
            values = plistlib.load(f)
    except (OSError, plistlib.InvalidFileException, ValueError) as e:
        raise MacOSSigningError(f"Invalid entitlements file {entitlements}: {e}") from e

    normalized = Path(tmp_dir) / "entitlements.plist"
    with open(normalized, "wb") as f:
        plistlib.dump(values, f)
    return normalized


def _codesign(
    target: Path,
    identity: SigningIdentity,
    entitlements: Optional[Path] = None,
) -> None:
    args = ["codesign", "--force", "--sign", identity.sha1]
    if not identity.is_adhoc:
        args += ["--timestamp", "--options", "runtime"]
    if entitlements is not None:
        args += ["--entitlements", str(entitlements)]
    args.append(str(target))

    result = _run(args)
    if result.returncode != 0:
        raise MacOSSigningError(
            f"codesign failed for {target}:\n{result.stderr.strip()}"
        )


def sign_app(
    app_path: Union[str, Path],
    identity: SigningIdentity,
    entitlements: Optional[Union[str, Path]] = None,
    log: Callable[[str], None] = lambda message: None,
) -> int:
    """Sign a .app bundle inside out and verify the result.

    Every nested Mach-O is signed individually (deepest first), then nested
    bundles, then the app itself. Entitlements go on the app bundle and on
    standalone helper executables (MH_EXECUTE — e.g. a JIT-using helper like
    Playwright's bundled node would be killed under the hardened runtime
    without them); libraries are signed without entitlements, per Apple
    guidance. Returns the number of individually signed binaries.
    """

    app_path = Path(app_path).resolve()
    if not app_path.is_dir() or app_path.suffix != ".app":
        raise MacOSSigningError(f"Not an app bundle: {app_path}")
    entitlements = Path(entitlements) if entitlements else None
    if entitlements and not entitlements.is_file():
        raise MacOSSigningError(f"Entitlements file not found: {entitlements}")

    # Quarantine and Finder-info extended attributes make codesign fail with
    # "resource fork, Finder information, or similar detritus not allowed".
    _run(["xattr", "-cr", str(app_path)])

    mach_o_files = find_mach_o_files(app_path)
    main_executable = _main_executable(app_path)

    def depth(path: Path) -> int:
        return len(path.parts)

    inner_binaries = [
        f
        for f in mach_o_files
        if not _is_bundle_main_binary(f, app_path, main_executable)
    ]
    with tempfile.TemporaryDirectory() as tmp_dir:
        normalized = (
            _normalized_entitlements(entitlements, tmp_dir) if entitlements else None
        )

        for f in sorted(inner_binaries, key=depth, reverse=True):
            log(f"Signing {f.relative_to(app_path)}")
            is_executable = mach_o_filetype(f) == MH_EXECUTE
            _codesign(f, identity, entitlements=normalized if is_executable else None)

        for bundle in sorted(find_nested_bundles(app_path), key=depth, reverse=True):
            log(f"Signing {bundle.relative_to(app_path)}")
            _codesign(bundle, identity)

        log(f"Signing {app_path.name}")
        _codesign(app_path, identity, entitlements=normalized)

    verify_app(app_path, mach_o_files)
    return len(mach_o_files)


def verify_app(app_path: Path, mach_o_files: list[Path]) -> None:
    """Deep-verify the bundle signature and assert every Mach-O is signed.

    A shallow `codesign -v` passes even when a nested seal is broken — the
    exact failure mode that produces "app is damaged" for end users — so
    strict deep verification plus per-file coverage is the acceptance bar.
    """

    result = _run(
        ["codesign", "--verify", "--deep", "--strict", "--verbose=2", str(app_path)]
    )
    if result.returncode != 0:
        raise MacOSSigningError(
            f"Signature verification failed for {app_path}:\n{result.stderr.strip()}"
        )

    unsigned = []
    for f in mach_o_files:
        if _run(["codesign", "--verify", str(f)]).returncode != 0:
            unsigned.append(f)
    if unsigned:
        listing = "\n".join(f"  {f.relative_to(app_path)}" for f in unsigned)
        raise MacOSSigningError(
            f"Mach-O binaries left unsigned or invalid in {app_path.name}:\n{listing}"
        )


def notarize_and_staple(
    app_path: Union[str, Path],
    credentials: NotaryCredentials,
    log: Callable[[str], None] = lambda message: None,
    timeout: int = 4 * 60 * 60,
) -> None:
    """Submit a signed app to the Apple notary service and staple the ticket.

    Waits for the verdict; on rejection fetches and surfaces Apple's
    per-file notarization log, which is the only place the actual errors
    (e.g. an unsigned binary) are reported. The timeout is generous —
    submissions normally finish within minutes, but the service is known to
    back up for hours around events like WWDC.
    """

    app_path = Path(app_path).resolve()

    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / f"{app_path.stem}.zip"
        log("Archiving app for notarization")
        result = _run(
            ["ditto", "-c", "-k", "--keepParent", str(app_path), str(archive)]
        )
        if result.returncode != 0:
            raise MacOSSigningError(
                f"Failed to archive app for notarization:\n{result.stderr.strip()}"
            )

        log("Submitting to Apple notary service (this can take a few minutes)")
        try:
            result = _run(
                [
                    "xcrun",
                    "notarytool",
                    "submit",
                    str(archive),
                    "--wait",
                    "--output-format",
                    "json",
                    *credentials.as_args(),
                ],
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as e:
            raise MacOSSigningError(
                f"Notarization did not complete within {timeout // 60} minutes. "
                "The submission may still finish on Apple's side — check it "
                "with `xcrun notarytool history` (same credentials) and, once "
                f'accepted, staple manually with `xcrun stapler staple "{app_path}"`.'
            ) from e

    submission: dict = {}
    with contextlib.suppress(json.JSONDecodeError):
        submission = json.loads(result.stdout or "{}")
    status = submission.get("status")
    submission_id = submission.get("id")

    if result.returncode != 0 or status != "Accepted":
        details = ""
        if submission_id:
            log_result = _run(
                [
                    "xcrun",
                    "notarytool",
                    "log",
                    submission_id,
                    *credentials.as_args(),
                ]
            )
            details = log_result.stdout.strip() or log_result.stderr.strip()
        raise MacOSSigningError(
            f"Notarization failed (status: {status or 'unknown'}, "
            f"submission id: {submission_id or 'unknown'}).\n"
            + (f"Notary log:\n{details}\n" if details else "")
            + (f"{result.stderr.strip()}" if result.stderr else "")
        )

    log("Notarization accepted; stapling ticket")
    result = _run(["xcrun", "stapler", "staple", str(app_path)])
    if result.returncode != 0:
        raise MacOSSigningError(
            f"Stapling failed for {app_path}:\n"
            f"{result.stdout.strip()}\n{result.stderr.strip()}"
        )

    result = _run(["xcrun", "stapler", "validate", str(app_path)])
    if result.returncode != 0:
        raise MacOSSigningError(
            f"Staple validation failed for {app_path}:\n"
            f"{result.stdout.strip()}\n{result.stderr.strip()}"
        )
