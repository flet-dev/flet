"""macOS code signing and notarization for built .app bundles.

Signs every Mach-O binary in a bundle "inside out" (nested code first, the
bundle itself last) as required by Apple for distribution-signed code, then
optionally submits the result to the Apple notary service and staples the
ticket. `codesign --deep` is deprecated for signing and misses Mach-O files
in resource bundles (where the embedded Python stdlib and site-packages
live), which is why binaries are discovered and signed individually.

Typical flow, as driven by `flet build macos`:

1. `resolve_identity()` — validate the requested identity against the
   keychain before spending time on anything else.
2. `sign_app()` — discover, sign, and verify the bundle.
3. `notarize_and_staple()` — optional, requires a real (non-ad-hoc)
   identity and `NotaryCredentials`.

All failures raise `MacOSSigningError` with a user-actionable message; no
other exception type is intentionally propagated.
"""

import contextlib
import json
import os
import plistlib
import re
import shutil
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
FAT_MAGIC_64 = b"\xca\xfe\xba\xbf"  # FAT_MAGIC_64 (fat_arch_64 entries)
FAT_CIGAM_64 = b"\xbf\xba\xfe\xca"

# Mach-O header filetype value for standalone executables.
MH_EXECUTE = 0x2

# Directories treated as nested code bundles that receive their own
# signature (sealing their resources) after their inner binaries are signed.
NESTED_BUNDLE_SUFFIXES = {".framework", ".app", ".appex", ".xpc"}


class MacOSSigningError(Exception):
    """Raised when signing, verification, or notarization fails."""


@dataclass
class SigningIdentity:
    """A codesigning identity resolved from the keychain.

    Obtain instances via `resolve_identity()` (or use the `ADHOC` constant)
    rather than constructing them directly, so that only identities that
    actually exist in the keychain are ever passed to `codesign`.
    """

    sha1: str
    """
    The certificate's SHA-1 fingerprint (40 hex characters), or `-` for the
    ad-hoc pseudo-identity. Passed to `codesign --sign`; the fingerprint is
    preferred over the name because it stays unambiguous when several
    certificates share a name (e.g. a renewed certificate alongside an
    expired one).
    """

    name: str
    """
    The certificate's common name, e.g.
    `Developer ID Application: Jane Doe (TEAM123456)`.
    """

    @property
    def is_adhoc(self) -> bool:
        """Whether this is the ad-hoc pseudo-identity (`-`)."""
        return self.sha1 == ADHOC_IDENTITY

    @property
    def description(self) -> str:
        """Human-readable identity name for status and log messages."""
        return self.name if not self.is_adhoc else "ad-hoc"


ADHOC = SigningIdentity(sha1=ADHOC_IDENTITY, name=ADHOC_IDENTITY)


