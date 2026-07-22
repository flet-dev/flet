"""Tests for `flet_cli.utils.macos_sign`.

Most tests are platform-independent: Mach-O discovery and classification are
exercised against hand-crafted header bytes, and keychain identity
resolution against canned `security find-identity` output (no real
certificates or keychains are touched). Only the tests marked
`skipif(sys.platform != "darwin")` invoke the real `codesign` — ad-hoc
signing needs no certificate, so they run on any Mac, including CI runners.
"""

import os
import plistlib
import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path

import pytest

from flet_cli.utils import macos_sign
from flet_cli.utils.macos_sign import (
    ADHOC,
    MH_EXECUTE,
    MacOSSigningError,
    NotaryCredentials,
    SigningIdentity,
    _is_bundle_main_binary,
    app_store_entitlements,
    build_pkg,
    find_mach_o_files,
    find_nested_bundles,
    identity_team_id,
    is_mach_o,
    mach_o_filetype,
    notarize_and_staple,
    profile_application_identifier,
    profile_covers_application,
    resolve_identity,
    sign_app,
    verify_app,
    verify_app_store_app,
)

# Minimal file contents that `is_mach_o()` must classify correctly: thin
# 64-bit (little-endian file) and 32-bit (big-endian file) Mach-O headers,
# fat headers with plausible architecture counts, and a Java class file
# (shares the fat magic — see `is_mach_o()`).
MACH_O_64 = b"\xcf\xfa\xed\xfe" + b"\x00" * 12
MACH_O_32 = b"\xfe\xed\xfa\xce" + b"\x00" * 12
FAT_TWO_ARCHS = b"\xca\xfe\xba\xbe" + (2).to_bytes(4, "big") + b"\x00" * 8
FAT_64 = b"\xca\xfe\xba\xbf" + (2).to_bytes(4, "big") + b"\x00" * 8
JAVA_CLASS = b"\xca\xfe\xba\xbe" + (52).to_bytes(4, "big") + b"\x00" * 8

# Mach-O filetype for a dynamic library — the "not an executable" case for
# `mach_o_filetype()`; only MH_EXECUTE is exported by the module under test.
MH_DYLIB = 0x6


def thin_mach_o(filetype: int) -> bytes:
    """Build a minimal little-endian 64-bit Mach-O header.

    Args:
        filetype: Value for the header's `filetype` field, e.g.
            `MH_EXECUTE` or `MH_DYLIB`.

    Returns:
        Header bytes just long enough for `mach_o_filetype()` to parse.
    """
    return (
        b"\xcf\xfa\xed\xfe"  # MH_MAGIC_64, little-endian file
        + (0x0100000C).to_bytes(4, "little")  # cputype arm64
        + (0).to_bytes(4, "little")  # cpusubtype
        + filetype.to_bytes(4, "little")
        + b"\x00" * 16
    )


