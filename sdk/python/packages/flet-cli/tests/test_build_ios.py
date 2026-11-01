"""Tests for `flet build ipa`."""

import argparse
import datetime
import plistlib
import re
from pathlib import Path
from typing import Optional

import pytest
from jinja2 import Environment, StrictUndefined

from flet_cli.commands import build as build_module
from flet_cli.commands.build import Command
from flet_cli.commands.build_base import BaseBuildCommand
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


IOS_TEMPLATE_DIR = (
    Path(__file__).resolve().parents[3] / "templates/build/{{cookiecutter.out_dir}}/ios"
)


def _entitlements_command(pyproject: Optional[dict], cli: Optional[list] = None):
    """Create a build command reading `[tool.flet.ios.entitlement]` and CLI entries."""
    cmd = Command(argparse.ArgumentParser())
    cmd.get_pyproject = lambda key: (
        pyproject if key == "tool.flet.ios.entitlement" else None
    )
    cmd.options = argparse.Namespace(ios_entitlements=cli or [])

    def cleanup(code, message=None, **kwargs):
        raise Exit(code, message)

    cmd.cleanup = cleanup
    return cmd


def _render_ios(name: str, entitlements: dict) -> str:
    """Render an iOS template file with the given entitlements."""
    path = IOS_TEMPLATE_DIR / name
    return (
        Environment(keep_trailing_newline=True)
        .from_string(path.read_text())
        .render(cookiecutter={"_options": {"ios_entitlements": entitlements}})
    )


class TestEntitlements:
    def test_absent_settings_resolve_to_no_entitlements(self):
        """Without settings, the app declares no entitlements."""
        assert _entitlements_command(None).get_ios_entitlements() == {}

    def test_cli_entries_override_pyproject_and_keep_their_types(self):
        """CLI entries override pyproject ones and keep their plist value types."""
        cmd = _entitlements_command(
            {
                "aps-environment": "development",
                "com.apple.developer.usernotifications.critical-alerts": True,
            },
            cli=[
                "aps-environment=production",
                "com.apple.developer.associated-domains=['applinks:example.com']",
            ],
        )
        assert cmd.get_ios_entitlements() == {
            "aps-environment": "production",
            "com.apple.developer.usernotifications.critical-alerts": True,
            "com.apple.developer.associated-domains": ["applinks:example.com"],
        }

    def test_malformed_cli_entry_fails(self):
        """A CLI entry without `=` is rejected."""
        with pytest.raises(Exit, match="Invalid iOS entitlement option"):
            _entitlements_command(None, cli=["aps-environment"]).get_ios_entitlements()

    def test_unsupported_value_type_fails(self):
        """A value plists cannot hold is rejected with its key."""
        cmd = _entitlements_command({"com.example.when": datetime.date(2030, 1, 1)})
        with pytest.raises(Exit, match="com.example.when"):
            cmd.get_ios_entitlements()

    def test_entitlements_file_holds_the_resolved_values(self):
        """The rendered entitlements file is a plist of the resolved entries."""
        entitlements = {
            "aps-environment": "development",
            "com.apple.developer.usernotifications.critical-alerts": True,
            "com.apple.developer.associated-domains": ["applinks:example.com"],
        }
        rendered = _render_ios("Runner/Runner.entitlements", entitlements)
        assert plistlib.loads(rendered.encode()) == entitlements

    def test_entitlements_keep_their_types_through_cookiecutter(self):
        """Numbers keep their plist types and strings are escaped after cookiecutter
        processes the build's context."""
        from cookiecutter.prompt import prompt_for_config

        entitlements = {
            "com.example.count": 32,
            "com.example.ratio": 0.5,
            "com.example.name": "Tom & Jerry <{{ x }}>",
            "com.example.enabled": True,
        }
        context = prompt_for_config(
            {"cookiecutter": {"_options": {"ios_entitlements": entitlements}}},
            no_input=True,
        )
        rendered = (
            Environment(keep_trailing_newline=True)
            .from_string((IOS_TEMPLATE_DIR / "Runner/Runner.entitlements").read_text())
            .render(cookiecutter=context)
        )
        assert plistlib.loads(rendered.encode()) == entitlements

    @pytest.mark.parametrize(
        ("entitlements", "expected"),
        [({}, 0), ({"aps-environment": "development"}, 3)],
    )
    def test_project_signs_with_entitlements_only_when_declared(
        self, entitlements, expected
    ):
        """Every app build configuration uses the file, but only if it has entries."""
        rendered = _render_ios("Runner.xcodeproj/project.pbxproj", entitlements)
        assert (
            rendered.count("CODE_SIGN_ENTITLEMENTS = Runner/Runner.entitlements;")
            == expected
        )