@dataclass
class NotaryCredentials:
    """Credentials for the Apple notary service.

    Populate either `keychain_profile` alone, or the complete API key
    triple (`api_key`, `api_key_id`, `api_issuer`). A profile is not a
    different kind of credential — it is the same secrets stored once in
    the macOS keychain under a name, so `notarytool` can look them up
    instead of receiving them inline.
    """

    keychain_profile: Optional[str] = None
    """Name of a notarytool keychain profile previously
    created with `xcrun notarytool store-credentials`.
    """

    api_key: Optional[str] = None
    """Path to an App Store Connect API private key (`.p8` file)."""

    api_key_id: Optional[str] = None
    """The App Store Connect API key ID."""

    api_issuer: Optional[str] = None
    """The App Store Connect API key issuer ID."""

    def as_args(self) -> list[str]:
        """Return these credentials as `notarytool` command-line arguments.

        Used for both `notarytool submit` and `notarytool log`, which must
        authenticate with the same credentials.

        Returns:
            `["--keychain-profile", ...]` when a profile is set, otherwise
                `["--key", ..., "--key-id", ..., "--issuer", ...]`.
        """
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
    """Run a command, capturing text output and never raising on exit code.

    Args:
        args: Full command line, executable first.
        timeout: Seconds to wait before `subprocess.TimeoutExpired` is
            raised; `None` waits indefinitely. Only the notarization
            submit uses a timeout — everything else is local and fast.

    Returns:
        The completed process; callers decide how to treat `returncode`.
    """
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def resolve_identity(identity: str, policy: str = "codesigning") -> SigningIdentity:
    """Resolve a user-provided identity against the keychain.

    Fails fast — with the list of available identities — instead of letting
    a typo'd identity surface later as an opaque `codesign` error for every
    file in the bundle.

    Args:
        identity: `-` for ad-hoc signing, a 40-hex SHA-1 fingerprint, the
            full certificate name (e.g. `Developer ID Application: Jane Doe
            (TEAM123456)`), or any substring of the name that matches
            exactly one certificate (e.g. just the team ID).
        policy: `security find-identity` policy to match against.
            `codesigning` for certificates that sign code; `basic` for
            installer certificates (`3rd Party Mac Developer Installer` /
            `Mac Installer Distribution`), which sign packages, not code,
            and are invisible under the codesigning policy.

    Returns:
        The matched identity; its SHA-1 fingerprint is what is ultimately
            passed to `codesign` / `productbuild`.

    Raises:
        MacOSSigningError: If `security find-identity` fails, no identity
            matches, or the value matches more than one certificate.
    """

    identity = identity.strip()
    if identity == ADHOC_IDENTITY:
        return ADHOC

    result = _run(["security", "find-identity", "-v", "-p", policy])
    if result.returncode != 0:
        raise MacOSSigningError(
            f"Unable to list signing identities in the keychain:\n{result.stderr}"
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
        else "  (no valid identities found)"
    )
    problem = (
        "matches multiple identities" if matches else "does not match any identity"
    )
    raise MacOSSigningError(
        f'Signing identity "{identity}" {problem} in the keychain. '
        f'Valid identities for the "{policy}" policy:\n{listing}\n'
        "Pass the exact certificate name, its SHA-1 fingerprint, "
        'or "-" for ad-hoc signing.'
    )


def identity_team_id(identity: SigningIdentity) -> Optional[str]:
    """Extract the Team ID from a certificate's common name.

    Apple-issued certificate names end in the team identifier, e.g.
    `Apple Distribution: Jane Doe (TEAM123456)` — the value App Store
    signing needs for the `com.apple.application-identifier` and
    `com.apple.developer.team-identifier` entitlements.

    Args:
        identity: A resolved signing identity.

    Returns:
        The 10-character Team ID, or None for ad-hoc or non-Apple
            certificates without one.
    """

    m = re.search(r"\(([A-Z0-9]{10})\)$", identity.name)
    return m.group(1) if m else None


def is_mach_o(path: Path) -> bool:
    """Check whether a file is a Mach-O binary by its magic number.

    Recognizes thin 32/64-bit images in both byte orders as well as fat
    (universal) binaries. Java `.class` files, which share the fat magic
    `0xcafebabe`, are explicitly excluded (see inline comment).

    Args:
        path: File to inspect; only its first 8 bytes are read.

    Returns:
        True if the file starts with a Mach-O or fat header; False for
            anything else, including unreadable or too-short files.
    """

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
    if magic in {FAT_MAGIC_64, FAT_CIGAM_64}:
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

    Every file is checked by content — extension or executable-bit filters would miss
    binaries like versioned libraries (`libfoo.so.3`) or extensionless helper tools
    that Python wheels ship, and a single unsigned Mach-O fails notarization.
    Symlinks are skipped because signatures live in the real file; frameworks contain
    symlinked duplicates (`Foo.framework/Foo` → `Versions/A/Foo`) that must not be
    signed twice.

    Args:
        app_path: Bundle directory to walk recursively.

    Returns:
        Paths of all Mach-O files found, in filesystem walk order
            (callers sort as needed).
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
    """Return the Mach-O header filetype value of a binary, if readable.

    Used to tell standalone executables (`MH_EXECUTE`) apart from libraries
    and bundles (`MH_DYLIB`, `MH_BUNDLE`, ...), which determines whether a
    binary receives entitlements when signed. For fat binaries, the first
    architecture slice is inspected (all slices of a real universal binary
    share one filetype).

    Args:
        path: A Mach-O file, as identified by `is_mach_o()`.

    Returns:
        The `filetype` field of the Mach-O header (e.g. `MH_EXECUTE`), or
            None if the file is unreadable or not a recognizable Mach-O image.
    """

    def thin_filetype(header: bytes) -> Optional[int]:
        """Read the filetype field from a thin Mach-O header, if valid."""
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
            header = f.read(24)
            magic = header[:4]
            if magic in {FAT_MAGIC, FAT_CIGAM} and len(header) >= 20:
                # fat_header (magic, nfat_arch) is followed by fat_arch
                # entries (cputype, cpusubtype, offset, size, align), all
                # big-endian for FAT_MAGIC.
                endianness = "big" if magic == FAT_MAGIC else "little"
                slice_offset = int.from_bytes(header[16:20], endianness)
                f.seek(slice_offset)
                return thin_filetype(f.read(16))
            if magic in {FAT_MAGIC_64, FAT_CIGAM_64} and len(header) >= 24:
                # fat_arch_64 widens offset and size to 64 bits: cputype(4),
                # cpusubtype(4), offset(8), size(8), align(4), reserved(4).
                endianness = "big" if magic == FAT_MAGIC_64 else "little"
                slice_offset = int.from_bytes(header[16:24], endianness)
                f.seek(slice_offset)
                return thin_filetype(f.read(16))
            return thin_filetype(header)
    except OSError:
        return None