def write(path: Path, content: bytes, executable: bool = False) -> Path:
    """Write a file, creating parent directories as needed.

    Args:
        path: Destination file path.
        content: Bytes to write.
        executable: Whether to also set the executable bits.

    Returns:
        The written path, for inline use in assertions.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    if executable:
        path.chmod(path.stat().st_mode | 0o111)
    return path


def test_is_mach_o_detects_magic_numbers(tmp_path):
    """Thin and fat Mach-O magics should be detected, other content not."""
    assert is_mach_o(write(tmp_path / "thin64.so", MACH_O_64))
    assert is_mach_o(write(tmp_path / "thin32.so", MACH_O_32))
    assert is_mach_o(write(tmp_path / "fat.dylib", FAT_TWO_ARCHS))
    assert is_mach_o(write(tmp_path / "fat64.dylib", FAT_64))
    assert not is_mach_o(write(tmp_path / "script.so", b"#!/bin/sh\necho hi\n"))
    assert not is_mach_o(write(tmp_path / "short.so", b"\xcf"))
    assert not is_mach_o(tmp_path / "missing.so")


def test_is_mach_o_rejects_java_class_files(tmp_path):
    """The shared cafebabe magic should not match Java class files."""
    assert not is_mach_o(write(tmp_path / "Foo.class", JAVA_CLASS))


def test_find_mach_o_files_walks_bundle(tmp_path):
    """Mach-O discovery should match by content, not extension."""
    app = tmp_path / "Test.app"
    exe = write(app / "Contents" / "MacOS" / "test", MACH_O_64, executable=True)
    lib = write(app / "Contents" / "Resources" / "py.bundle" / "x.so", MACH_O_64)
    helper = write(
        app / "Contents" / "Resources" / "py.bundle" / "node", MACH_O_64, True
    )
    # versioned suffix and no exec bit — still a Mach-O, still found
    versioned = write(
        app / "Contents" / "Resources" / "py.bundle" / "libfoo.so.3", MACH_O_64
    )
    write(app / "Contents" / "Resources" / "data.txt", b"not a binary")
    write(app / "Contents" / "Resources" / "fake.so", b"just text")
    link = app / "Contents" / "Resources" / "link.so"
    link.symlink_to(lib)

    assert sorted(find_mach_o_files(app)) == sorted([exe, lib, helper, versioned])


def test_mach_o_filetype_detection(tmp_path):
    """Executable vs library filetype should be read from thin and fat headers."""
    exe = write(tmp_path / "helper", thin_mach_o(MH_EXECUTE))
    lib = write(tmp_path / "lib.so", thin_mach_o(MH_DYLIB))
    # fat wrapper: header + one arch entry whose slice is a thin executable
    slice_offset = 4096
    fat = (
        b"\xca\xfe\xba\xbe"
        + (1).to_bytes(4, "big")  # nfat_arch
        + (0x0100000C).to_bytes(4, "big")  # cputype
        + (0).to_bytes(4, "big")  # cpusubtype
        + slice_offset.to_bytes(4, "big")
        + (32).to_bytes(4, "big")  # size
        + (12).to_bytes(4, "big")  # align
    )
    fat_exe = write(
        tmp_path / "fat",
        fat + b"\x00" * (slice_offset - len(fat)) + thin_mach_o(MH_EXECUTE),
    )

    assert mach_o_filetype(exe) == MH_EXECUTE
    assert mach_o_filetype(lib) == MH_DYLIB
    assert mach_o_filetype(fat_exe) == MH_EXECUTE
    assert mach_o_filetype(write(tmp_path / "x.txt", b"hello")) is None


def test_mach_o_filetype_fat64_and_swapped(tmp_path):
    """fat64 and byte-swapped fat headers should be parsed to the right slice."""
    slice_offset = 4096
    # fat_arch_64: cputype(4) cpusubtype(4) offset(8) size(8) align(4) reserved(4)
    fat64 = (
        b"\xca\xfe\xba\xbf"
        + (1).to_bytes(4, "big")  # nfat_arch
        + (0x0100000C).to_bytes(4, "big")  # cputype
        + (0).to_bytes(4, "big")  # cpusubtype
        + slice_offset.to_bytes(8, "big")
        + (32).to_bytes(8, "big")  # size
        + (12).to_bytes(4, "big")  # align
        + (0).to_bytes(4, "big")  # reserved
    )
    fat64_exe = write(
        tmp_path / "fat64",
        fat64 + b"\x00" * (slice_offset - len(fat64)) + thin_mach_o(MH_EXECUTE),
    )
    # byte-swapped 32-bit fat header (FAT_CIGAM): all fields little-endian
    cigam = (
        b"\xbe\xba\xfe\xca"
        + (1).to_bytes(4, "little")
        + (0x0100000C).to_bytes(4, "little")
        + (0).to_bytes(4, "little")
        + slice_offset.to_bytes(4, "little")
        + (32).to_bytes(4, "little")
        + (12).to_bytes(4, "little")
    )
    cigam_lib = write(
        tmp_path / "cigam",
        cigam + b"\x00" * (slice_offset - len(cigam)) + thin_mach_o(MH_DYLIB),
    )

    assert mach_o_filetype(fat64_exe) == MH_EXECUTE
    assert mach_o_filetype(cigam_lib) == MH_DYLIB


def canonical_framework(path: Path, binary: bytes = MACH_O_64) -> Path:
    """Create a versioned framework layout codesign would accept.

    `<path>/Versions/A/<name>` plus the `Versions/Current -> A` symlink that
    marks the layout as canonical — the shape Flutter and CocoaPods produce
    and `_is_signable_framework()` requires.

    Args:
        path: The `.framework` directory to create.
        binary: Content for the framework's main binary.

    Returns:
        The framework directory, for inline use in assertions.
    """
    write(path / "Versions" / "A" / path.stem, binary)
    (path / "Versions" / "Current").symlink_to("A")
    return path


def test_find_nested_bundles(tmp_path):
    """Frameworks and helper bundles should be discovered, the app root not."""
    app = tmp_path / "Test.app"
    fw = canonical_framework(app / "Contents" / "Frameworks" / "Foo.framework")
    helper = app / "Contents" / "Frameworks" / "Helper.app"
    write(helper / "Contents" / "MacOS" / "Helper", MACH_O_64, executable=True)

    assert sorted(find_nested_bundles(app)) == sorted([fw, helper])


def test_find_nested_bundles_skips_non_canonical_frameworks(tmp_path):
    """Wheel-shipped framework layouts codesign cannot seal must be excluded.

    Wheels cannot contain symlinks, so frameworks installed from pip arrive
    either without `Versions/Current` (codesign: "bundle format
    unrecognized") or with `Current` de-symlinked into a real directory
    (codesign: "bundle format is ambiguous"). Either would abort the whole
    signing run if treated as a bundle; their binaries are signed
    individually instead.
    """
    app = tmp_path / "Test.app"
    site = app / "Contents" / "Resources" / "py.bundle" / "site-packages"
    # no Versions/Current at all
    write(site / "NoCurrent.framework" / "Versions" / "A" / "NoCurrent", MACH_O_64)
    # Current de-symlinked into a real directory
    desym = site / "DeSym.framework"
    write(desym / "Versions" / "A" / "DeSym", MACH_O_64)
    write(desym / "Versions" / "Current" / "DeSym", MACH_O_64)
    # flat framework with an Info.plist is canonical (iOS-style) — kept
    flat = site / "Flat.framework"
    write(flat / "Flat", MACH_O_64)
    write(flat / "Info.plist", b"<plist/>")
    canonical = canonical_framework(site / "Good.framework")

    assert sorted(find_nested_bundles(app)) == sorted([flat, canonical])


def test_is_bundle_main_binary(tmp_path):
    """Bundle main binaries are signed with their bundle, everything else not."""
    app = tmp_path / "Test.app"
    main = app / "Contents" / "MacOS" / "test"
    fw = canonical_framework(app / "Contents" / "Frameworks" / "Foo.framework")

    assert _is_bundle_main_binary(main, app, main)
    # a helper tool next to the main executable is NOT covered by the app seal
    assert not _is_bundle_main_binary(app / "Contents" / "MacOS" / "helper", app, main)
    assert _is_bundle_main_binary(fw / "Versions" / "A" / "Foo", app, main)
    assert _is_bundle_main_binary(fw / "Foo", app, main)
    assert not _is_bundle_main_binary(
        fw / "Versions" / "A" / "Libraries" / "bar.dylib", app, main
    )
    assert not _is_bundle_main_binary(
        app / "Contents" / "Resources" / "py.bundle" / "x.so", app, main
    )
    # a "Versions" directory elsewhere in the framework must not match
    assert not _is_bundle_main_binary(
        fw / "Resources" / "Versions" / "A" / "Foo", app, main
    )


def test_is_bundle_main_binary_ignores_non_canonical_frameworks(tmp_path):
    """Binaries of unsealable frameworks must be signed individually.

    If the framework will not be signed as a bundle, excluding its main
    binary from the individual pass would leave it entirely unsigned.
    """
    app = tmp_path / "Test.app"
    main = app / "Contents" / "MacOS" / "test"
    fw = app / "Contents" / "Resources" / "Bad.framework"
    binary = write(fw / "Versions" / "A" / "Bad", MACH_O_64)

    assert not _is_bundle_main_binary(binary, app, main)


# Canned `security find-identity -v -p codesigning` output: two distinct
# certificates that share the owner name "Jane Doe", so substring matching
# on the name alone is ambiguous while each full name stays unique.
SECURITY_LISTING = (
    "Policy: Code Signing\n"
    "  Matching identities\n"
    f'  1) {"a" * 40} "Developer ID Application: Jane Doe (TEAM123456)"\n'
    f'  2) {"b" * 40} "Apple Development: Jane Doe (XYZ98765)"\n'
    "     2 valid identities found\n"
)


def fake_security(monkeypatch, stdout=SECURITY_LISTING, returncode=0):
    """Replace the module's subprocess runner with a canned `security` result.

    `resolve_identity()` is the only code path exercised through this fake,
    and it must not invoke anything but `security` — the inner assert
    guards against that.

    Args:
        monkeypatch: pytest's monkeypatch fixture.
        stdout: Fake `security find-identity` output to return.
        returncode: Fake exit code.
    """

    def fake_run(args, timeout=None):
        assert args[0] == "security"
        # pins resolve_identity's default policy for its pre-existing callers
        assert args[args.index("-p") + 1] == "codesigning"
        return subprocess.CompletedProcess(args, returncode, stdout, "")

    monkeypatch.setattr(macos_sign, "_run", fake_run)


def test_resolve_identity_adhoc():
    """The `-` pseudo-identity should resolve without touching the keychain."""
    assert resolve_identity("-").is_adhoc


def test_resolve_identity_matches_name_sha_and_substring(monkeypatch):
    """Exact name, SHA-1 fingerprint, and unique substring should resolve."""
    fake_security(monkeypatch)
    full = "Developer ID Application: Jane Doe (TEAM123456)"
    assert resolve_identity(full).name == full
    assert resolve_identity("a" * 40).name == full
    assert resolve_identity("A" * 40).sha1 == "a" * 40
    assert resolve_identity("Developer ID").name == full
    assert resolve_identity("TEAM123456").name == full


def test_resolve_identity_rejects_ambiguous_and_unknown(monkeypatch):
    """Ambiguous substrings and unknown identities should fail fast."""
    fake_security(monkeypatch)
    with pytest.raises(MacOSSigningError, match="multiple identities"):
        resolve_identity("Jane Doe")
    with pytest.raises(MacOSSigningError, match="does not match any"):
        resolve_identity("Developer ID Installer: Someone Else")


def test_resolve_identity_empty_keychain(monkeypatch):
    """An empty keychain should produce an actionable error."""
    fake_security(monkeypatch, stdout="     0 valid identities found\n")
    with pytest.raises(MacOSSigningError, match="no valid identities"):
        resolve_identity("Developer ID Application: Jane Doe (TEAM123456)")


def test_resolve_identity_deduplicates_multi_keychain_listings(monkeypatch):
    """The same certificate listed from several keychains is not ambiguous.

    `security find-identity` prints one line per keychain occurrence, so a
    certificate installed in both the login and System keychains (a common
    state on CI runners) appears twice with an identical fingerprint. Both
    the exact-name and the SHA-1 lookup must still resolve.
    """
    full = "Developer ID Application: Jane Doe (TEAM123456)"
    listing = (
        f'  1) {"a" * 40} "{full}"\n'
        f'  2) {"a" * 40} "{full}"\n'
        "     2 valid identities found\n"
    )
    fake_security(monkeypatch, stdout=listing)
    assert resolve_identity(full).sha1 == "a" * 40
    assert resolve_identity("a" * 40).name == full


def test_resolve_identity_security_failure(monkeypatch):
    """A failing `security` invocation should produce an actionable error."""
    fake_security(monkeypatch, stdout="", returncode=1)
    with pytest.raises(MacOSSigningError, match="Unable to list"):
        resolve_identity("Developer ID Application: Jane Doe (TEAM123456)")


def test_notary_credentials_args():
    """Credential argument generation for both authentication mechanisms."""
    assert NotaryCredentials(keychain_profile="flet").as_args() == [
        "--keychain-profile",
        "flet",
    ]
    assert NotaryCredentials(
        api_key="key.p8", api_key_id="KID", api_issuer="ISS"
    ).as_args() == ["--key", "key.p8", "--key-id", "KID", "--issuer", "ISS"]


# Real (non-ad-hoc) identities for tests that never touch the keychain.
DEV_ID = SigningIdentity(
    sha1="a" * 40, name="Developer ID Application: Jane Doe (TEAM123456)"
)
APPLE_DIST = SigningIdentity(
    sha1="c" * 40, name="Apple Distribution: Jane Doe (TEAM123456)"
)
INSTALLER = SigningIdentity(
    sha1="d" * 40, name="3rd Party Mac Developer Installer: Jane Doe (TEAM123456)"
)


def build_signable_app(tmp_path: Path) -> Path:
    """Create the richest bundle layout the signing order must handle.

    Contains a main executable, a standalone helper tool, a canonical
    framework with an extra library inside, a nested helper `.app`, a
    resource-tree `.so`, and a non-canonical (wheel-style) framework —
    every classification `sign_app()` distinguishes.

    Args:
        tmp_path: Test-scoped temporary directory.

    Returns:
        The `.app` bundle directory.
    """
    app = tmp_path / "Test.app"
    with_plist = {
        "CFBundleExecutable": "test",
        "CFBundleIdentifier": "dev.flet.signtest",
    }
    write(app / "Contents" / "MacOS" / "test", thin_mach_o(MH_EXECUTE), True)
    (app / "Contents" / "Info.plist").write_bytes(plistlib.dumps(with_plist))
    write(app / "Contents" / "MacOS" / "helper", thin_mach_o(MH_EXECUTE), True)
    fw = canonical_framework(
        app / "Contents" / "Frameworks" / "Foo.framework",
        binary=thin_mach_o(MH_DYLIB),
    )
    write(fw / "Versions" / "A" / "Libraries" / "bar.dylib", thin_mach_o(MH_DYLIB))
    write(
        app
        / "Contents"
        / "Frameworks"
        / "Helper.app"
        / "Contents"
        / "MacOS"
        / "Helper",
        thin_mach_o(MH_EXECUTE),
        True,
    )
    write(
        app / "Contents" / "Resources" / "py.bundle" / "site-packages" / "x.so",
        thin_mach_o(MH_DYLIB),
    )
    write(
        app
        / "Contents"
        / "Resources"
        / "py.bundle"
        / "site-packages"
        / "Bad.framework"
        / "Versions"
        / "A"
        / "Bad",
        thin_mach_o(MH_DYLIB),
    )
    return app


def test_sign_app_order_and_entitlements_routing(tmp_path, monkeypatch):
    """Inside-out order and the entitlements-per-target rules.

    Asserts the three signing passes (inner binaries, nested bundles, the
    app last), that every binary is signed before its enclosing bundle,
    and the entitlements routing: executables and helper bundles get them,
    frameworks and libraries do not — including that the nested helper
    `.app`'s bundle signature carries entitlements (a plain bundle re-sign
    would strip the ones its main executable received in pass 1).
    """
    app = build_signable_app(tmp_path)
    entitlements = tmp_path / "Release.entitlements"
    entitlements.write_bytes(plistlib.dumps({"com.apple.security.cs.allow-jit": True}))

    calls: list[tuple[Path, bool]] = []
    # the only remaining _run call is `xattr -cr`, which does not exist on
    # non-mac platforms — stub it so this test runs everywhere
    monkeypatch.setattr(
        macos_sign,
        "_run",
        lambda args, timeout=None: subprocess.CompletedProcess(args, 0, "", ""),
    )
    monkeypatch.setattr(
        macos_sign,
        "_codesign",
        lambda target, identity, entitlements=None, hardened_runtime=True: calls.append(
            (target, entitlements is not None)
        ),
    )
    verified: dict = {}
    monkeypatch.setattr(
        macos_sign,
        "verify_app",
        lambda app_path, mach_o_files, identity: verified.update(
            app=app_path, files=mach_o_files, identity=identity
        ),
    )

    count = sign_app(app, DEV_ID, entitlements=entitlements)

    targets = [t.relative_to(app) if t != app else Path(".") for t, _ in calls]
    entitled = {(t.relative_to(app) if t != app else Path(".")): e for t, e in calls}
    order = {t: i for i, t in enumerate(targets)}

    contents = Path("Contents")
    fw = contents / "Frameworks" / "Foo.framework"
    helper_app = contents / "Frameworks" / "Helper.app"
    bad = (
        contents
        / "Resources"
        / "py.bundle"
        / "site-packages"
        / "Bad.framework"
        / "Versions"
        / "A"
        / "Bad"
    )

    # every Mach-O accounted for: 7 discovered, 5 signed individually (the
    # app's and the canonical framework's main binaries ride on bundle
    # signatures), plus 2 bundle signatures and the app itself
    assert count == 7
    assert len(verified["files"]) == 7
    assert verified["identity"] is DEV_ID
    assert set(targets) == {
        contents / "MacOS" / "helper",
        helper_app / "Contents" / "MacOS" / "Helper",
        fw / "Versions" / "A" / "Libraries" / "bar.dylib",
        contents / "Resources" / "py.bundle" / "site-packages" / "x.so",
        bad,
        fw,
        helper_app,
        Path("."),
    }

    # inside-out: binaries before their enclosing bundles, bundles before
    # the app, the app strictly last
    assert order[fw / "Versions" / "A" / "Libraries" / "bar.dylib"] < order[fw]
    assert order[helper_app / "Contents" / "MacOS" / "Helper"] < order[helper_app]
    assert order[fw] < order[Path(".")]
    assert order[helper_app] < order[Path(".")]
    assert order[Path(".")] == len(targets) - 1

    # entitlements: executables, helper bundles, and the app get them;
    # frameworks and libraries do not
    assert entitled[contents / "MacOS" / "helper"]
    assert entitled[helper_app / "Contents" / "MacOS" / "Helper"]
    assert entitled[helper_app]
    assert entitled[Path(".")]
    assert not entitled[fw]
    assert not entitled[fw / "Versions" / "A" / "Libraries" / "bar.dylib"]
    assert not entitled[contents / "Resources" / "py.bundle" / "site-packages" / "x.so"]
    # the wheel-style framework is not bundle-signed; its binary is signed
    # individually, without entitlements
    assert not entitled[bad]


# Signature detail blocks as `codesign --display --verbose=2` reports them
# (on stderr): the linker's stub signature every pip wheel ships with, a
# regular ad-hoc signature as produced by this module, and a Developer ID
# signature with its certificate chain.
DISPLAY_LINKER_SIGNED = (
    "Identifier=lib_pydantic_core.dylib\n"
    "CodeDirectory v=20400 flags=0x20002(adhoc,linker-signed) hashes=1011+0\n"
    "Signature=adhoc\n"
    "TeamIdentifier=not set\n"
)
DISPLAY_ADHOC = (
    "Identifier=x\n"
    "CodeDirectory v=20400 flags=0x2(adhoc) hashes=9+2\n"
    "Signature=adhoc\n"
    "TeamIdentifier=not set\n"
)
DISPLAY_DEV_ID = (
    "Identifier=x\n"
    "CodeDirectory v=20500 flags=0x10000(runtime) hashes=9+2\n"
    f"Authority={DEV_ID.name}\n"
    "Authority=Developer ID Certification Authority\n"
    "Authority=Apple Root CA\n"
    "TeamIdentifier=TEAM123456\n"
)


def fake_verify_runner(monkeypatch, display_by_name: dict):
    """Fake the codesign invocations `verify_app()` makes.

    Deep verification and per-file `--verify` always succeed, so the
    per-file provenance check is isolated as the deciding factor.

    Args:
        monkeypatch: pytest's monkeypatch fixture.
        display_by_name: Maps file basename to the `--display` detail block
            to report for it.
    """

    def fake_run(args, timeout=None):
        assert args[0] == "codesign"
        if "--display" in args:
            return subprocess.CompletedProcess(
                args, 0, "", display_by_name[Path(args[-1]).name]
            )
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(macos_sign, "_run", fake_run)


def test_verify_app_rejects_files_not_signed_by_identity(tmp_path, monkeypatch):
    """The coverage check must catch files that kept a foreign signature.

    A skipped file still carries the wheel's `linker-signed` stub — which
    plain `codesign --verify` accepts — so provenance, not integrity, is
    what the safety net has to assert.
    """
    app = tmp_path / "Test.app"
    good = write(app / "Contents" / "MacOS" / "test", MACH_O_64)
    skipped = write(app / "Contents" / "Resources" / "skipped.so", MACH_O_64)
    fake_verify_runner(
        monkeypatch,
        {"test": DISPLAY_DEV_ID, "skipped.so": DISPLAY_LINKER_SIGNED},
    )

    with pytest.raises(MacOSSigningError, match=r"skipped\.so"):
        verify_app(app, [good, skipped], DEV_ID)


def test_verify_app_rejects_wrong_authority(tmp_path, monkeypatch):
    """A valid signature from a different identity is still a failure."""
    app = tmp_path / "Test.app"
    binary = write(app / "Contents" / "MacOS" / "test", MACH_O_64)
    fake_verify_runner(monkeypatch, {"test": DISPLAY_ADHOC})

    with pytest.raises(MacOSSigningError, match="not signed with"):
        verify_app(app, [binary], DEV_ID)


def test_verify_app_accepts_matching_signatures(tmp_path, monkeypatch):
    """Both identity flavors pass when every file matches."""
    app = tmp_path / "Test.app"
    binary = write(app / "Contents" / "MacOS" / "test", MACH_O_64)

    fake_verify_runner(monkeypatch, {"test": DISPLAY_DEV_ID})
    verify_app(app, [binary], DEV_ID)

    fake_verify_runner(monkeypatch, {"test": DISPLAY_ADHOC})
    verify_app(app, [binary], ADHOC)


def test_verify_app_rejects_linker_signed_for_adhoc(tmp_path, monkeypatch):
    """Ad-hoc mode must still reject untouched linker-signed wheel stubs."""
    app = tmp_path / "Test.app"
    binary = write(app / "Contents" / "Resources" / "x.so", MACH_O_64)
    fake_verify_runner(monkeypatch, {"x.so": DISPLAY_LINKER_SIGNED})

    with pytest.raises(MacOSSigningError, match=r"x\.so"):
        verify_app(app, [binary], ADHOC)


def fake_notary_runner(
    monkeypatch,
    submit_stdout='{"status": "Accepted", "id": "sub-1"}',
    submit_returncode=0,
    submit_timeout=False,
    ditto_returncode=0,
    staple_returncode=0,
):
    """Fake every external command `notarize_and_staple()` runs.

    Args:
        monkeypatch: pytest's monkeypatch fixture.
        submit_stdout: Fake `notarytool submit` JSON output.
        submit_returncode: Fake `notarytool submit` exit code.
        submit_timeout: Whether submit should raise `TimeoutExpired`.
        ditto_returncode: Fake `ditto` exit code.
        staple_returncode: Fake `stapler staple` exit code.

    Returns:
        The list of invoked command lines, appended to as they happen.
    """
    invocations: list[list[str]] = []

    def fake_run(args, timeout=None):
        invocations.append(args)
        if args[0] == "ditto":
            return subprocess.CompletedProcess(args, ditto_returncode, "", "ditto err")
        if args[:3] == ["xcrun", "notarytool", "submit"]:
            if submit_timeout:
                raise subprocess.TimeoutExpired(args, timeout or 0)
            return subprocess.CompletedProcess(
                args, submit_returncode, submit_stdout, ""
            )
        if args[:3] == ["xcrun", "notarytool", "log"]:
            return subprocess.CompletedProcess(args, 0, "problems: 1 unsigned", "")
        if args[:3] == ["xcrun", "stapler", "staple"]:
            return subprocess.CompletedProcess(args, staple_returncode, "", "")
        if args[:3] == ["xcrun", "stapler", "validate"]:
            return subprocess.CompletedProcess(args, 0, "", "")
        raise AssertionError(f"unexpected command: {args}")

    monkeypatch.setattr(macos_sign, "_run", fake_run)
    return invocations


CREDENTIALS = NotaryCredentials(keychain_profile="flet")


def test_notarize_and_staple_happy_path(tmp_path, monkeypatch):
    """Archive, submit, staple, validate — in that order, with credentials."""
    invocations = fake_notary_runner(monkeypatch)

    notarize_and_staple(tmp_path / "Test.app", CREDENTIALS)

    assert [i[0] if i[0] != "xcrun" else " ".join(i[1:3]) for i in invocations] == [
        "ditto",
        "notarytool submit",
        "stapler staple",
        "stapler validate",
    ]
    submit = invocations[1]
    assert submit[-2:] == ["--keychain-profile", "flet"]
    assert "--wait" in submit


def test_notarize_and_staple_archive_failure(tmp_path, monkeypatch):
    """A ditto failure should fail before anything is submitted."""
    invocations = fake_notary_runner(monkeypatch, ditto_returncode=1)

    with pytest.raises(MacOSSigningError, match="Failed to archive"):
        notarize_and_staple(tmp_path / "Test.app", CREDENTIALS)
    assert len(invocations) == 1


def test_notarize_and_staple_rejection_fetches_log(tmp_path, monkeypatch):
    """On rejection, Apple's notarization log must surface in the error."""
    fake_notary_runner(
        monkeypatch, submit_stdout='{"status": "Invalid", "id": "sub-1"}'
    )

    with pytest.raises(MacOSSigningError, match="problems: 1 unsigned"):
        notarize_and_staple(tmp_path / "Test.app", CREDENTIALS)


