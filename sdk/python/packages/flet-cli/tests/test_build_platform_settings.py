"""Platform-over-global precedence of `[tool.flet]` settings in `flet build`."""

import argparse
import plistlib
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from jinja2 import Environment

from flet_cli.commands.build_base import BaseBuildCommand

ANDROID_NS = "http://schemas.android.com/apk/res/android"


def _command(pyproject=None, platform="android"):
    cmd = BaseBuildCommand.__new__(BaseBuildCommand)
    cmd.config_platform = platform
    values = pyproject or {}
    cmd.get_pyproject = lambda key=None: values.get(key)
    return cmd


def test_platform_value_wins():
    cmd = _command(
        {
            "tool.flet.android.app.exclude": ["tests"],
            "tool.flet.app.exclude": ["docs"],
        }
    )
    assert cmd.get_platform_setting("app.exclude") == ["tests"]


def test_global_value_used_when_platform_unset():
    cmd = _command({"tool.flet.app.exclude": ["docs"]})
    assert cmd.get_platform_setting("app.exclude") == ["docs"]


def test_default_when_neither_set():
    assert _command().get_platform_setting("app.exclude") is None
    assert _command().get_platform_setting("app.exclude", []) == []


@pytest.mark.parametrize("empty", [[], {}, ""])
def test_empty_platform_value_clears_global(empty):
    cmd = _command(
        {
            "tool.flet.android.source_packages": empty,
            "tool.flet.source_packages": ["numpy"],
        }
    )
    assert cmd.get_platform_setting("source_packages", ["default"]) == empty


def test_other_platform_value_ignored():
    cmd = _command(
        {
            "tool.flet.ios.dev_packages": {},
            "tool.flet.dev_packages": {"flet": "../flet"},
        }
    )
    assert cmd.get_platform_setting("dev_packages") == {"flet": "../flet"}


def test_explicit_platform_overrides_the_build_platform():
    """An explicit `platform` reads that platform's table, not the built one's."""
    cmd = _command(
        {
            "tool.flet.android.icon_background": "#003366",
            "tool.flet.icon_background": "#1a1a2e",
        },
        platform="macos",
    )
    assert cmd.get_platform_setting("icon_background", platform="android") == "#003366"
    assert cmd.get_platform_setting("icon_background") == "#1a1a2e"


@pytest.mark.parametrize(
    "key",
    ["color", "dark_color", "icon_background", "icon_dark_background", "icon_fit"],
)
def test_empty_platform_splash_value_clears_global(key):
    """An empty platform splash value replaces the global one."""
    cmd = _command(
        {f"tool.flet.android.splash.{key}": "", f"tool.flet.splash.{key}": "global"}
    )
    assert cmd.splash_setting(key) == ""


def test_empty_platform_splash_colour_falls_back_to_the_default():
    """An empty platform splash colour resolves to the default colour."""
    cmd = _command(
        {"tool.flet.android.splash.color": "", "tool.flet.splash.color": "#000000"}
    )
    cmd.options = SimpleNamespace(
        no_android_splash=None,
        no_ios_splash=None,
        no_web_splash=None,
        splash_color=None,
        splash_dark_color=None,
    )
    assert cmd._resolve_splash()["color"] == "#ffffff"


def test_empty_platform_icon_background_falls_back_to_white():
    """An empty platform icon background resolves to white."""
    cmd = _command(
        {
            "tool.flet.macos.icon_background": "",
            "tool.flet.icon_background": "#1a1a2e",
        },
        platform="macos",
    )
    assert cmd.icon_background_value("macos") == ""
    assert cmd._resolve_icon_background() == (255, 255, 255)


def _template_data(pyproject, tmp_path):
    """Build the template data of an Android build with the real options."""
    parser = argparse.ArgumentParser(add_help=False)
    cmd = BaseBuildCommand(parser)
    cmd.options = parser.parse_args([])
    cmd.python_app_path = tmp_path
    cmd.flutter_dir = tmp_path
    cmd.config_platform = "android"
    cmd.target_platform = "apk"
    cmd.package_platform = "Android"
    cmd.python_release = MagicMock(android_abis=["arm64-v8a"])
    values = {"project.name": "my-app", **pyproject}
    cmd.get_pyproject = lambda key=None: values.get(key) if key else {}
    cmd.setup_template_data()
    return cmd.template_data


