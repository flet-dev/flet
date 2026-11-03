"""Tests for the settings and templates of `flet build macos`."""

import argparse
import datetime
import plistlib
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

import pytest
from cookiecutter.prompt import prompt_for_config
from jinja2 import Environment, StrictUndefined

from flet_cli.commands.build_base import BaseBuildCommand

MACOS_TEMPLATE_DIR = (
    Path(__file__).resolve().parents[3]
    / "templates/build/{{cookiecutter.out_dir}}/macos"
)
DEFAULT_ENTITLEMENTS = {
    "com.apple.security.app-sandbox": False,
    "com.apple.security.cs.allow-jit": True,
    "com.apple.security.cs.allow-unsigned-executable-memory": True,
    "com.apple.security.network.client": True,
    "com.apple.security.network.server": True,
    "com.apple.security.files.user-selected.read-write": True,
}
PBXPROJ = "Runner.xcodeproj/project.pbxproj"
SCHEME = "Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme"


class Exit(Exception):
    """Captures `cleanup(code, message)` calls, which normally sys.exit."""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"cleanup({code}): {message}")


def _settings_command(settings=None, argv=()):
    """Create a macOS build command with the real `flet build` options parsed from
    `argv`, whose configuration errors raise `Exit`."""
    parser = argparse.ArgumentParser(add_help=False)
    cmd = BaseBuildCommand(parser)
    cmd.options = parser.parse_args(list(argv))
    values = settings or {}
    cmd.get_pyproject = lambda key=None: values.get(key)
    cmd.package_platform = "Darwin"
    cmd.config_platform = "macos"

    def cleanup(code, message=None, **kwargs):
        raise Exit(code, message)

    cmd.cleanup = cleanup
    return cmd


def _render_template(name: str, options: Optional[dict] = None, **values) -> str:
    """Render a macOS template file from a context processed by cookiecutter,
    like a real build; `values` and `options` replace the build's settings."""
    context = prompt_for_config(
        {
            "cookiecutter": {
                "product_name": "Example",
                "artifact_name": "Example",
                "bundle_id": "com.example.app",
                "copyright": "Copyright (c) 2026 Example",
                "flutter": {"dependencies": []},
                **values,
                "_options": {
                    "info_plist": {},
                    "macos_entitlements": {},
                    **(options or {}),
                },
            }
        },
        no_input=True,
    )
    return (
        Environment(undefined=StrictUndefined, keep_trailing_newline=True)
        .from_string((MACOS_TEMPLATE_DIR / name).read_text())
        .render(cookiecutter=context)
    )


