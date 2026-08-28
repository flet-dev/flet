"""Tests for `flet build ipa`."""

import argparse
import datetime
from pathlib import Path
from typing import Optional

import pytest

from flet_cli.commands import build as build_module
from flet_cli.commands.build import Command
from flet_cli.utils.ios_sign import ProvisioningProfile, find_provisioning_profile


class Exit(Exception):
    """Captures `cleanup(code, message)` calls, which normally sys.exit."""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"cleanup({code}): {message}")


def make_command(
    tmp_path: Path,
    target_platform: str = "ipa",
    template_data: Optional[dict] = None,
) -> Command:
    """
    Build a Command instance for iOS build tests.

    Uses the real constructor so `platforms` — and the status texts the
    build actually reports with — are the production ones.

    Args:
        tmp_path: Test-scoped directory; receives out_dir and flutter_dir.
        target_platform: Platform whose behaviour is under test.
        template_data: Resolved build settings, as `setup_template_data`
            would leave them.

    Returns:
        A command with empty output directories, whose `cleanup` raises
            `Exit` instead of exiting.
    """
    cmd = Command(argparse.ArgumentParser())
    cmd.target_platform = target_platform
    cmd.template_data = template_data if template_data is not None else {}
    cmd.out_dir = tmp_path / "out"
    cmd.flutter_dir = tmp_path / "flutter"
    for directory in (cmd.out_dir, cmd.flutter_dir):
        directory.mkdir(parents=True, exist_ok=True)

    def cleanup(code, message=None, **kwargs):
        raise Exit(code, message)

    cmd.cleanup = cleanup
    return cmd


def make_profile(
    name: str = "Store Profile",
    uuid: str = "1111-2222",
    team_id: Optional[str] = "TEAM123456",
    app_id: Optional[str] = "TEAM123456.com.example.app",
    expires: Optional[datetime.datetime] = None,
) -> ProvisioningProfile:
    """
    Build a provisioning profile fixture.

    Args:
        name: Profile name, as the portal shows it.
        uuid: Profile UUID.
        team_id: Team the profile belongs to.
        app_id: App ID it authorizes, explicit or wildcard.
        expires: Expiration date; defaults to a year from now.

    Returns:
        A profile as `installed_provisioning_profiles()` would report it.
    """
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


def stub_installed_profiles(monkeypatch, profiles: list[ProvisioningProfile]) -> None:
    """Serve `profiles` instead of reading the machine's profile directories."""
    monkeypatch.setattr(
        build_module, "installed_provisioning_profiles", lambda: profiles
    )


# ---------------------------------------------------------------------------
# build output reporting
# ---------------------------------------------------------------------------


class TestBuildOutput:
    """What the command reports having produced.

    An unsigned build yields only an `.xcarchive`, so the reported artifact
    comes from what is on disk rather than from the target's usual output.
    """

    def test_reports_xcarchive_when_no_ipa_produced(self, tmp_path):
        """An unsigned build must not announce an .ipa that was never written."""
        cmd = make_command(tmp_path)
        (cmd.out_dir / "MyApp.xcarchive").mkdir()

        assert cmd.built_ipa() is False
        assert cmd.describe_build_output() == ".xcarchive (Xcode archive) for iOS"

    def test_reports_ipa_when_produced(self, tmp_path):
        """A signed build keeps the platform's normal status text."""
        cmd = make_command(tmp_path)
        (cmd.out_dir / "MyApp.ipa").write_bytes(b"")

        assert cmd.built_ipa() is True
        assert cmd.describe_build_output() == cmd.platforms["ipa"]["status_text"]

    def test_ipa_found_before_outputs_are_copied(self, tmp_path):
        """The check also runs right after the build, from the Flutter project."""
        cmd = make_command(tmp_path)
        ipa_dir = cmd.flutter_dir / "build" / "ios" / "ipa"
        ipa_dir.mkdir(parents=True)
        (ipa_dir / "MyApp.ipa").write_bytes(b"")

        assert cmd.built_ipa() is True

    def test_other_platforms_keep_their_status_text(self, tmp_path):
        """The .ipa-specific check must not leak into other targets."""
        cmd = make_command(tmp_path, target_platform="macos")
        assert cmd.describe_build_output() == cmd.platforms["macos"]["status_text"]