def _is_signable_framework(path: Path) -> bool:
    """Check whether a `.framework` directory can be signed as a bundle.

    codesign only accepts canonical framework layouts: versioned with a
    `Versions/Current` symlink, or flat (iOS-style) with an `Info.plist`.
    Frameworks that arrive through pip wheels are never canonical — the zip
    wheel format cannot represent symlinks, so `Versions/Current` is either
    missing (codesign: "bundle format unrecognized") or a de-symlinked real
    directory (codesign: "bundle format is ambiguous"), and hybrid layouts
    like PyQt6's produce a junk "generic bundle" signature that leaves the
    framework binary untouched. Non-canonical frameworks are therefore not
    signed as bundles at all — their Mach-O files are signed individually
    like any other library, which library validation and notarization
    accept just as well.

    Args:
        path: A directory whose name ends in `.framework`.

    Returns:
        True if the framework has a canonical layout codesign can seal.
    """

    versions = path / "Versions"
    if versions.is_dir():
        current = versions / "Current"
        return current.is_symlink() and current.exists()
    return (path / "Info.plist").is_file() or (
        path / "Resources" / "Info.plist"
    ).is_file()


def find_nested_bundles(app_path: Path) -> list[Path]:
    """Find nested code bundles inside an app bundle.

    Matches frameworks, helper apps, app extensions, and XPC services (see
    `NESTED_BUNDLE_SUFFIXES`). Each of these must receive its own signature
    — signing the framework/bundle root signs its main binary and seals its
    resources — after its inner binaries were signed, and before the
    enclosing app is sealed. Frameworks with non-canonical layouts (typical
    for frameworks shipped inside pip wheels) are excluded — codesign
    cannot seal them, so their binaries are signed individually instead
    (see `_is_signable_framework()`).

    Args:
        app_path: Bundle directory to walk recursively; the root itself is
            never included.

    Returns:
        Paths of nested bundle directories, in filesystem walk order
            (callers sort deepest-first before signing).
    """

    bundles = []
    for root, dirs, _files in os.walk(app_path):
        root_path = Path(root)
        for name in dirs:
            path = root_path / name
            if path.suffix.lower() not in NESTED_BUNDLE_SUFFIXES or path.is_symlink():
                continue
            if path.suffix.lower() == ".framework" and not _is_signable_framework(path):
                continue
            bundles.append(path)
    return bundles