class TestInfoPlistSettings:
    def test_no_settings_add_no_entries(self):
        """Without settings, the build adds nothing to `Info.plist`."""
        assert _settings_command().get_info_plist(impeller=True) == {}

    def test_permission_bundle_adds_its_macos_entries(self):
        """A permission bundle adds its macOS entries, not its iOS ones."""
        cmd = _settings_command(argv=["--permissions", "location"])
        assert set(cmd.get_info_plist(impeller=True)) == {"NSLocationUsageDescription"}

    def test_platform_permissions_replace_the_common_ones(self):
        """`[tool.flet.macos].permissions` replaces `[tool.flet].permissions`."""
        cmd = _settings_command(
            {
                "tool.flet.macos.permissions": ["camera"],
                "tool.flet.permissions": ["microphone"],
            }
        )
        assert set(cmd.get_info_plist(impeller=True)) == {"NSCameraUsageDescription"}

    def test_info_table_overrides_permission_bundles(self):
        """`[tool.flet.macos.info]` overrides a bundle's entry and adds its own."""
        cmd = _settings_command(
            {
                "tool.flet.macos.permissions": ["camera"],
                "tool.flet.macos.info": {
                    "NSCameraUsageDescription": "Scan receipts",
                    "LSUIElement": True,
                },
            }
        )
        assert cmd.get_info_plist(impeller=True) == {
            "NSCameraUsageDescription": "Scan receipts",
            "LSUIElement": True,
        }

    def test_ios_table_is_ignored_on_macos(self):
        """macOS builds don't read `[tool.flet.ios.info]`."""
        cmd = _settings_command({"tool.flet.ios.info": {"UIStatusBarHidden": True}})
        assert cmd.get_info_plist(impeller=True) == {}

    def test_cli_entries_override_the_table_and_keep_their_types(self):
        """`--info-plist` entries override the table and get their value types."""
        cmd = _settings_command(
            {"tool.flet.macos.info": {"Name": "table", "Kept": "table"}},
            argv=[
                "--info-plist",
                "Name=cli",
                "Enabled=true",
                "Count=32",
                "Ratio=0.5",
                'Modes=["basic", "advanced"]',
                "Table={ Nested = false }",
            ],
        )
        assert cmd.get_info_plist(impeller=True) == {
            "Name": "cli",
            "Kept": "table",
            "Enabled": True,
            "Count": 32,
            "Ratio": 0.5,
            "Modes": ["basic", "advanced"],
            "Table": {"Nested": False},
        }

    def test_impeller_off_adds_its_key(self):
        """Turning Impeller off is written to `Info.plist`."""
        assert _settings_command().get_info_plist(impeller=False) == {
            "FLTEnableImpeller": False
        }

    @pytest.mark.parametrize(
        ("settings", "argv"),
        [
            ({"tool.flet.macos.info": {"FLTEnableImpeller": True}}, ()),
            ({}, ("--info-plist", "FLTEnableImpeller=true")),
        ],
    )
    def test_explicit_entry_overrides_the_impeller_key(self, settings, argv):
        """An explicit `FLTEnableImpeller` entry wins over the Impeller setting."""
        cmd = _settings_command(settings, argv=argv)
        assert cmd.get_info_plist(impeller=False) == {"FLTEnableImpeller": True}

    def test_malformed_cli_entry_fails(self):
        """An `--info-plist` entry without `=` is rejected."""
        cmd = _settings_command(argv=["--info-plist", "Name"])
        with pytest.raises(Exit, match="Invalid Info.plist option: Name"):
            cmd.get_info_plist(impeller=True)

    def test_unsupported_value_type_fails(self):
        """A value plists cannot hold is rejected with its key."""
        cmd = _settings_command(
            {"tool.flet.macos.info": {"When": datetime.date(2030, 1, 1)}}
        )
        with pytest.raises(Exit, match="Unsupported Info.plist value type for When"):
            cmd.get_info_plist(impeller=True)


class TestEntitlementSettings:
    def test_defaults(self):
        """Without settings, the app gets Flet's default entitlements."""
        assert _settings_command().get_macos_entitlements() == DEFAULT_ENTITLEMENTS

    @pytest.mark.parametrize(
        ("bundle", "added"),
        [
            ("location", {"com.apple.security.personal-information.location": True}),
            ("camera", {"com.apple.security.device.camera": True}),
            ("microphone", {"com.apple.security.device.audio-input": True}),
            (
                "photo_library",
                {"com.apple.security.personal-information.photos-library": True},
            ),
            ("biometric", {}),
        ],
    )
    def test_permission_bundle_adds_its_entitlements(self, bundle, added):
        """A permission bundle adds its entitlements to the defaults."""
        cmd = _settings_command(argv=["--permissions", bundle])
        assert cmd.get_macos_entitlements() == {**DEFAULT_ENTITLEMENTS, **added}

    def test_table_overrides_defaults_and_bundles(self):
        """`[tool.flet.macos.entitlement]` overrides defaults and bundles."""
        cmd = _settings_command(
            {
                "tool.flet.macos.permissions": ["camera"],
                "tool.flet.macos.entitlement": {
                    "com.apple.security.app-sandbox": True,
                    "com.apple.security.device.camera": False,
                },
            }
        )
        assert cmd.get_macos_entitlements() == {
            **DEFAULT_ENTITLEMENTS,
            "com.apple.security.app-sandbox": True,
            "com.apple.security.device.camera": False,
        }

    def test_cli_entries_override_the_table_and_keep_their_types(self):
        """`--macos-entitlements` entries override the table and get their types."""
        cmd = _settings_command(
            {"tool.flet.macos.entitlement": {"com.example.name": "table"}},
            argv=[
                "--macos-entitlements",
                "com.example.name=cli",
                "com.apple.security.app-sandbox=true",
                'com.example.groups=["a", "b"]',
            ],
        )
        assert cmd.get_macos_entitlements() == {
            **DEFAULT_ENTITLEMENTS,
            "com.apple.security.app-sandbox": True,
            "com.example.name": "cli",
            "com.example.groups": ["a", "b"],
        }

    def test_malformed_cli_entry_fails(self):
        """A `--macos-entitlements` entry without `=` is rejected."""
        cmd = _settings_command(argv=["--macos-entitlements", "com.example.name"])
        with pytest.raises(Exit, match="Invalid macOS entitlement option"):
            cmd.get_macos_entitlements()

    def test_unsupported_value_type_fails(self):
        """A value plists cannot hold is rejected with its key."""
        cmd = _settings_command(
            {"tool.flet.macos.entitlement": {"com.example.when": datetime.date.today()}}
        )
        with pytest.raises(Exit, match="value type for com.example.when"):
            cmd.get_macos_entitlements()