def test_notarize_and_staple_timeout_gives_recovery_steps(tmp_path, monkeypatch):
    """A submit timeout should explain how to recover, not just fail."""
    fake_notary_runner(monkeypatch, submit_timeout=True)

    with pytest.raises(MacOSSigningError, match="notarytool history"):
        notarize_and_staple(tmp_path / "Test.app", CREDENTIALS, timeout=60)


def test_notarize_and_staple_staple_failure(tmp_path, monkeypatch):
    """An accepted submission with a failing staple is still an error."""
    fake_notary_runner(monkeypatch, staple_returncode=1)

    with pytest.raises(MacOSSigningError, match="Stapling failed"):
        notarize_and_staple(tmp_path / "Test.app", CREDENTIALS)


def find_real_shared_object() -> Path:
    """Locate a real Mach-O .so from the running interpreter's stdlib.

    The end-to-end signing test needs a genuine Mach-O library — codesign
    rejects the fake-header fixtures used elsewhere in this suite — and any
    C extension from the interpreter's `lib-dynload` directory fits. Skips
    the calling test on interpreters that ship without one.
    """
    dynload = Path(sysconfig.get_path("stdlib")) / "lib-dynload"
    for so in sorted(dynload.glob("*.so")):
        return so
    pytest.skip("no lib-dynload .so available")