def _main_executable(app_path: Path) -> Optional[Path]:
    """Return the app's main executable, as named by CFBundleExecutable.

    Args:
        app_path: The `.app` bundle directory.

    Returns:
        `Contents/MacOS/<CFBundleExecutable>`, or None when `Info.plist`
            is missing, unreadable, or has no `CFBundleExecutable` key — in
            which case no file is treated as the main executable and everything
            gets signed individually, which is safe (merely redundant).
    """

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

    A false positive here (excluding a file that is not actually a bundle
    main binary) would leave that file unsigned — `verify_app()`'s coverage
    check is the safety net for that case.

    Args:
        path: The Mach-O file to classify.
        app_path: The enclosing `.app` bundle root.
        main_executable: The app's `CFBundleExecutable` path, from
            `_main_executable()`, or None if it could not be determined.

    Returns:
        True for the app's main executable and for framework main binaries
            (`<Name>.framework/Versions/<V>/<Name>` or flat
            `<Name>.framework/<Name>`); False for everything else.
    """

    # <App>.app/Contents/MacOS/<CFBundleExecutable>
    if main_executable is not None and path == main_executable:
        return True
    # <Name>.framework/Versions/<V>/<Name> or <Name>.framework/<Name> — but
    # only for frameworks that will actually be signed as bundles; binaries
    # of non-canonical (e.g. wheel-shipped) frameworks are signed
    # individually and must not be excluded here.
    for ancestor in path.parents:
        if ancestor == app_path:
            break
        if ancestor.suffix.lower() == ".framework":
            framework_name = ancestor.stem
            if (
                path.name == framework_name
                and (
                    path.parent == ancestor
                    or path.parent.parent == ancestor / "Versions"
                )
                and _is_signable_framework(ancestor)
            ):
                return True
    return False


def _normalized_entitlements(entitlements: Path, tmp_dir: str) -> Path:
    """Rewrite an entitlements plist in canonical form for codesign.

    codesign embeds the file verbatim and the kernel's AMFI parser is far
    stricter than CoreFoundation — e.g. it rejects self-closing tags written
    with a space (`<true />`), which plutil and Xcode accept. Round-tripping
    through plistlib guarantees a canonical file and validates it early,
    with a clear error instead of `AMFIUnserializeXML` noise at sign time.

    Args:
        entitlements: The entitlements plist to normalize (any plistlib-
            readable format).
        tmp_dir: Existing directory to write the canonical copy into; the
            caller owns its lifetime (typically a `TemporaryDirectory`).

    Returns:
        Path of the canonical copy, valid as long as `tmp_dir` exists.

    Raises:
        MacOSSigningError: If the file cannot be read or parsed as a plist.
    """

    try:
        with open(entitlements, "rb") as f:
            values = plistlib.load(f)
    except (OSError, plistlib.InvalidFileException, ValueError) as e:
        raise MacOSSigningError(f"Invalid entitlements file {entitlements}: {e}") from e

    # Keep the original stem: several entitlements files (app + helper) may
    # be normalized into the same directory and must not overwrite each other.
    normalized = Path(tmp_dir) / f"{Path(entitlements).stem}-normalized.plist"
    with open(normalized, "wb") as f:
        plistlib.dump(values, f)
    return normalized


def _codesign(
    target: Path,
    identity: SigningIdentity,
    entitlements: Optional[Path] = None,
    hardened_runtime: bool = True,
) -> None:
    """Run one `codesign` invocation on a file or bundle.

    Always uses `--force` to replace the ad-hoc signature that Xcode/the
    linker already put on the build output. For real identities a secure
    timestamp is added, plus the hardened runtime (`--options runtime`)
    unless disabled — notarization requires it, App Store distribution
    forbids relying on it (sandbox is the store's containment model).
    Ad-hoc signatures get neither (a timestamp cannot be issued for them,
    and the hardened runtime would only hinder local development).

    Args:
        target: Mach-O file or bundle directory to sign. For a bundle,
            codesign signs its main binary and seals everything else as
            resources.
        identity: Identity to sign with, from `resolve_identity()`.
        entitlements: Canonical entitlements plist to embed, or None to
            sign without entitlements (correct for libraries).
        hardened_runtime: Whether real-identity signatures opt into the
            hardened runtime. True for Developer ID / notarization;
            False for App Store distribution.

    Raises:
        MacOSSigningError: If codesign exits non-zero, with its stderr.
    """
    args = ["codesign", "--force", "--sign", identity.sha1]
    if not identity.is_adhoc:
        args.append("--timestamp")
        if hardened_runtime:
            args += ["--options", "runtime"]
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
    *,
    helper_entitlements: Optional[Union[str, Path]] = None,
    provisioning_profile: Optional[Union[str, Path]] = None,
    hardened_runtime: bool = True,
) -> int:
    """Sign a .app bundle inside out and verify the result.

    The order guarantees no file is ever modified after its enclosing
    bundle's resource seal was created (which would invalidate the seal and
    make Gatekeeper report the app as "damaged"):

    1. Every nested Mach-O, deepest paths first — except bundle main
       binaries, which are covered by step 2.
    2. Nested bundles (frameworks etc.), deepest first.
    3. The app bundle itself.

    Entitlements go on the app bundle, on standalone helper executables
    (`MH_EXECUTE` — e.g. a JIT-using helper like Playwright's bundled node
    would be killed under the hardened runtime without them), and on nested
    helper bundles (`.app`/`.appex`/`.xpc`, whose main executables face the
    same hardened-runtime restrictions — and whose bundle signature would
    otherwise strip the entitlements applied in step 1); frameworks and
    libraries are signed without entitlements, per Apple guidance.
    Quarantine/Finder extended attributes are cleared first, since codesign
    refuses to sign over them.

    Args:
        app_path: The `.app` bundle to sign, e.g. `build/macos/MyApp.app`.
        identity: Identity to sign with, from `resolve_identity()` or the
            `ADHOC` constant.
        entitlements: Entitlements plist for the app and helper
            executables; normalized via `_normalized_entitlements()` before
            use, so any plistlib-readable formatting is accepted. None
            signs without entitlements.
        log: Per-file progress callback (used for `-v` output); defaults
            to a no-op.
        helper_entitlements: Separate entitlements plist for helper
            executables and nested helper bundles instead of the app's.
            App Store builds need this: helpers must carry exactly the
            sandbox `inherit` pair, not the app's entitlement set. None
            keeps the default (helpers share `entitlements`).
        provisioning_profile: Provisioning profile copied to
            `Contents/embedded.provisionprofile` before signing so the app
            seal covers it — required for App Store distribution.
        hardened_runtime: Whether to sign with the hardened runtime
            (Developer ID / notarization). App Store builds pass False —
            the store's containment model is the App Sandbox, and Apple
            re-signs store binaries on delivery.

    Returns:
        The total number of Mach-O binaries discovered in the bundle — all
            of them signed (individually, or via their enclosing bundle) and
            verified.

    Raises:
        MacOSSigningError: If `app_path` is not an app bundle, an
            entitlements or profile file is missing or invalid, any
            codesign invocation fails, or the final verification fails.
    """

    app_path = Path(app_path).resolve()
    if not app_path.is_dir() or app_path.suffix != ".app":
        raise MacOSSigningError(f"Not an app bundle: {app_path}")
    entitlements = Path(entitlements) if entitlements else None
    if entitlements and not entitlements.is_file():
        raise MacOSSigningError(f"Entitlements file not found: {entitlements}")
    helper_entitlements = Path(helper_entitlements) if helper_entitlements else None
    if helper_entitlements and not helper_entitlements.is_file():
        raise MacOSSigningError(
            f"Helper entitlements file not found: {helper_entitlements}"
        )

    # Embed the provisioning profile before anything is signed so the app
    # bundle's resource seal (created last) covers it — and before the
    # xattr sweep below, which must also scrub the embedded copy: profiles
    # are downloaded from the developer portal, so the source file carries
    # com.apple.quarantine, macOS propagates it onto the copy, and App
    # Store Connect processing rejects any quarantined file in the package
    # (error 91109) — a check `altool --validate-app` does NOT perform.
    if provisioning_profile is not None:
        provisioning_profile = Path(provisioning_profile)
        if not provisioning_profile.is_file():
            raise MacOSSigningError(
                f"Provisioning profile not found: {provisioning_profile}"
            )
        shutil.copy(
            provisioning_profile, app_path / "Contents" / "embedded.provisionprofile"
        )
        log("Embedded provisioning profile")

    # Quarantine and Finder-info extended attributes make codesign fail with
    # "resource fork, Finder information, or similar detritus not allowed",
    # and App Store Connect rejects quarantined files outright.
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
        # Helpers default to the app's entitlements; App Store builds pass a
        # dedicated sandbox-inherit plist instead.
        normalized_helper = (
            _normalized_entitlements(helper_entitlements, tmp_dir)
            if helper_entitlements
            else normalized
        )

        for f in sorted(inner_binaries, key=depth, reverse=True):
            log(f"Signing {f.relative_to(app_path)}")
            is_executable = mach_o_filetype(f) == MH_EXECUTE
            _codesign(
                f,
                identity,
                entitlements=normalized_helper if is_executable else None,
                hardened_runtime=hardened_runtime,
            )

        for bundle in sorted(find_nested_bundles(app_path), key=depth, reverse=True):
            log(f"Signing {bundle.relative_to(app_path)}")
            is_framework = bundle.suffix.lower() == ".framework"
            _codesign(
                bundle,
                identity,
                entitlements=None if is_framework else normalized_helper,
                hardened_runtime=hardened_runtime,
            )

        log(f"Signing {app_path.name}")
        _codesign(
            app_path,
            identity,
            entitlements=normalized,
            hardened_runtime=hardened_runtime,
        )

    verify_app(app_path, mach_o_files, identity)
    return len(mach_o_files)


def _signature_matches(path: Path, identity: SigningIdentity) -> bool:
    """Check that a binary's signature was produced by the given identity.

    A plain `codesign --verify` passes for signatures this tool never made
    — the linker's `adhoc,linker-signed` stub every pip wheel ships with,
    or a third party's ad-hoc signature — so integrity alone cannot prove a
    file was actually (re-)signed. Provenance is read from
    `codesign --display` instead: linker-signed stubs are rejected always,
    real identities must appear in the certificate `Authority=` chain, and
    the ad-hoc identity requires a plain `Signature=adhoc` (which is the
    best available discriminator — a pre-existing non-linker ad-hoc
    signature is indistinguishable from one made here).

    Args:
        path: A Mach-O file inside the signed bundle.
        identity: The identity the file should have been signed with.

    Returns:
        True if the signature's provenance matches the identity.
    """

    # codesign --display prints signature details on stderr.
    result = _run(["codesign", "--display", "--verbose=2", str(path)])
    if result.returncode != 0:
        return False
    info = result.stderr
    if "linker-signed" in info:
        return False
    if identity.is_adhoc:
        return "Signature=adhoc" in info
    return f"Authority={identity.name}" in info


def verify_app(
    app_path: Path, mach_o_files: list[Path], identity: SigningIdentity
) -> None:
    """Deep-verify the bundle signature and assert every Mach-O was signed.

    A shallow `codesign -v` passes even when a nested seal is broken — the
    exact failure mode that produces "app is damaged" for end users — so
    strict deep verification plus per-file coverage is the acceptance bar.
    (`--deep` is deprecated for *signing* only; it remains Apple's
    documented flag for verification.) Per-file coverage checks both
    integrity (`codesign --verify`) and provenance
    (`_signature_matches()`), because a file skipped by the signing passes
    would still verify fine under its original wheel/linker signature —
    and then be rejected by notarization or library validation.

    Args:
        app_path: The signed `.app` bundle.
        mach_o_files: Every Mach-O in the bundle (from
            `find_mach_o_files()`); each one is verified individually so
            that a file missed by the signing passes cannot slip through
            to notarization.
        identity: The identity the bundle was signed with.

    Raises:
        MacOSSigningError: If deep verification fails or any binary is
            unsigned, invalid, or not signed by `identity`, listing the
            offending files.
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
        if _run(
            ["codesign", "--verify", str(f)]
        ).returncode != 0 or not _signature_matches(f, identity):
            unsigned.append(f)
    if unsigned:
        listing = "\n".join(f"  {f.relative_to(app_path)}" for f in unsigned)
        raise MacOSSigningError(
            f"Mach-O binaries left unsigned, invalid, or not signed with "
            f'"{identity.description}" in {app_path.name}:\n{listing}'
        )