def _settings_command(settings=None, argv=(), package_platform="iOS"):
    """Create a build command with the real `flet build` options parsed from
    `argv`, whose configuration errors raise `Exit`."""
    parser = argparse.ArgumentParser(add_help=False)
    cmd = BaseBuildCommand(parser)
    cmd.options = parser.parse_args(list(argv))
    values = settings or {}
    cmd.get_pyproject = lambda key=None: values.get(key)
    cmd.package_platform = package_platform
    cmd.config_platform = {"iOS": "ios", "Darwin": "macos"}[package_platform]

    def cleanup(code, message=None, **kwargs):
        raise Exit(code, message)

    cmd.cleanup = cleanup
    return cmd


def _render_template(name: str, options: Optional[dict] = None, **values) -> str:
    """Render an iOS template file from a context processed by cookiecutter,
    like a real build; `values` and `options` replace the build's settings."""
    from cookiecutter.prompt import prompt_for_config

    context = prompt_for_config(
        {
            "cookiecutter": {
                "project_name": "example",
                "product_name": "Example",
                "artifact_name": "Example",
                "bundle_id": "com.example.app",
                "ios_export_method": "debugging",
                "ios_provisioning_profile": None,
                "ios_signing_certificate": None,
                "ios_team_id": None,
                **values,
                "_options": {
                    "deep_linking": {"scheme": None, "host": None},
                    "info_plist": {},
                    "ios_entitlements": {},
                    "ios_export_options": {},
                    **(options or {}),
                },
            }
        },
        no_input=True,
    )
    return (
        Environment(undefined=StrictUndefined, keep_trailing_newline=True)
        .from_string((IOS_TEMPLATE_DIR / name).read_text())
        .render(cookiecutter=context)
    )


class TestInfoPlistSettings:
    def test_no_settings_add_no_entries(self):
        """Without settings, the build adds nothing to `Info.plist`."""
        assert _settings_command().get_info_plist(impeller=True) == {}

    def test_permission_bundle_adds_its_ios_entries(self):
        """A permission bundle adds its iOS entries, not its macOS ones."""
        cmd = _settings_command(argv=["--permissions", "location"])
        assert set(cmd.get_info_plist(impeller=True)) == {
            "NSLocationWhenInUseUsageDescription",
            "NSLocationAlwaysAndWhenInUseUsageDescription",
        }

    def test_unknown_permission_bundle_adds_nothing(self):
        """A name that isn't a permission bundle adds no entries."""
        cmd = _settings_command({"tool.flet.permissions": ["unknown"]})
        assert cmd.get_info_plist(impeller=True) == {}

    def test_platform_permissions_replace_the_common_ones(self):
        """`[tool.flet.ios].permissions` replaces `[tool.flet].permissions`."""
        cmd = _settings_command(
            {
                "tool.flet.ios.permissions": ["camera"],
                "tool.flet.permissions": ["microphone"],
            }
        )
        assert set(cmd.get_info_plist(impeller=True)) == {"NSCameraUsageDescription"}

    def test_info_table_overrides_permission_bundles(self):
        """`[tool.flet.ios.info]` overrides a bundle's entry and adds its own."""
        cmd = _settings_command(
            {
                "tool.flet.ios.permissions": ["camera"],
                "tool.flet.ios.info": {
                    "NSCameraUsageDescription": "Scan receipts",
                    "UIStatusBarHidden": True,
                },
            }
        )
        assert cmd.get_info_plist(impeller=True) == {
            "NSCameraUsageDescription": "Scan receipts",
            "UIStatusBarHidden": True,
        }

    def test_macos_table_is_ignored_on_ios(self):
        """iOS builds don't read `[tool.flet.macos.info]`."""
        cmd = _settings_command({"tool.flet.macos.info": {"LSUIElement": True}})
        assert cmd.get_info_plist(impeller=True) == {}

    def test_cli_entries_override_the_table_and_keep_their_types(self):
        """`--info-plist` entries override the table and get their value types."""
        cmd = _settings_command(
            {"tool.flet.ios.info": {"Name": "table", "Kept": "table"}},
            argv=[
                "--info-plist",
                "Name=cli",
                "Enabled=true",
                "Count=3",
                "Ratio=0.5",
                'Names=["a", "b"]',
            ],
        )
        assert cmd.get_info_plist(impeller=True) == {
            "Name": "cli",
            "Kept": "table",
            "Enabled": True,
            "Count": 3,
            "Ratio": 0.5,
            "Names": ["a", "b"],
        }

    def test_malformed_cli_entry_fails(self):
        """An `--info-plist` entry without `=` is rejected."""
        cmd = _settings_command(argv=["--info-plist", "Name"])
        with pytest.raises(Exit, match="Invalid Info.plist option: Name"):
            cmd.get_info_plist(impeller=True)

    def test_unsupported_value_type_fails(self):
        """A value plists cannot hold is rejected with its key."""
        cmd = _settings_command(
            {"tool.flet.ios.info": {"When": datetime.date(2030, 1, 1)}}
        )
        with pytest.raises(Exit, match="Unsupported Info.plist value type for When"):
            cmd.get_info_plist(impeller=True)

    @pytest.mark.parametrize(
        ("package_platform", "expected"),
        [("iOS", {}), ("Darwin", {"FLTEnableImpeller": False})],
    )
    def test_impeller_off_only_adds_a_key_on_macos(self, package_platform, expected):
        """Turning Impeller off adds a key on macOS; iOS has no such switch."""
        cmd = _settings_command(package_platform=package_platform)
        assert cmd.get_info_plist(impeller=False) == expected