# The exact formatting Xcode tolerates but codesign's AMFI parser rejects
# (self-closing tags with a space) — must be normalized before signing.
AMFI_HOSTILE_ENTITLEMENTS = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" \
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true />
</dict>
</plist>
"""


@pytest.mark.skipif(sys.platform != "darwin", reason="requires macOS codesign")
def test_sign_app_adhoc_end_to_end(tmp_path):
    """Ad-hoc signing a minimal real bundle should produce a verifiable app.

    Builds the smallest bundle real `codesign` accepts — an Info.plist, a
    genuine main executable (the running Python), and a genuine .so in a
    resource bundle, mirroring where flet apps keep site-packages — signs
    it with entitlements written in the AMFI-hostile `<true />` formatting
    (must be normalized, not passed through), and independently re-verifies
    the result with `codesign --verify --deep --strict`.
    """
    app = tmp_path / "Test.app"
    macos_dir = app / "Contents" / "MacOS"
    macos_dir.mkdir(parents=True)
    shutil.copy(os.path.realpath(sys.executable), macos_dir / "test")
    resources = app / "Contents" / "Resources" / "py.bundle"
    resources.mkdir(parents=True)
    shutil.copy(find_real_shared_object(), resources / "native.so")
    with open(app / "Contents" / "Info.plist", "wb") as f:
        plistlib.dump(
            {
                "CFBundleExecutable": "test",
                "CFBundleIdentifier": "dev.flet.signtest",
                "CFBundleName": "Test",
                "CFBundlePackageType": "APPL",
            },
            f,
        )
    entitlements = tmp_path / "Release.entitlements"
    entitlements.write_text(AMFI_HOSTILE_ENTITLEMENTS)

    signed = sign_app(app, ADHOC, entitlements=entitlements)

    assert signed == 2  # main executable + native.so
    result = subprocess.run(
        ["codesign", "--verify", "--deep", "--strict", str(app)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_sign_app_rejects_non_bundle(tmp_path):
    """Signing should refuse paths that are not .app bundles.

    Not darwin-gated: the check fires before any subprocess runs.
    """
    with pytest.raises(MacOSSigningError, match="Not an app bundle"):
        sign_app(tmp_path, ADHOC)


def test_sign_app_rejects_missing_inputs(tmp_path):
    """Missing entitlements/helper-entitlements/profile files fail fast."""
    app = tmp_path / "Test.app"
    write(app / "Contents" / "MacOS" / "test", MACH_O_64)

    with pytest.raises(MacOSSigningError, match="Entitlements file not found"):
        sign_app(app, ADHOC, entitlements=tmp_path / "missing.plist")
    with pytest.raises(MacOSSigningError, match="Helper entitlements file not found"):
        sign_app(app, ADHOC, helper_entitlements=tmp_path / "missing.plist")
    with pytest.raises(MacOSSigningError, match="Provisioning profile not found"):
        sign_app(app, ADHOC, provisioning_profile=tmp_path / "missing.provisionprofile")


def test_sign_app_rejects_invalid_entitlements(tmp_path, monkeypatch):
    """A non-plist entitlements file fails with a clean error, not a traceback."""
    app = tmp_path / "Test.app"
    write(app / "Contents" / "MacOS" / "test", MACH_O_64)
    bad = write(tmp_path / "bad.plist", b"not a plist at all")
    monkeypatch.setattr(
        macos_sign,
        "_run",
        lambda args, timeout=None: subprocess.CompletedProcess(args, 0, "", ""),
    )

    with pytest.raises(MacOSSigningError, match="Invalid entitlements file"):
        sign_app(app, ADHOC, entitlements=bad)


# ---------------------------------------------------------------------------
# App Store mode
# ---------------------------------------------------------------------------


def test_identity_team_id():
    """The Team ID comes from the certificate name's parenthesized suffix."""
    assert identity_team_id(APPLE_DIST) == "TEAM123456"
    assert identity_team_id(DEV_ID) == "TEAM123456"
    assert identity_team_id(ADHOC) is None
    assert identity_team_id(SigningIdentity(sha1="e" * 40, name="Self Signed")) is None


