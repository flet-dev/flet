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
    _is_bundle_main_binary,
    find_mach_o_files,
    find_nested_bundles,
    is_mach_o,
    mach_o_filetype,
    resolve_identity,
    sign_app,
)

MACH_O_64 = b"\xcf\xfa\xed\xfe" + b"\x00" * 12
MACH_O_32 = b"\xfe\xed\xfa\xce" + b"\x00" * 12
FAT_TWO_ARCHS = b"\xca\xfe\xba\xbe" + (2).to_bytes(4, "big") + b"\x00" * 8
JAVA_CLASS = b"\xca\xfe\xba\xbe" + (52).to_bytes(4, "big") + b"\x00" * 8

MH_DYLIB = 0x6


def thin_mach_o(filetype: int) -> bytes:
    """A minimal little-endian 64-bit Mach-O header with the given filetype."""
    return (
        b"\xcf\xfa\xed\xfe"  # MH_MAGIC_64, little-endian file
        + (0x0100000C).to_bytes(4, "little")  # cputype arm64
        + (0).to_bytes(4, "little")  # cpusubtype
        + filetype.to_bytes(4, "little")
        + b"\x00" * 16
    )


def write(path: Path, content: bytes, executable: bool = False) -> Path:
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


def test_find_nested_bundles(tmp_path):
    """Frameworks and helper bundles should be discovered, the app root not."""
    app = tmp_path / "Test.app"
    fw = app / "Contents" / "Frameworks" / "Foo.framework"
    write(fw / "Versions" / "A" / "Foo", MACH_O_64)
    helper = app / "Contents" / "Frameworks" / "Helper.app"
    write(helper / "Contents" / "MacOS" / "Helper", MACH_O_64, executable=True)

    assert sorted(find_nested_bundles(app)) == sorted([fw, helper])


def test_is_bundle_main_binary(tmp_path):
    """Bundle main binaries are signed with their bundle, everything else not."""
    app = tmp_path / "Test.app"
    main = app / "Contents" / "MacOS" / "test"
    fw = app / "Contents" / "Frameworks" / "Foo.framework"

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


SECURITY_LISTING = (
    "Policy: Code Signing\n"
    "  Matching identities\n"
    f'  1) {"a" * 40} "Developer ID Application: Jane Doe (TEAM123456)"\n'
    f'  2) {"b" * 40} "Apple Development: Jane Doe (XYZ98765)"\n'
    "     2 valid identities found\n"
)


def fake_security(monkeypatch, stdout=SECURITY_LISTING, returncode=0):
    def fake_run(args, timeout=None):
        assert args[0] == "security"
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
    with pytest.raises(MacOSSigningError, match="no valid codesigning identities"):
        resolve_identity("Developer ID Application: Jane Doe (TEAM123456)")


def test_resolve_identity_deduplicates_multi_keychain_listings(monkeypatch):
    """The same certificate listed from several keychains is not ambiguous."""
    full = "Developer ID Application: Jane Doe (TEAM123456)"
    listing = (
        f'  1) {"a" * 40} "{full}"\n'
        f'  2) {"a" * 40} "{full}"\n'
        "     2 valid identities found\n"
    )
    fake_security(monkeypatch, stdout=listing)
    assert resolve_identity(full).sha1 == "a" * 40
    assert resolve_identity("a" * 40).name == full


def test_notary_credentials_args():
    """Credential argument generation for both authentication mechanisms."""
    assert NotaryCredentials(keychain_profile="flet").as_args() == [
        "--keychain-profile",
        "flet",
    ]
    assert NotaryCredentials(
        api_key="key.p8", api_key_id="KID", api_issuer="ISS"
    ).as_args() == ["--key", "key.p8", "--key-id", "KID", "--issuer", "ISS"]


def find_real_shared_object() -> Path:
    """Locate a real Mach-O .so from the running interpreter's stdlib."""
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
    """Ad-hoc signing a minimal real bundle should produce a verifiable app."""
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


@pytest.mark.skipif(sys.platform != "darwin", reason="requires macOS codesign")
def test_sign_app_rejects_non_bundle(tmp_path):
    """Signing should refuse paths that are not .app bundles."""
    with pytest.raises(MacOSSigningError, match="Not an app bundle"):
        sign_app(tmp_path, ADHOC)