class TestInfoPlistTemplate:
    def test_names_are_written_escaped(self):
        """The product and project names are escaped in `Info.plist`."""
        plist = plistlib.loads(
            _render_template(
                "Runner/Info.plist",
                product_name="Tom & Jerry",
                project_name="tom<jerry>",
            ).encode()
        )
        assert plist["CFBundleDisplayName"] == "Tom & Jerry"
        assert plist["CFBundleName"] == "tom<jerry>"

    def test_entries_keep_their_types_and_are_escaped(self):
        """Every plist value type survives the build, and keys and text are
        escaped and never rendered as Jinja."""
        entries = {
            "Text": "Tom & Jerry <{{ x }}>",
            "Tom&Jerry": "key",
            "Enabled": True,
            "Disabled": False,
            "Count": 3,
            "Ratio": 0.5,
            "Table": {"Nested": ["a", 1, 0.5, True, {"Deep": "b"}]},
        }
        plist = plistlib.loads(
            _render_template(
                "Runner/Info.plist", options={"info_plist": entries}
            ).encode()
        )
        assert {key: plist[key] for key in entries} == entries


def _podfile_macros(info_plist: dict) -> list:
    """Return the permission macros the rendered `Podfile` enables."""
    rendered = _render_template("Podfile", options={"info_plist": info_plist})
    return re.findall(r"'(PERMISSION_\w+)=1'", rendered)


class TestPodfile:
    def test_no_entries_enable_no_macros(self):
        """Without usage descriptions, the app enables no permission."""
        assert _podfile_macros({}) == []

    @pytest.mark.parametrize(
        ("key", "macros"),
        [
            ("NSCalendarsUsageDescription", ["PERMISSION_EVENTS"]),
            ("NSCalendarWriteOnlyAccessUsageDescription", ["PERMISSION_EVENTS"]),
            (
                "NSCalendarsFullAccessUsageDescription",
                ["PERMISSION_EVENTS_FULL_ACCESS"],
            ),
            ("NSRemindersFullAccessUsageDescription", ["PERMISSION_REMINDERS"]),
            ("NSContactsUsageDescription", ["PERMISSION_CONTACTS"]),
            ("NSCameraUsageDescription", ["PERMISSION_CAMERA"]),
            ("NSMicrophoneUsageDescription", ["PERMISSION_MICROPHONE"]),
            ("NSSpeechRecognitionUsageDescription", ["PERMISSION_SPEECH_RECOGNIZER"]),
            ("NSPhotoLibraryUsageDescription", ["PERMISSION_PHOTOS"]),
            ("NSPhotoLibraryAddUsageDescription", ["PERMISSION_PHOTOS_ADD_ONLY"]),
            ("NSLocationUsageDescription", ["PERMISSION_LOCATION"]),
            ("NSLocationAlwaysAndWhenInUseUsageDescription", ["PERMISSION_LOCATION"]),
            (
                "NSLocationWhenInUseUsageDescription",
                ["PERMISSION_LOCATION", "PERMISSION_LOCATION_WHENINUSE"],
            ),
            ("NSAppleMusicUsageDescription", ["PERMISSION_MEDIA_LIBRARY"]),
            ("NSMotionUsageDescription", ["PERMISSION_SENSORS"]),
            ("NSBluetoothAlwaysUsageDescription", ["PERMISSION_BLUETOOTH"]),
            ("NSBluetoothPeripheralUsageDescription", ["PERMISSION_BLUETOOTH"]),
            (
                "NSUserTrackingUsageDescription",
                ["PERMISSION_APP_TRACKING_TRANSPARENCY"],
            ),
            ("UNAuthorizationOptionCriticalAlert", ["PERMISSION_CRITICAL_ALERTS"]),
            ("NSSiriUsageDescription", ["PERMISSION_ASSISTANT"]),
        ],
    )
    def test_usage_description_enables_its_macros(self, key, macros):
        """Declaring a usage description compiles in its permission's handler,
        without which requesting that permission fails at runtime."""
        assert _podfile_macros({key: "Why"}) == macros

    @pytest.mark.parametrize(
        ("bundle", "macros"),
        [
            ("location", ["PERMISSION_LOCATION", "PERMISSION_LOCATION_WHENINUSE"]),
            ("camera", ["PERMISSION_CAMERA"]),
            ("microphone", ["PERMISSION_MICROPHONE"]),
            ("photo_library", ["PERMISSION_PHOTOS"]),
            ("biometric", []),
        ],
    )
    def test_permission_bundle_enables_its_macros(self, bundle, macros):
        """A permission bundle's entries enable the macros that bundle needs."""
        cmd = _settings_command({"tool.flet.permissions": [bundle]})
        assert _podfile_macros(cmd.get_info_plist(impeller=True)) == macros


