"""Tests for `flet build macos`'s signing orchestration.

Covers the distribution-lane dispatch and the pre-build preflight in
`flet_cli.commands.build.Command` — the layer between the CLI options and
`flet_cli.utils.macos_sign` (which has its own suite). The command object
is constructed without argparse and driven with fake options/pyproject
values; every `macos_sign` entry point is stubbed, so no keychain,
codesign, or network is touched.
"""

import argparse
import plistlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from flet_cli.commands import build as build_module
from flet_cli.commands.build import Command
from flet_cli.utils.macos_sign import MacOSSigningError, SigningIdentity

DEV_ID = SigningIdentity(
    sha1="a" * 40, name="Developer ID Application: Jane Doe (TEAM123456)"
)
APPLE_DIST = SigningIdentity(
    sha1="c" * 40, name="Apple Distribution: Jane Doe (TEAM123456)"
)


class Exit(Exception):
    """Captures `cleanup(1, message)` calls, which normally sys.exit."""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"cleanup({code}): {message}")


def make_command(
    tmp_path: Path,
    options: dict | None = None,
    pyproject: dict | None = None,
    info_plist: dict | None = None,
) -> Command:
    """Build a Command instance wired for signing tests, without argparse.

    Args:
        tmp_path: Test-scoped directory; receives out_dir and flutter_dir.
        options: CLI option values; unset signing options default to None.
        pyproject: Fake `tool.flet.*` values, keyed by full dotted path.
        info_plist: Resolved Info.plist dict for `template_data`.

    Returns:
        A command whose `cleanup` raises `Exit` instead of exiting.
    """
    cmd = object.__new__(Command)
    defaults = dict(
        macos_distribution=None,
        macos_signing_identity=None,
        macos_notary_profile=None,
        macos_provisioning_profile=None,
        macos_installer_identity=None,
    )
    defaults.update(options or {})
    cmd.options = argparse.Namespace(**defaults)
    config = pyproject or {}
    cmd.get_pyproject = lambda key=None: config.get(key)
    cmd.template_data = {"options": {"info_plist": info_plist or {}}}
    cmd.python_app_path = tmp_path
    cmd.out_dir = tmp_path / "out"
    cmd.out_dir.mkdir(exist_ok=True)
    cmd.rel_out_dir = "out"
    cmd.flutter_dir = tmp_path / "flutter"
    entitlements = cmd.flutter_dir / "macos" / "Runner" / "Release.entitlements"
    entitlements.parent.mkdir(parents=True, exist_ok=True)
    entitlements.write_bytes(plistlib.dumps({"com.apple.security.cs.allow-jit": True}))
    cmd.verbose = 0
    cmd.emojis = {"checkmark": ""}
    cmd.update_status = lambda *args, **kwargs: None

    def cleanup(code, message=None, **kwargs):
        raise Exit(code, message)

    cmd.cleanup = cleanup
    return cmd


def forbid_keychain(monkeypatch):
    """Make any identity resolution fail the test."""
    monkeypatch.setattr(
        build_module,
        "resolve_identity",
        lambda *a, **k: pytest.fail("resolve_identity called unexpectedly"),
    )


# ---------------------------------------------------------------------------
# resolve_macos_distribution
# ---------------------------------------------------------------------------


def test_distribution_resolution_order(tmp_path):
    """CLI beats pyproject; default is 'none'."""
    assert make_command(tmp_path).resolve_macos_distribution() == "none"
    assert (
        make_command(
            tmp_path, pyproject={"tool.flet.macos.signing.distribution": "developer-id"}
        ).resolve_macos_distribution()
        == "developer-id"
    )
    assert (
        make_command(
            tmp_path,
            options={"macos_distribution": "app-store"},
            pyproject={"tool.flet.macos.signing.distribution": "developer-id"},
        ).resolve_macos_distribution()
        == "app-store"
    )


def test_distribution_rejects_invalid_configured_value(tmp_path):
    """A pyproject typo must fail loudly, not fall through to an ad-hoc build.

    argparse `choices=` only protects the CLI layer.
    """
    cmd = make_command(
        tmp_path, pyproject={"tool.flet.macos.signing.distribution": "app_store"}
    )
    with pytest.raises(Exit, match="Invalid macOS distribution 'app_store'"):
        cmd.resolve_macos_distribution()


# ---------------------------------------------------------------------------
# preflight_macos_signing (pre-build fail-fast)
# ---------------------------------------------------------------------------


def test_preflight_noop_without_signing_config(tmp_path, monkeypatch):
    """A build with no signing configured must not touch the keychain."""
    forbid_keychain(monkeypatch)
    make_command(tmp_path).preflight_macos_signing()