def notarize_and_staple(
    app_path: Union[str, Path],
    credentials: NotaryCredentials,
    log: Callable[[str], None] = lambda message: None,
    timeout: int = 4 * 60 * 60,
) -> None:
    """Submit a signed app to the Apple notary service and staple the ticket.

    Steps: zip the app with `ditto` (preserving bundle metadata), submit
    with `notarytool submit --wait`, and on acceptance staple the ticket to
    the `.app` itself — so however the user distributes it afterwards (DMG,
    zip), Gatekeeper can validate it even offline. On rejection, Apple's
    per-file notarization log is fetched and included in the error, as it
    is the only place the actual problems (e.g. an unsigned binary) are
    reported.

    Args:
        app_path: A `.app` bundle already signed with a Developer ID
            identity, hardened runtime, and secure timestamps (ad-hoc
            signed apps are rejected by the notary service).
        credentials: Notary service authentication.
        log: Progress callback for the coarse steps; defaults to a no-op.
        timeout: Seconds to wait for the notary verdict. Generous by
            default — submissions normally finish within minutes, but the
            service is known to back up for hours around events like WWDC.

    Raises:
        MacOSSigningError: If archiving, submission, stapling, or staple
            validation fails; on rejection the message includes Apple's
            notarization log, on timeout it includes recovery instructions
            (`notarytool history` + manual stapling).
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


def verify_app_store_app(app_path: Path, application_identifier: str) -> None:
    """Assert the App Store-specific invariants of a signed bundle.

    Complements `verify_app()` (which checks seals and signing identity)
    with the two things App Store Connect ingestion additionally requires
    and TestFlight enforces (ITMS-90889): an embedded provisioning profile,
    and the `com.apple.application-identifier` entitlement on the main
    executable matching the profile's App ID.

    Args:
        app_path: The signed `.app` bundle.
        application_identifier: Expected value, `<TEAMID>.<bundle id>`.

    Raises:
        MacOSSigningError: If the profile is missing or the sealed
            entitlements do not carry the expected identifier.
    """

    profile = app_path / "Contents" / "embedded.provisionprofile"
    if not profile.is_file():
        raise MacOSSigningError(
            f"App Store build is missing {profile} — the provisioning "
            "profile was not embedded."
        )

    main_executable = _main_executable(app_path)
    if main_executable is None:
        raise MacOSSigningError(
            f"Cannot determine the main executable of {app_path} from its Info.plist."
        )
    # codesign prints the entitlements XML on stdout, diagnostics on stderr.
    result = _run(
        [
            "codesign",
            "--display",
            "--entitlements",
            "-",
            "--xml",
            str(main_executable),
        ]
    )
    entitlements: dict = {}
    with contextlib.suppress(plistlib.InvalidFileException, ValueError):
        entitlements = plistlib.loads(result.stdout.encode())
    found = entitlements.get("com.apple.application-identifier")
    if found != application_identifier:
        raise MacOSSigningError(
            "The main executable's sealed entitlements carry "
            f"com.apple.application-identifier={found!r}, expected "
            f"{application_identifier!r}. TestFlight rejects such builds "
            "(ITMS-90889)."
        )


def build_pkg(
    app_path: Union[str, Path],
    installer_identity: SigningIdentity,
    output: Union[str, Path],
    log: Callable[[str], None] = lambda message: None,
) -> Path:
    """Build the signed installer package App Store Connect ingests.

    Store submissions are uploaded as a `.pkg` produced by `productbuild`
    and signed with an installer certificate (`3rd Party Mac Developer
    Installer` / `Mac Installer Distribution`) — a different certificate
    type from the one that signed the app; resolve it with
    `resolve_identity(..., policy="basic")`. The result is verified with
    `pkgutil --check-signature`.

    Args:
        app_path: The signed (App Store-style) `.app` bundle.
        installer_identity: Installer certificate identity.
        output: Path of the `.pkg` to write; replaced if it exists.
        log: Progress callback; defaults to a no-op.

    Returns:
        The path of the signed package.

    Raises:
        MacOSSigningError: If `productbuild` fails or the package's
            signature does not verify.
    """

    app_path = Path(app_path).resolve()
    output = Path(output).resolve()
    output.unlink(missing_ok=True)

    log(f"Building installer package {output.name}")
    result = _run(
        [
            "productbuild",
            "--component",
            str(app_path),
            "/Applications",
            "--sign",
            installer_identity.sha1,
            str(output),
        ]
    )
    if result.returncode != 0:
        raise MacOSSigningError(
            f"productbuild failed for {app_path}:\n{result.stderr.strip()}"
        )

    result = _run(["pkgutil", "--check-signature", str(output)])
    if result.returncode != 0:
        raise MacOSSigningError(
            f"Installer package signature verification failed for {output}:\n"
            f"{result.stdout.strip()}\n{result.stderr.strip()}"
        )
    return output


def profile_application_identifier(profile: Union[str, Path]) -> Optional[str]:
    """Read the App ID a provisioning profile authorizes.

    Used to catch a profile/bundle-id mismatch before uploading — App Store
    Connect rejects mismatches only after processing (ITMS-90889), which is
    a slow way to find a wrong file path.

    Args:
        profile: A `.provisionprofile` file (CMS-wrapped plist).

    Returns:
        The profile's `com.apple.application-identifier` entitlement (e.g.
            `TEAM123456.com.example.app`), or None if the profile cannot be
            read or parsed.
    """

    result = _run(["security", "cms", "-D", "-i", str(profile)])
    if result.returncode != 0:
        return None
    try:
        values = plistlib.loads(result.stdout.encode())
        return values["Entitlements"]["com.apple.application-identifier"]
    except (plistlib.InvalidFileException, ValueError, KeyError, TypeError):
        return None