class TestSigningSettings:
    def test_defaults(self):
        """Without settings, the app exports for debugging and isn't signed."""
        assert _settings_command().get_ios_signing() == {
            "export_method": "debugging",
            "provisioning_profile": None,
            "signing_certificate": None,
            "team_id": None,
            "export_options": {},
        }

    def test_export_method_cli_overrides_pyproject(self):
        """`--ios-export-method` overrides `[tool.flet.ios].export_method`."""
        cmd = _settings_command(
            {"tool.flet.ios.export_method": "enterprise"},
            argv=["--ios-export-method", "app-store-connect"],
        )
        assert cmd.get_ios_signing()["export_method"] == "app-store-connect"

    def test_export_method_from_pyproject(self):
        """`[tool.flet.ios].export_method` overrides the default."""
        cmd = _settings_command({"tool.flet.ios.export_method": "enterprise"})
        assert cmd.get_ios_signing()["export_method"] == "enterprise"

    @pytest.mark.parametrize(
        ("setting", "flag"),
        [
            ("provisioning_profile", "--ios-provisioning-profile"),
            ("signing_certificate", "--ios-signing-certificate"),
            ("team_id", "--ios-team-id"),
        ],
    )
    def test_resolution_order(self, setting, flag):
        """Each setting comes from the CLI, then the export method's table, then
        `[tool.flet.ios]`."""
        common = {f"tool.flet.ios.{setting}": "common"}
        method = {
            "tool.flet.ios.export_methods": {"debugging": {setting: "method"}},
        }
        assert _settings_command(common).get_ios_signing()[setting] == "common"
        assert (
            _settings_command({**common, **method}).get_ios_signing()[setting]
            == "method"
        )
        assert (
            _settings_command(
                {**common, **method}, argv=[flag, "cli"]
            ).get_ios_signing()[setting]
            == "cli"
        )

    def test_tables_of_other_export_methods_are_ignored(self):
        """Only the table of the selected export method applies."""
        cmd = _settings_command(
            {
                "tool.flet.ios.export_method": "enterprise",
                "tool.flet.ios.export_methods": {"debugging": {"team_id": "OTHER"}},
            }
        )
        assert cmd.get_ios_signing()["team_id"] is None

    def test_export_method_options_replace_the_common_ones(self):
        """The export method's options replace `[tool.flet.ios].export_options`."""
        cmd = _settings_command(
            {
                "tool.flet.ios.export_options": {"uploadSymbols": False, "a": "b"},
                "tool.flet.ios.export_methods": {
                    "debugging": {"export_options": {"uploadSymbols": True}}
                },
            }
        )
        assert cmd.get_ios_signing()["export_options"] == {"uploadSymbols": True}

    def test_export_options_must_be_a_table(self):
        """Export options that aren't a table are rejected."""
        cmd = _settings_command({"tool.flet.ios.export_options": "thinning"})
        with pytest.raises(Exit, match="Invalid iOS export options"):
            cmd.get_ios_signing()

    def test_unsupported_export_option_value_fails(self):
        """A value plists cannot hold is rejected with its key."""
        cmd = _settings_command(
            {"tool.flet.ios.export_options": {"when": datetime.date(2030, 1, 1)}}
        )
        with pytest.raises(Exit, match="value type for when"):
            cmd.get_ios_signing()