# ---------------------------------------------------------------------------
# provisioning profile preflight
# ---------------------------------------------------------------------------


class TestProvisioningPreflight:
    """Resolution of the configured profile before the build starts.

    Xcode resolves the profile only when it archives, so the command checks
    the same specifier up front — every rejection below would otherwise
    surface minutes later, from Xcode.
    """

    def test_unsigned_build_skips_the_check(self, tmp_path, monkeypatch):
        """No profile configured is a supported (unsigned .xcarchive) build."""
        monkeypatch.setattr(
            build_module,
            "installed_provisioning_profiles",
            lambda: pytest.fail("profile scan not expected"),
        )
        make_command(
            tmp_path, template_data={"ios_provisioning_profile": None}
        ).preflight_ios_signing()

    def test_missing_profile_lists_installed_ones(self, tmp_path, monkeypatch):
        """The message must name alternatives — Xcode's cannot."""
        stub_installed_profiles(monkeypatch, [make_profile(name="Store Profile")])
        cmd = make_command(
            tmp_path, template_data={"ios_provisioning_profile": "Typo Profile"}
        )

        with pytest.raises(Exit) as exc:
            cmd.preflight_ios_signing()
        assert "'Typo Profile' is not installed" in exc.value.message
        assert "Store Profile" in exc.value.message

    def test_profile_resolves_by_name_or_uuid(self, tmp_path, monkeypatch):
        """Xcode accepts either specifier form, so both must pass preflight."""
        stub_installed_profiles(
            monkeypatch, [make_profile(name="Store Profile", uuid="ABCD-1234")]
        )

        for specifier in ("Store Profile", "ABCD-1234"):
            make_command(
                tmp_path,
                template_data={
                    "ios_provisioning_profile": specifier,
                    "ios_team_id": "TEAM123456",
                    "bundle_id": "com.example.app",
                },
            ).preflight_ios_signing()

    def test_expired_profile_rejected(self, tmp_path, monkeypatch):
        """An expired profile fails signing; say so instead of building first."""
        past = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
        stub_installed_profiles(monkeypatch, [make_profile(expires=past)])
        cmd = make_command(
            tmp_path, template_data={"ios_provisioning_profile": "Store Profile"}
        )

        with pytest.raises(Exit, match="expired"):
            cmd.preflight_ios_signing()

    def test_team_mismatch_rejected(self, tmp_path, monkeypatch):
        """Xcode matches the profile within the team, so both must agree."""
        stub_installed_profiles(monkeypatch, [make_profile(team_id="TEAM123456")])
        cmd = make_command(
            tmp_path,
            template_data={
                "ios_provisioning_profile": "Store Profile",
                "ios_team_id": "OTHER99999",
            },
        )

        with pytest.raises(Exit, match="belongs to team TEAM123456"):
            cmd.preflight_ios_signing()

    def test_bundle_id_not_covered_rejected(self, tmp_path, monkeypatch):
        """A profile for another App ID cannot sign this app."""
        stub_installed_profiles(
            monkeypatch, [make_profile(app_id="TEAM123456.com.example.other")]
        )
        cmd = make_command(
            tmp_path,
            template_data={
                "ios_provisioning_profile": "Store Profile",
                "bundle_id": "com.example.app",
            },
        )

        with pytest.raises(Exit, match="does not cover"):
            cmd.preflight_ios_signing()

    def test_wildcard_profile_covers_bundle_id(self, tmp_path, monkeypatch):
        """Wildcard App IDs authorize every bundle id sharing their prefix."""
        stub_installed_profiles(
            monkeypatch, [make_profile(app_id="TEAM123456.com.example.*")]
        )
        make_command(
            tmp_path,
            template_data={
                "ios_provisioning_profile": "Store Profile",
                "bundle_id": "com.example.app",
            },
        ).preflight_ios_signing()

    def test_find_profile_ignores_surrounding_whitespace(self):
        """A stray space in pyproject shouldn't look like a missing profile."""
        assert (
            find_provisioning_profile("  Store Profile  ", [make_profile()]) is not None
        )