@pytest.mark.parametrize(
    ("platform_value", "org_name", "artifact_name", "bundle_id"),
    [
        ("", "com.flet", "my-app", "com.flet.my-app"),
        (None, "com.global", "global", "com.global.id"),
        ("android", "android", "android", "android"),
    ],
)
def test_identity_settings_reach_the_template(
    tmp_path, platform_value, org_name, artifact_name, bundle_id
):
    """`org`, `artifact` and `bundle_id` resolve platform over global over default."""
    data = _template_data(
        {
            "tool.flet.org": "com.global",
            "tool.flet.artifact": "global",
            "tool.flet.bundle_id": "com.global.id",
            "tool.flet.android.org": platform_value,
            "tool.flet.android.artifact": platform_value,
            "tool.flet.android.bundle_id": platform_value,
        },
        tmp_path,
    )
    assert data["org_name"] == org_name
    assert data["artifact_name"] == artifact_name
    assert data["bundle_id"] == bundle_id


@pytest.mark.parametrize(
    ("cli", "pyproject", "expected"),
    [
        (None, {}, True),
        (None, {"tool.flet.compile.app": False}, False),
        (
            None,
            {"tool.flet.android.compile.app": True, "tool.flet.compile.app": False},
            True,
        ),
        (
            None,
            {"tool.flet.android.compile.app": False, "tool.flet.compile.app": True},
            False,
        ),
        (False, {"tool.flet.compile.app": True}, False),
    ],
)
def test_bool_setting_precedence(cli, pyproject, expected):
    cmd = _command(pyproject)
    assert cmd.get_bool_setting(cli, "compile.app", True) is expected


def _deep_linking_command(pyproject, package_platform, scheme=None, host=None):
    cmd = _command(pyproject)
    cmd.package_platform = package_platform
    cmd.options = argparse.Namespace(deep_linking_scheme=scheme, deep_linking_host=host)

    def cleanup(code, message):
        """Capture a failed build setting without exiting the test process."""
        assert code == 1
        raise ValueError(message)

    cmd.cleanup = cleanup
    return cmd


_COMMON_DEEP_LINK = {
    "tool.flet.deep_linking.scheme": "https",
    "tool.flet.deep_linking.host": "app.example.com",
}


@pytest.mark.parametrize("package_platform", ["Android", "iOS", "Darwin", "Emscripten"])
def test_common_deep_linking_is_the_fallback(package_platform):
    cmd = _deep_linking_command(_COMMON_DEEP_LINK, package_platform)
    assert cmd.get_deep_linking() == {"scheme": "https", "host": "app.example.com"}


@pytest.mark.parametrize(
    ("package_platform", "section"), [("Android", "android"), ("iOS", "ios")]
)
def test_platform_deep_linking_overrides_common_per_key(package_platform, section):
    cmd = _deep_linking_command(
        {
            **_COMMON_DEEP_LINK,
            f"tool.flet.{section}.deep_linking.host": "m.example.com",
        },
        package_platform,
    )
    assert cmd.get_deep_linking() == {"scheme": "https", "host": "m.example.com"}


def test_platform_only_deep_linking():
    cmd = _deep_linking_command(
        {
            "tool.flet.ios.deep_linking.scheme": "myapp",
            "tool.flet.ios.deep_linking.host": "open",
        },
        "iOS",
    )
    assert cmd.get_deep_linking() == {"scheme": "myapp", "host": "open"}
    # The iOS table doesn't leak to Android.
    android = _deep_linking_command(
        {"tool.flet.ios.deep_linking.scheme": "myapp"}, "Android"
    )
    assert android.get_deep_linking() == {"scheme": None, "host": None}