class TestProjectTemplate:
    @pytest.mark.parametrize(
        ("value", "line"),
        [
            ({"ios_team_id": "TEAM123456"}, 'DEVELOPMENT_TEAM = "TEAM123456";'),
            (
                {"ios_signing_certificate": "Apple Distribution"},
                'CODE_SIGN_IDENTITY = "Apple Distribution";',
            ),
            (
                {"ios_provisioning_profile": "Store Profile"},
                'PROVISIONING_PROFILE_SPECIFIER = "Store Profile";',
            ),
        ],
    )
    def test_signing_settings_apply_to_every_app_configuration(self, value, line):
        """A signing setting is written to the app's three build configurations,
        and is left out when it isn't set."""
        pbxproj = "Runner.xcodeproj/project.pbxproj"
        assert _render_template(pbxproj, **value).count(line) == 3
        assert line.split('"')[0] not in _render_template(pbxproj)

    def test_bundle_id_and_product_name(self):
        """The bundle ID and artifact name reach every app configuration, and the
        test target gets a bundle ID of its own."""
        rendered = _render_template(
            "Runner.xcodeproj/project.pbxproj",
            bundle_id="com.acme.app",
            artifact_name="Acme App",
        )
        assert rendered.count("PRODUCT_BUNDLE_IDENTIFIER = com.acme.app;") == 3
        assert (
            rendered.count("PRODUCT_BUNDLE_IDENTIFIER = com.acme.app.RunnerTests;") == 3
        )
        assert rendered.count('PRODUCT_NAME = "Acme App";') == 3


class TestExportOptionsTemplate:
    @staticmethod
    def _render(options=None, **values):
        """Return the parsed `exportOptions.plist`."""
        return plistlib.loads(
            _render_template(
                "exportOptions.plist",
                options={"ios_export_options": options or {}},
                **values,
            ).encode()
        )

    def test_signing_settings(self):
        """The method, profile, team and certificate are written, with the profile
        under the app's bundle ID."""
        assert self._render(
            ios_export_method="app-store-connect",
            ios_provisioning_profile="Store Profile",
            ios_team_id="TEAM123456",
            ios_signing_certificate="Apple Distribution",
        ) == {
            "method": "app-store-connect",
            "provisioningProfiles": {"com.example.app": "Store Profile"},
            "teamID": "TEAM123456",
            "signingCertificate": "Apple Distribution",
        }

    def test_unset_team_and_certificate_are_left_out(self):
        """Without a team or certificate, their keys are left out."""
        assert set(self._render(ios_provisioning_profile="Store Profile")) == {
            "method",
            "provisioningProfiles",
        }

    def test_signing_settings_are_escaped(self):
        """A profile name with XML characters still makes a valid plist."""
        plist = self._render(ios_provisioning_profile="R&D <Store>")
        assert plist["provisioningProfiles"]["com.example.app"] == "R&D <Store>"

    def test_documented_example(self):
        """The example of the publishing docs makes a valid plist."""
        options = {
            "uploadSymbols": False,
            "compileBitcode": False,
            "thinning": "<none>",
            "manifest": {
                "appURL": "https://example.com/app.ipa",
                "displayImageURL": "https://example.com/icon57.png",
                "fullSizeImageURL": "https://example.com/icon512.png",
            },
        }
        plist = self._render(options, ios_provisioning_profile="Store Profile")
        assert {key: plist[key] for key in options} == options

    def test_values_keep_their_types_and_are_escaped(self):
        """Every plist value type survives the build, and keys and text are
        escaped and never rendered as Jinja."""
        options = {
            "text": "Tom & Jerry <{{ x }}>",
            "tom&jerry": "key",
            "count": 3,
            "ratio": 0.5,
            "enabled": True,
            "table": {"nested": ["a", 1, 0.5, False, {"deep": "b"}]},
        }
        plist = self._render(options, ios_provisioning_profile="Store Profile")
        assert {key: plist[key] for key in options} == options