def test_resolve_identity_uses_policy(monkeypatch):
    """The find-identity policy must be forwarded — installer certs are
    invisible under `codesigning` and resolve only under `basic`."""
    captured = {}

    def fake_run(args, timeout=None):
        assert args[:3] == ["security", "find-identity", "-v"]
        captured["policy"] = args[args.index("-p") + 1]
        return subprocess.CompletedProcess(
            args, 0, f'  1) {"d" * 40} "{INSTALLER.name}"\n', ""
        )

    monkeypatch.setattr(macos_sign, "_run", fake_run)
    resolved = resolve_identity("3rd Party Mac Developer Installer", policy="basic")
    assert captured["policy"] == "basic"
    assert resolved.sha1 == "d" * 40


def test_sign_app_app_store_mode(tmp_path, monkeypatch):
    """App Store signing: no hardened runtime, helper entitlements routing,
    and the provisioning profile embedded before the first signature."""
    app = build_signable_app(tmp_path)
    app_ents = tmp_path / "app.entitlements"
    app_ents.write_bytes(plistlib.dumps({"com.apple.security.app-sandbox": True}))
    helper_ents = tmp_path / "helper.entitlements"
    helper_ents.write_bytes(
        plistlib.dumps(
            {
                "com.apple.security.app-sandbox": True,
                "com.apple.security.inherit": True,
            }
        )
    )
    profile = tmp_path / "test.provisionprofile"
    profile.write_bytes(b"fake profile bytes")

    embedded = app / "Contents" / "embedded.provisionprofile"
    codesign_calls = []
    xattr_sweeps = []

    def fake_run(args, timeout=None):
        if args[0] == "xattr":
            # the xattr sweep must scrub the *embedded* profile copy too —
            # profiles are browser downloads carrying com.apple.quarantine,
            # and App Store Connect processing rejects any quarantined file
            # in the package (error 91109, observed empirically)
            assert embedded.is_file(), "profile embedded after the xattr sweep"
            xattr_sweeps.append(args)
        if args[0] == "codesign":
            # the profile must already be in place when signing starts
            assert embedded.is_file(), "profile embedded after signing began"
            codesign_calls.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(macos_sign, "_run", fake_run)
    monkeypatch.setattr(
        macos_sign, "verify_app", lambda app_path, files, identity: None
    )

    sign_app(
        app,
        APPLE_DIST,
        entitlements=app_ents,
        helper_entitlements=helper_ents,
        provisioning_profile=profile,
        hardened_runtime=False,
    )

    # the sweep itself must happen — deleting it would resurrect the 91109
    # App Store rejection
    assert ["xattr", "-cr", str(app)] in xattr_sweeps
    assert embedded.read_bytes() == b"fake profile bytes"
    assert codesign_calls, "nothing was signed"
    for args in codesign_calls:
        assert "--options" not in args, f"hardened runtime leaked into {args}"
        assert "--timestamp" in args  # real identity keeps secure timestamps

    def entitlements_arg(args):
        return (
            args[args.index("--entitlements") + 1] if "--entitlements" in args else None
        )

    # entitlements are normalized to "<stem>-normalized.plist" copies
    by_target = {Path(args[-1]): entitlements_arg(args) for args in codesign_calls}
    helper = app / "Contents" / "MacOS" / "helper"
    assert "helper-normalized" in by_target[helper]
    assert "app-normalized" in by_target[app]
    # nested helper bundle also carries the helper entitlements
    helper_app = app / "Contents" / "Frameworks" / "Helper.app"
    assert "helper-normalized" in by_target[helper_app]


