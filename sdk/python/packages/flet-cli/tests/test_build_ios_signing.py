"""
Tests for `flet build ipa`'s provisioning-profile preflight.

Xcode resolves the profile only when it archives, minutes into a build, so
the command checks the same specifier up front. These cover each way that
check can reject a configuration, both accepted specifier forms, and the
unsigned build that must skip it.
"""

import argparse
import datetime
from pathlib import Path

import pytest

from flet_cli.commands import build as build_module
from flet_cli.commands.build import Command
from flet_cli.utils.ios_sign import ProvisioningProfile, find_provisioning_profile


class Exit(Exception):
    """Captures `cleanup(1, message)` calls, which normally sys.exit."""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"cleanup({code}): {message}")


def profile(
    name="Store Profile",
    uuid="1111-2222",
    team_id="TEAM123456",
    app_id="TEAM123456.com.example.app",
    expires=None,
) -> ProvisioningProfile:
    """Build a profile fixture; `expires` defaults to a year from now."""
    if expires is None:
        expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            days=365
        )
    return ProvisioningProfile(
        name=name,
        uuid=uuid,
        team_id=team_id,
        application_identifier=app_id,
        expires=expires,
        path=Path("/tmp") / f"{uuid}.mobileprovision",
    )


def make_command(template_data: dict) -> Command:
    """A Command whose cleanup raises instead of exiting."""
    cmd = object.__new__(Command)
    cmd.options = argparse.Namespace()
    cmd.target_platform = "ipa"
    cmd.template_data = template_data

    def cleanup(code, message=None, **kwargs):
        raise Exit(code, message)

    cmd.cleanup = cleanup
    return cmd


def stub_profiles(monkeypatch, profiles):
    monkeypatch.setattr(
        build_module, "installed_provisioning_profiles", lambda: profiles
    )


def test_unsigned_build_skips_the_check(monkeypatch):
    """No profile configured is a supported (unsigned .xcarchive) build."""
    monkeypatch.setattr(
        build_module,
        "installed_provisioning_profiles",
        lambda: pytest.fail("keychain/profile scan not expected"),
    )
    make_command({"ios_provisioning_profile": None}).preflight_ios_signing()


def test_missing_profile_lists_installed_ones(monkeypatch):
    """The message must name alternatives — Xcode's cannot."""
    stub_profiles(monkeypatch, [profile(name="Store Profile")])
    cmd = make_command({"ios_provisioning_profile": "Typo Profile"})

    with pytest.raises(Exit) as exc:
        cmd.preflight_ios_signing()
    assert "'Typo Profile' is not installed" in exc.value.message
    assert "Store Profile" in exc.value.message


def test_profile_resolves_by_name_or_uuid(monkeypatch):
    """Xcode accepts either specifier form, so both must pass preflight."""
    installed = [profile(name="Store Profile", uuid="ABCD-1234")]
    stub_profiles(monkeypatch, installed)

    for specifier in ("Store Profile", "ABCD-1234"):
        make_command(
            {
                "ios_provisioning_profile": specifier,
                "ios_team_id": "TEAM123456",
                "bundle_id": "com.example.app",
            }
        ).preflight_ios_signing()


def test_expired_profile_rejected(monkeypatch):
    """An expired profile fails signing; say so instead of building first."""
    past = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    stub_profiles(monkeypatch, [profile(expires=past)])
    cmd = make_command({"ios_provisioning_profile": "Store Profile"})

    with pytest.raises(Exit, match="expired"):
        cmd.preflight_ios_signing()


def test_team_mismatch_rejected(monkeypatch):
    """Xcode matches the profile within the team, so both must agree."""
    stub_profiles(monkeypatch, [profile(team_id="TEAM123456")])
    cmd = make_command(
        {"ios_provisioning_profile": "Store Profile", "ios_team_id": "OTHER99999"}
    )

    with pytest.raises(Exit, match="belongs to team TEAM123456"):
        cmd.preflight_ios_signing()


def test_bundle_id_not_covered_rejected(monkeypatch):
    """A profile for another App ID cannot sign this app."""
    stub_profiles(monkeypatch, [profile(app_id="TEAM123456.com.example.other")])
    cmd = make_command(
        {"ios_provisioning_profile": "Store Profile", "bundle_id": "com.example.app"}
    )

    with pytest.raises(Exit, match="does not cover"):
        cmd.preflight_ios_signing()


def test_wildcard_profile_covers_bundle_id(monkeypatch):
    """Wildcard App IDs authorize every bundle id sharing their prefix."""
    stub_profiles(monkeypatch, [profile(app_id="TEAM123456.com.example.*")])
    make_command(
        {"ios_provisioning_profile": "Store Profile", "bundle_id": "com.example.app"}
    ).preflight_ios_signing()


def test_find_profile_ignores_surrounding_whitespace():
    """A stray space in pyproject shouldn't look like a missing profile."""
    installed = [profile(name="Store Profile")]
    assert find_provisioning_profile("  Store Profile  ", installed) is not None