class TestInfoPlistTemplate:
    def test_product_name_is_written_escaped(self):
        """The product name is the display name, escaped; the bundle name comes
        from the build setting that follows the artifact name."""
        plist = plistlib.loads(
            _render_template("Runner/Info.plist", product_name="Tom & <Jerry>").encode()
        )
        assert plist["CFBundleDisplayName"] == "Tom & <Jerry>"
        assert plist["CFBundleName"] == "$(PRODUCT_NAME)"
        assert plist["NSHumanReadableCopyright"] == "$(PRODUCT_COPYRIGHT)"

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


@pytest.mark.parametrize(
    "name", ["Runner/Release.entitlements", "Runner/DebugProfile.entitlements"]
)
class TestEntitlementsTemplates:
    def test_file_holds_the_default_entitlements(self, name):
        """Both entitlements files hold what the settings resolve to."""
        entitlements = _settings_command().get_macos_entitlements()
        rendered = _render_template(name, options={"macos_entitlements": entitlements})
        assert plistlib.loads(rendered.encode()) == DEFAULT_ENTITLEMENTS

    def test_entries_keep_their_types_and_are_escaped(self, name):
        """Every plist value type survives the build, and keys and text are
        escaped and never rendered as Jinja."""
        entitlements = {
            "com.example.text": "Tom & Jerry <{{ x }}>",
            "com.example&key": "key",
            "com.example.enabled": True,
            "com.example.count": 32,
            "com.example.ratio": 0.5,
            "com.example.table": {"nested": ["a", 1, False, {"deep": "b"}]},
        }
        rendered = _render_template(name, options={"macos_entitlements": entitlements})
        assert plistlib.loads(rendered.encode()) == entitlements


class TestAppInfoConfig:
    def test_names_and_copyright(self):
        """The artifact name, bundle ID and copyright reach the build settings."""
        rendered = _render_template(
            "Runner/Configs/AppInfo.xcconfig",
            artifact_name="Tom & Jerry",
            bundle_id="com.acme.app",
            copyright="Copyright (c) 2026 Acme",
        )
        lines = rendered.splitlines()
        assert "PRODUCT_NAME = Tom & Jerry" in lines
        assert "PRODUCT_BUNDLE_IDENTIFIER = com.acme.app" in lines
        assert (
            "PRODUCT_COPYRIGHT = Copyright (c) 2026 Acme. All rights reserved." in lines
        )


class TestProjectTemplate:
    def test_artifact_name_names_the_app(self):
        """The app's file reference and the test host follow the artifact name."""
        rendered = _render_template(PBXPROJ, artifact_name="Acme App")
        assert 'path = "Acme App.app";' in rendered
        assert rendered.count('"$(BUILT_PRODUCTS_DIR)/Acme App.app/') == 3

    def test_test_target_gets_its_own_bundle_id(self):
        """The test target's bundle ID derives from the app's in every configuration."""
        rendered = _render_template(PBXPROJ, bundle_id="com.acme.app")
        assert (
            rendered.count("PRODUCT_BUNDLE_IDENTIFIER = com.acme.app.RunnerTests;") == 3
        )

    @pytest.mark.parametrize(
        ("dependencies", "expected"), [([], 0), (["flet_rive"], 3)]
    )
    def test_rive_setup_phase_only_with_flet_rive(self, dependencies, expected):
        """The Rive setup build phase is only added for apps using `flet_rive`."""
        rendered = _render_template(PBXPROJ, flutter={"dependencies": dependencies})
        assert rendered.count("Rive Native Setup") == expected


class TestScheme:
    def test_scheme_is_valid_for_any_artifact_name(self):
        """The scheme doesn't hold the artifact name: Flutter's Swift Package Manager
        migration copies its `BuildableName` back unescaped, so a `&` in that name
        would make the scheme unreadable and fail the build."""
        rendered = _render_template(SCHEME, artifact_name="Tom & Jerry")
        names = {
            reference.get("BuildableName")
            for reference in ET.fromstring(rendered).iter("BuildableReference")
        }
        assert names == {"Runner.app", "RunnerTests.xctest"}