def test_preflight_developer_id_resolves_identity_and_credentials(
    tmp_path, monkeypatch
):
    """The developer-id lane pre-resolves the identity and notary credentials."""
    calls = []
    monkeypatch.setattr(
        build_module,
        "resolve_identity",
        lambda identity, policy="codesigning", types=None: (
            calls.append(types),
            DEV_ID,
        )[1],
    )
    cmd = make_command(
        tmp_path,
        pyproject={"tool.flet.macos.signing.distribution": "developer-id"},
        options={"macos_notary_profile": "flet-notary"},
    )
    cmd.preflight_macos_signing()
    assert calls == [build_module.DEVELOPER_ID_CERTIFICATE_TYPES]

    # missing credentials must fail before the build
    cmd = make_command(
        tmp_path, pyproject={"tool.flet.macos.signing.distribution": "developer-id"}
    )
    with pytest.raises(Exit, match="credentials"):
        cmd.preflight_macos_signing()


def test_preflight_developer_id_surfaces_identity_errors(tmp_path, monkeypatch):
    """Keychain resolution failures fail the build in seconds, not minutes."""

    def raise_ambiguous(*args, **kwargs):
        raise MacOSSigningError("matches multiple identities")

    monkeypatch.setattr(build_module, "resolve_identity", raise_ambiguous)
    cmd = make_command(
        tmp_path,
        pyproject={"tool.flet.macos.signing.distribution": "developer-id"},
        options={"macos_notary_profile": "flet-notary"},
    )
    with pytest.raises(Exit, match="matches multiple identities"):
        cmd.preflight_macos_signing()


def test_preflight_app_store_requirements(tmp_path, monkeypatch):
    """The app-store lane pre-checks both identities, profile, and category."""
    monkeypatch.setattr(
        build_module,
        "resolve_identity",
        lambda identity, policy="codesigning", types=None: APPLE_DIST,
    )
    profile = tmp_path / "test.provisionprofile"

    def command(**overrides):
        return make_command(
            tmp_path,
            pyproject={
                "tool.flet.macos.signing.distribution": "app-store",
                "tool.flet.macos.signing.provisioning_profile": str(profile),
            },
            **overrides,
        )

    with pytest.raises(Exit, match="Provisioning profile not found"):
        command().preflight_macos_signing()

    profile.write_bytes(b"profile")
    with pytest.raises(Exit, match="LSApplicationCategoryType"):
        command().preflight_macos_signing()

    command(
        info_plist={"LSApplicationCategoryType": "public.app-category.utilities"}
    ).preflight_macos_signing()


# ---------------------------------------------------------------------------
# sign_macos_app lane dispatch
# ---------------------------------------------------------------------------


def stub_lanes(monkeypatch, cmd):
    """Stub every lane body, returning a recorder of what ran."""
    ran = SimpleNamespace(signed=None, notarized=False, store=False)
    monkeypatch.setattr(
        build_module,
        "resolve_identity",
        lambda identity, policy="codesigning", types=None: DEV_ID,
    )
    monkeypatch.setattr(
        build_module,
        "sign_app",
        lambda *a, **k: setattr(ran, "signed", a[1]) or 1,
    )
    monkeypatch.setattr(
        build_module,
        "notarize_and_staple",
        lambda *a, **k: setattr(ran, "notarized", True),
    )
    cmd._macos_notary_credentials = lambda: object()
    cmd._sign_macos_app_store = lambda *a, **k: setattr(ran, "store", True)
    return ran


def test_dispatch_none_without_identity_is_noop(tmp_path, monkeypatch):
    """Bare builds never sign and never touch the keychain."""
    cmd = make_command(tmp_path)
    forbid_keychain(monkeypatch)
    cmd.sign_macos_app()


def test_dispatch_none_with_identity_signs_only(tmp_path, monkeypatch):
    """The plain lane signs but never notarizes."""
    cmd = make_command(tmp_path, options={"macos_signing_identity": "Developer ID"})
    (cmd.out_dir / "Test.app").mkdir()
    ran = stub_lanes(monkeypatch, cmd)
    cmd.sign_macos_app()
    assert ran.signed is DEV_ID and not ran.notarized and not ran.store


def test_dispatch_developer_id_signs_and_notarizes(tmp_path, monkeypatch):
    """The developer-id lane is sign + notarize, no store packaging."""
    cmd = make_command(
        tmp_path, pyproject={"tool.flet.macos.signing.distribution": "developer-id"}
    )
    (cmd.out_dir / "Test.app").mkdir()
    ran = stub_lanes(monkeypatch, cmd)
    cmd.sign_macos_app()
    assert ran.signed is DEV_ID and ran.notarized and not ran.store


def test_dispatch_app_store_routes_to_store_lane(tmp_path, monkeypatch):
    """The app-store lane delegates wholesale to _sign_macos_app_store."""
    cmd = make_command(
        tmp_path, pyproject={"tool.flet.macos.signing.distribution": "app-store"}
    )
    (cmd.out_dir / "Test.app").mkdir()
    ran = stub_lanes(monkeypatch, cmd)
    cmd.sign_macos_app()
    assert ran.store and ran.signed is None and not ran.notarized


def test_dispatch_cli_flips_lane_over_pyproject(tmp_path, monkeypatch):
    """The one-pyproject-two-lanes workflow: CLI lane wins wholesale."""
    cmd = make_command(
        tmp_path,
        options={"macos_distribution": "app-store"},
        pyproject={"tool.flet.macos.signing.distribution": "developer-id"},
    )
    (cmd.out_dir / "Test.app").mkdir()
    ran = stub_lanes(monkeypatch, cmd)
    cmd.sign_macos_app()
    assert ran.store and not ran.notarized