def test_verify_app_store_app(tmp_path, monkeypatch):
    """The store check needs the embedded profile and a matching sealed
    application-identifier."""
    app = tmp_path / "Test.app"
    write(app / "Contents" / "MacOS" / "test", MACH_O_64)
    (app / "Contents" / "Info.plist").write_bytes(
        plistlib.dumps({"CFBundleExecutable": "test"})
    )

    with pytest.raises(MacOSSigningError, match="missing.*embedded.provisionprofile"):
        verify_app_store_app(app, "TEAM123456.dev.example.app")

    write(app / "Contents" / "embedded.provisionprofile", b"profile")

    def fake_run_with(identifier):
        def fake_run(args, timeout=None):
            assert args[0] == "codesign" and "--entitlements" in args
            xml = plistlib.dumps(
                {"com.apple.application-identifier": identifier}
            ).decode()
            return subprocess.CompletedProcess(args, 0, xml, "")

        return fake_run

    monkeypatch.setattr(macos_sign, "_run", fake_run_with("TEAM123456.dev.example.app"))
    verify_app_store_app(app, "TEAM123456.dev.example.app")

    monkeypatch.setattr(macos_sign, "_run", fake_run_with("TEAM123456.dev.other"))
    with pytest.raises(MacOSSigningError, match="ITMS-90889"):
        verify_app_store_app(app, "TEAM123456.dev.example.app")