class TestDeepLinking:
    """Cover resolving the deep-linking scheme and host and rendering them."""

    TEMPLATE = (
        Path(__file__).resolve().parents[3] / "templates/build/{{cookiecutter.out_dir}}"
    )

    @staticmethod
    def _command(pyproject=None, package_platform="Android", scheme=None, host=None):
        """Create a build command whose configuration errors raise ValueError."""
        return _deep_linking_command(pyproject or {}, package_platform, scheme, host)

    @classmethod
    def _render(cls, path, deep_linking):
        """Render a template file with only the deep-linking options set."""
        return (
            Environment()
            .from_string((cls.TEMPLATE / path).read_text())
            .render(
                cookiecutter={
                    "product_name": "Example",
                    "_pyproject": {},
                    "_options": {
                        "deep_linking": deep_linking,
                        "android_activity": {"intent_filters": []},
                        "android_application_attributes": {},
                        "android_queries": {
                            "packages": [],
                            "intents": [],
                            "providers": [],
                        },
                        "android_receivers": {},
                        "android_services": {},
                        "android_permissions": {},
                        "android_features": {},
                        "android_meta_data": {},
                        "android_providers": {},
                        "info_plist": {},
                    },
                }
            )
        )

    @classmethod
    def _android_filters(cls, deep_linking):
        """Return the main activity's VIEW intent filters as `<data>` attributes."""
        manifest = ET.fromstring(
            cls._render("android/app/src/main/AndroidManifest.xml", deep_linking)
        )
        filters = []
        for intent_filter in manifest.findall("application/activity/intent-filter"):
            action = intent_filter.find("action").get(f"{{{ANDROID_NS}}}name")
            if action == "android.intent.action.VIEW":
                data = intent_filter.find("data")
                filters.append({k.split("}")[1]: v for k, v in data.attrib.items()})
        return manifest, filters

    @classmethod
    def _ios_url_types(cls, deep_linking):
        """Return the rendered `CFBundleURLTypes` of the iOS `Info.plist`."""
        rendered = cls._render("ios/Runner/Info.plist", deep_linking)
        return plistlib.loads(rendered.encode()).get("CFBundleURLTypes")

    @pytest.mark.parametrize(
        "pyproject, cli, expected",
        [
            ({}, {}, {"scheme": None, "host": None}),
            (
                {"tool.flet.deep_linking.scheme": "myapp"},
                {},
                {"scheme": "myapp", "host": None},
            ),
            (
                _COMMON_DEEP_LINK,
                {},
                {"scheme": "https", "host": "app.example.com"},
            ),
            (_COMMON_DEEP_LINK, {"scheme": "myapp"}, {"scheme": "myapp", "host": None}),
            (
                {
                    "tool.flet.deep_linking.scheme": " myapp ",
                    "tool.flet.deep_linking.host": " ",
                },
                {},
                {"scheme": "myapp", "host": None},
            ),
        ],
    )
    def test_scheme_alone_or_with_a_host_resolves(self, pyproject, cli, expected):
        """A scheme alone is enough, and a CLI scheme replaces the project's pair."""
        assert self._command(pyproject, **cli).get_deep_linking() == expected

    @pytest.mark.parametrize(
        "pyproject, cli, message",
        [
            ({}, {"host": "pay"}, "--deep-linking-host needs --deep-linking-scheme"),
            ({"tool.flet.deep_linking.host": "pay"}, {}, "needs a scheme"),
            ({"tool.flet.deep_linking.scheme": "https"}, {}, "needs a host"),
            ({"tool.flet.deep_linking.scheme": "HTTP"}, {}, "needs a host"),
            ({}, {"scheme": "https"}, "needs a host"),
            ({"tool.flet.deep_linking.scheme": 1}, {}, "expected a string"),
        ],
    )
    def test_incomplete_settings_fail_the_build(self, pyproject, cli, message):
        """A host without a scheme and web schemes without a host are rejected."""
        with pytest.raises(ValueError, match=message):
            self._command(pyproject, **cli).get_deep_linking()

    def test_other_platforms_skip_the_mobile_checks(self):
        """Deep links render only on Android and iOS, so other builds don't fail."""
        cmd = self._command({"tool.flet.deep_linking.host": "pay"}, "Emscripten")
        assert cmd.get_deep_linking() == {"scheme": None, "host": "pay"}

    @pytest.mark.parametrize(
        "deep_linking, expected",
        [
            ({"scheme": None, "host": None}, []),
            ({"scheme": "myapp", "host": None}, [{"scheme": "myapp"}]),
            (
                {"scheme": "https", "host": "a&b.example.com"},
                [{"scheme": "https", "host": "a&b.example.com"}],
            ),
        ],
    )
    def test_android_filter_needs_only_a_scheme(self, deep_linking, expected):
        """Render the activity's VIEW filter for a scheme, with a host only if set."""
        manifest, filters = self._android_filters(deep_linking)
        assert filters == expected
        flag = f"{{{ANDROID_NS}}}name"
        assert not [
            m
            for m in manifest.iter("meta-data")
            if m.get(flag) == "flutter_deeplinking_enabled"
        ]

    @pytest.mark.parametrize(
        "deep_linking, expected",
        [
            ({"scheme": None, "host": None}, None),
            (
                {"scheme": "myapp", "host": None},
                [
                    {
                        "CFBundleTypeRole": "Editor",
                        "CFBundleURLName": "$(PRODUCT_BUNDLE_IDENTIFIER)",
                        "CFBundleURLSchemes": ["myapp"],
                    }
                ],
            ),
            (
                {"scheme": "myapp", "host": "pay"},
                [
                    {
                        "CFBundleTypeRole": "Editor",
                        "CFBundleURLName": "pay",
                        "CFBundleURLSchemes": ["myapp"],
                    }
                ],
            ),
        ],
    )
    def test_ios_url_type_needs_only_a_scheme(self, deep_linking, expected):
        """Render `CFBundleURLTypes` for a scheme, named after the host if set."""
        assert self._ios_url_types(deep_linking) == expected
