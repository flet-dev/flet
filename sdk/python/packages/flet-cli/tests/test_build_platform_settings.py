"""Platform-over-global precedence of `[tool.flet]` settings in `flet build`."""

import pytest

from flet_cli.commands.build_base import BaseBuildCommand


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


def _deep_linking_command(pyproject, package_platform):
    cmd = _command(pyproject)
    cmd.package_platform = package_platform
    return cmd


_COMMON_DEEP_LINK = {
    "tool.flet.deep_linking.scheme": "https",
    "tool.flet.deep_linking.host": "app.example.com",
}


@pytest.mark.parametrize("package_platform", ["Android", "iOS", "Darwin", "Emscripten"])
def test_common_deep_linking_is_the_fallback(package_platform):
    cmd = _deep_linking_command(_COMMON_DEEP_LINK, package_platform)
    assert cmd.get_deep_linking_setting("scheme") == "https"
    assert cmd.get_deep_linking_setting("host") == "app.example.com"


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
    assert cmd.get_deep_linking_setting("scheme") == "https"
    assert cmd.get_deep_linking_setting("host") == "m.example.com"


def test_platform_only_deep_linking():
    cmd = _deep_linking_command(
        {
            "tool.flet.ios.deep_linking.scheme": "myapp",
            "tool.flet.ios.deep_linking.host": "open",
        },
        "iOS",
    )
    assert (
        cmd.get_deep_linking_setting("scheme"),
        cmd.get_deep_linking_setting("host"),
    ) == (
        "myapp",
        "open",
    )
    # The iOS table doesn't leak to Android.
    android = _deep_linking_command(
        {"tool.flet.ios.deep_linking.scheme": "myapp"}, "Android"
    )
    assert android.get_deep_linking_setting("scheme") is None