def test_build_pkg(tmp_path, monkeypatch):
    """productbuild + pkgutil signature check, with failure propagation."""
    app = tmp_path / "Test.app"
    app.mkdir()
    out = tmp_path / "Test.pkg"
    invocations = []

    def fake_run_rc(productbuild_rc=0, pkgutil_rc=0):
        def fake_run(args, timeout=None):
            invocations.append(args)
            rc = productbuild_rc if args[0] == "productbuild" else pkgutil_rc
            return subprocess.CompletedProcess(args, rc, "", "boom")

        return fake_run

    monkeypatch.setattr(macos_sign, "_run", fake_run_rc())
    assert build_pkg(app, INSTALLER, out) == out.resolve()
    assert invocations[0][:2] == ["productbuild", "--component"]
    assert str(app.resolve()) in invocations[0]
    assert "/Applications" in invocations[0]  # the store-mandated install root
    assert "--sign" in invocations[0] and "d" * 40 in invocations[0]
    assert invocations[1][:2] == ["pkgutil", "--check-signature"]

    monkeypatch.setattr(macos_sign, "_run", fake_run_rc(productbuild_rc=1))
    with pytest.raises(MacOSSigningError, match="productbuild failed"):
        build_pkg(app, INSTALLER, out)

    monkeypatch.setattr(macos_sign, "_run", fake_run_rc(pkgutil_rc=1))
    with pytest.raises(MacOSSigningError, match="signature verification failed"):
        build_pkg(app, INSTALLER, out)


def test_profile_application_identifier(tmp_path, monkeypatch):
    """The profile's App ID comes from its CMS-wrapped Entitlements dict."""
    plist_xml = plistlib.dumps(
        {
            "Name": "test profile",
            "Entitlements": {
                "com.apple.application-identifier": "TEAM123456.dev.example.app"
            },
        }
    ).decode()

    def fake_run(args, timeout=None):
        assert args[:3] == ["security", "cms", "-D"]
        return subprocess.CompletedProcess(args, 0, plist_xml, "")

    monkeypatch.setattr(macos_sign, "_run", fake_run)
    assert (
        profile_application_identifier(tmp_path / "p.provisionprofile")
        == "TEAM123456.dev.example.app"
    )

    monkeypatch.setattr(
        macos_sign,
        "_run",
        lambda args, timeout=None: subprocess.CompletedProcess(args, 1, "", "err"),
    )
    assert profile_application_identifier(tmp_path / "p.provisionprofile") is None


def test_sign_app_hardened_runtime_default(tmp_path, monkeypatch):
    """Developer ID signing must carry --options runtime and --timestamp.

    The one property production notarization depends on and no other test
    asserts: without the hardened runtime flag every notarization fails.
    """
    app = tmp_path / "Test.app"
    write(app / "Contents" / "MacOS" / "test", thin_mach_o(MH_EXECUTE), True)
    (app / "Contents" / "Info.plist").write_bytes(
        plistlib.dumps({"CFBundleExecutable": "test"})
    )
    write(app / "Contents" / "Resources" / "x.so", thin_mach_o(MH_DYLIB))
    codesign_calls = []

    def fake_run(args, timeout=None):
        if args[0] == "codesign":
            codesign_calls.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(macos_sign, "_run", fake_run)
    monkeypatch.setattr(
        macos_sign, "verify_app", lambda app_path, files, identity: None
    )

    sign_app(app, DEV_ID)

    assert codesign_calls
    for args in codesign_calls:
        assert "--timestamp" in args
        assert args[args.index("--options") + 1] == "runtime"


def test_profile_covers_application():
    """Explicit and wildcard App IDs; wildcards cover matching prefixes."""
    assert profile_covers_application("T.dev.example.app", "T.dev.example.app")
    assert profile_covers_application("T.*", "T.dev.example.app")
    assert profile_covers_application("T.dev.example.*", "T.dev.example.app")
    assert not profile_covers_application("T.dev.other.*", "T.dev.example.app")
    assert not profile_covers_application("T.dev.example.app", "T.dev.example.two")