# ---------------------------------------------------------------------------
# Per-lane subtables: [tool.flet.macos.signing.<lane>]
# ---------------------------------------------------------------------------
# The fake get_pyproject is an exact-key dict, so lane subtables appear both
# as their dotted leaf paths (what macos_signing_setting queries) and, for
# the subtable-name validation, as the parent "tool.flet.macos.signing"
# dict.


def test_signing_setting_precedence(tmp_path, monkeypatch):
    """CLI > lane subtable > flat key > env var — lane beats flat."""
    monkeypatch.setenv("FLET_MACOS_SIGNING_IDENTITY", "from-env")
    cmd = make_command(
        tmp_path,
        pyproject={
            "tool.flet.macos.signing.developer-id.identity": "from-lane",
            "tool.flet.macos.signing.identity": "from-flat",
        },
    )

    setting = lambda cli, lane: cmd.macos_signing_setting(  # noqa: E731
        cli, lane, "identity", "FLET_MACOS_SIGNING_IDENTITY"
    )
    assert setting("from-cli", "developer-id") == "from-cli"
    assert setting(None, "developer-id") == "from-lane"
    assert setting(None, "app-store") == "from-flat"  # no app-store subtable

    cmd_flatless = make_command(
        tmp_path,
        pyproject={"tool.flet.macos.signing.developer-id.identity": "from-lane"},
    )
    assert (
        cmd_flatless.macos_signing_setting(
            None, "app-store", "identity", "FLET_MACOS_SIGNING_IDENTITY"
        )
        == "from-env"
    )
    # the plain lane never consults a subtable
    assert (
        cmd_flatless.macos_signing_setting(
            None, "none", "identity", "FLET_MACOS_SIGNING_IDENTITY"
        )
        == "from-env"
    )


def test_lane_subtables_pin_identities_per_lane(tmp_path, monkeypatch):
    """One pyproject can pin a different certificate per lane."""
    pyproject = {
        "tool.flet.macos.signing.distribution": "developer-id",
        "tool.flet.macos.signing.developer-id.identity": "Developer ID pinned",
        "tool.flet.macos.signing.app-store.identity": "Apple Distribution pinned",
    }
    seen = []

    def record_identity(monkeypatch):
        # applied after stub_lanes, which installs its own resolve_identity
        monkeypatch.setattr(
            build_module,
            "resolve_identity",
            lambda identity, policy="codesigning", types=None: (
                seen.append(identity),
                DEV_ID,
            )[1],
        )

    cmd = make_command(tmp_path, pyproject=pyproject)
    (cmd.out_dir / "Test.app").mkdir()
    stub_lanes(monkeypatch, cmd)
    record_identity(monkeypatch)
    cmd.sign_macos_app()
    assert seen[-1] == "Developer ID pinned"

    cmd = make_command(
        tmp_path, options={"macos_distribution": "app-store"}, pyproject=pyproject
    )
    (cmd.out_dir / "Test.app").mkdir(exist_ok=True)
    stub_lanes(monkeypatch, cmd)
    record_identity(monkeypatch)
    cmd.sign_macos_app()
    assert seen[-1] == "Apple Distribution pinned"


def test_unknown_lane_subtable_rejected(tmp_path):
    """A misnamed subtable fails loudly instead of being silently ignored."""
    cmd = make_command(
        tmp_path,
        pyproject={
            "tool.flet.macos.signing": {
                "distribution": "developer-id",
                "app_store": {"identity": "never read"},
            },
            "tool.flet.macos.signing.distribution": "developer-id",
        },
    )
    with pytest.raises(Exit, match=r"Unknown lane subtable .*signing\.app_store"):
        cmd.resolve_macos_distribution()


def test_fully_lane_organized_pyproject(tmp_path, monkeypatch):
    """Lane-only keys may live in their lane's subtable instead of flat.

    notary_profile is only read by the developer-id lane and
    provisioning_profile only by the app-store lane, so a config with no
    flat keys at all must resolve identically.
    """
    monkeypatch.setattr(
        build_module,
        "resolve_identity",
        lambda identity, policy="codesigning", types=None: APPLE_DIST,
    )
    profile = tmp_path / "test.provisionprofile"
    profile.write_bytes(b"profile")
    pyproject = {
        "tool.flet.macos.signing.distribution": "developer-id",
        "tool.flet.macos.signing.developer-id.notary_profile": "flet-notary",
        "tool.flet.macos.signing.app-store.provisioning_profile": str(profile),
    }

    # developer-id lane finds its notary profile in the subtable
    cmd = make_command(tmp_path, pyproject=pyproject)
    assert cmd._macos_notary_credentials().keychain_profile == "flet-notary"

    # app-store lane finds its provisioning profile in the subtable
    cmd = make_command(
        tmp_path, options={"macos_distribution": "app-store"}, pyproject=pyproject
    )
    assert cmd._macos_store_profile_path() == profile.resolve()
