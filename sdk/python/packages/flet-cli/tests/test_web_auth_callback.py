"""WebAuth callback scheme resolution and Android patching."""

from __future__ import annotations

from pathlib import Path

from flet_cli.utils.web_auth_callback import (
    default_callback_scheme_from_bundle_id,
    patch_android_web_auth_scheme,
    resolve_web_auth_callback_scheme,
    resolve_web_auth_callback_scheme_info,
)


def test_cli_scheme_wins():
    scheme = resolve_web_auth_callback_scheme(
        cli_scheme="Com.Example.Auth",
        get_pyproject=lambda key: None,
    )
    assert scheme == "com.example.auth"


def test_pyproject_web_auth_key():
    values = {"tool.flet.web_auth.callback_scheme": "Com.Example.MyApp.Auth"}
    scheme = resolve_web_auth_callback_scheme(
        cli_scheme=None,
        get_pyproject=lambda key: values.get(key),
    )
    assert scheme == "com.example.myapp.auth"


def test_default_from_bundle_id():
    values = {"tool.flet.bundle_id": "com.example.myapp"}
    resolved = default_callback_scheme_from_bundle_id(lambda key: values.get(key))
    assert resolved.scheme == "com.example.myapp.auth"
    assert "bundle id" in resolved.source


def test_platform_specific_overrides_shared():
    values = {
        "tool.flet.android.web_auth.callback_scheme": "android-scheme",
        "tool.flet.web_auth.callback_scheme": "shared-scheme",
    }
    assert (
        resolve_web_auth_callback_scheme(
            cli_scheme=None,
            get_pyproject=lambda key: values.get(key),
            config_platform="android",
        )
        == "android-scheme"
    )


def test_patch_android_inserts_placeholder(tmp_path: Path):
    gradle = tmp_path / "android" / "app" / "build.gradle"
    gradle.parent.mkdir(parents=True)
    gradle.write_text(
        "android {\n    defaultConfig {\n        applicationId 'com.example'\n    }\n}\n",
        encoding="utf-8",
    )
    assert patch_android_web_auth_scheme(tmp_path, "com.example.auth")
    text = gradle.read_text(encoding="utf-8")
    assert "webAuthCallbackScheme" in text
    assert "com.example.auth" in text