def test_app_store_entitlements(tmp_path):
    """cs.* exceptions stripped; sandbox and identifiers forced in."""
    source = tmp_path / "Release.entitlements"
    source.write_bytes(
        plistlib.dumps(
            {
                "com.apple.security.cs.allow-jit": True,
                "com.apple.security.cs.allow-unsigned-executable-memory": True,
                "com.apple.security.network.client": True,
                "com.apple.security.app-sandbox": False,
            }
        )
    )

    values = app_store_entitlements(source, "T.dev.example.app", "T")

    assert values == {
        "com.apple.security.network.client": True,
        "com.apple.security.app-sandbox": True,
        "com.apple.application-identifier": "T.dev.example.app",
        "com.apple.developer.team-identifier": "T",
    }

    bad = write(tmp_path / "bad.entitlements", b"not a plist")
    with pytest.raises(MacOSSigningError, match="Invalid entitlements file"):
        app_store_entitlements(bad, "T.dev.example.app", "T")


def test_verify_app_deep_verification_failure(tmp_path, monkeypatch):
    """A broken bundle seal fails before any per-file check runs."""
    app = tmp_path / "Test.app"
    binary = write(app / "Contents" / "MacOS" / "test", MACH_O_64)

    def fake_run(args, timeout=None):
        rc = 1 if "--deep" in args else 0
        return subprocess.CompletedProcess(args, rc, "", "seal broken")

    monkeypatch.setattr(macos_sign, "_run", fake_run)
    with pytest.raises(MacOSSigningError, match="Signature verification failed"):
        verify_app(app, [binary], ADHOC)


def test_verify_app_store_app_unreadable_entitlements(tmp_path, monkeypatch):
    """A codesign --display failure is reported as such, not as a mismatch."""
    app = tmp_path / "Test.app"
    write(app / "Contents" / "MacOS" / "test", MACH_O_64)
    (app / "Contents" / "Info.plist").write_bytes(
        plistlib.dumps({"CFBundleExecutable": "test"})
    )
    write(app / "Contents" / "embedded.provisionprofile", b"profile")
    monkeypatch.setattr(
        macos_sign,
        "_run",
        lambda args, timeout=None: subprocess.CompletedProcess(args, 1, "", "no sig"),
    )

    with pytest.raises(MacOSSigningError, match="Cannot read the sealed entitlements"):
        verify_app_store_app(app, "T.dev.example.app")


def test_verify_app_store_app_missing_main_executable(tmp_path):
    """An unreadable Info.plist is a clean error, not a KeyError."""
    app = tmp_path / "Test.app"
    write(app / "Contents" / "embedded.provisionprofile", b"profile")

    with pytest.raises(MacOSSigningError, match="Cannot determine the main executable"):
        verify_app_store_app(app, "T.dev.example.app")


def test_profile_application_identifier_malformed(tmp_path, monkeypatch):
    """Unparsable CMS output degrades to None, never an exception."""
    monkeypatch.setattr(
        macos_sign,
        "_run",
        lambda args, timeout=None: subprocess.CompletedProcess(
            args, 0, "not a plist", ""
        ),
    )
    assert profile_application_identifier(tmp_path / "p.provisionprofile") is None


def test_notarize_and_staple_validate_failure(tmp_path, monkeypatch):
    """A stapled-but-unvalidatable ticket is still an error."""
    fake_notary_runner(monkeypatch)
    happy_run = macos_sign._run

    def fake_run(args, timeout=None):
        if args[:3] == ["xcrun", "stapler", "validate"]:
            return subprocess.CompletedProcess(args, 1, "", "bad ticket")
        return happy_run(args, timeout)

    monkeypatch.setattr(macos_sign, "_run", fake_run)

    with pytest.raises(MacOSSigningError, match="Staple validation failed"):
        notarize_and_staple(tmp_path / "Test.app", CREDENTIALS)


@pytest.mark.skipif(sys.platform != "darwin", reason="requires macOS codesign")
def test_sign_app_app_store_end_to_end(tmp_path):
    """App Store-shaped signing against real codesign, ad-hoc.

    Verifies the two effects unit mocks cannot: the xattr sweep strips a
    real quarantine attribute from the embedded profile copy (App Store
    Connect rejects quarantined package contents, error 91109 — observed),
    and strict deep verification proves the bundle seal covers the profile.
    """
    app = tmp_path / "Test.app"
    macos_dir = app / "Contents" / "MacOS"
    macos_dir.mkdir(parents=True)
    shutil.copy(os.path.realpath(sys.executable), macos_dir / "test")
    with open(app / "Contents" / "Info.plist", "wb") as f:
        plistlib.dump(
            {
                "CFBundleExecutable": "test",
                "CFBundleIdentifier": "dev.flet.signtest.mas",
                "CFBundleName": "Test",
                "CFBundlePackageType": "APPL",
            },
            f,
        )
    entitlements = tmp_path / "app.entitlements"
    entitlements.write_bytes(plistlib.dumps({"com.apple.security.app-sandbox": True}))
    profile = tmp_path / "test.provisionprofile"
    profile.write_bytes(b"fake profile bytes")
    subprocess.run(
        ["xattr", "-w", "com.apple.quarantine", "0083;0;test;", str(profile)],
        check=True,
    )

    sign_app(
        app,
        ADHOC,
        entitlements=entitlements,
        provisioning_profile=profile,
        hardened_runtime=False,
    )

    embedded = app / "Contents" / "embedded.provisionprofile"
    listed = subprocess.run(
        ["xattr", str(embedded)], capture_output=True, text=True
    ).stdout
    assert "com.apple.quarantine" not in listed
    result = subprocess.run(
        ["codesign", "--verify", "--deep", "--strict", str(app)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    # modifying the profile now must break the seal it is covered by
    embedded.write_bytes(b"tampered")
    result = subprocess.run(
        ["codesign", "--verify", "--deep", "--strict", str(app)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_resolve_identity_explains_expired_certificate(monkeypatch):
    """An existing-but-invalid certificate must be named, not read as absent.

    `security find-identity -v` hides expired/revoked certificates, so
    without the second (unfiltered) query the error would claim no such
    identity exists while the user sees it in Keychain Access.
    """
    full = "Developer ID Application: Jane Doe (TEAM123456)"

    def fake_run(args, timeout=None):
        assert args[0] == "security"
        if "-v" in args:
            return subprocess.CompletedProcess(
                args, 0, "     0 valid identities found\n", ""
            )
        return subprocess.CompletedProcess(
            args,
            0,
            f'  1) {"a" * 40} "{full}" (CSSMERR_TP_CERT_EXPIRED)\n',
            "",
        )

    monkeypatch.setattr(macos_sign, "_run", fake_run)
    with pytest.raises(
        MacOSSigningError,
        match=r"not valid for signing \(CSSMERR_TP_CERT_EXPIRED\)",
    ):
        resolve_identity(full)
