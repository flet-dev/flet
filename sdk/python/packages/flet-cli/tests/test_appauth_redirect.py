from pathlib import Path

from flet_cli.utils.appauth_redirect import (
    patch_android_appauth_scheme,
    patch_ios_appauth_scheme,
    resolve_appauth_redirect_scheme,
)


def test_resolve_prefers_cli_scheme():
    scheme = resolve_appauth_redirect_scheme(
        cli_scheme="MyApp",
        get_pyproject=lambda key: "fromtoml",
        config_platform="ios",
    )
    assert scheme == "myapp"


def test_resolve_from_pyproject():
    values = {"tool.flet.appauth.redirect_scheme": "Com.Example"}
    scheme = resolve_appauth_redirect_scheme(
        cli_scheme=None,
        get_pyproject=lambda key: values.get(key),
    )
    assert scheme == "com.example"


def test_resolve_platform_specific_prefers_build_platform():
    values = {
        "tool.flet.android.appauth.redirect_scheme": "android-scheme",
        "tool.flet.ios.appauth.redirect_scheme": "ios-scheme",
        "tool.flet.appauth.redirect_scheme": "shared-scheme",
    }
    assert (
        resolve_appauth_redirect_scheme(
            cli_scheme=None,
            get_pyproject=lambda key: values.get(key),
            config_platform="ios",
        )
        == "ios-scheme"
    )
    assert (
        resolve_appauth_redirect_scheme(
            cli_scheme=None,
            get_pyproject=lambda key: values.get(key),
            config_platform="android",
        )
        == "android-scheme"
    )


def test_resolve_falls_back_to_shared_when_platform_unset():
    values = {
        "tool.flet.android.appauth.redirect_scheme": "android-scheme",
        "tool.flet.appauth.redirect_scheme": "shared-scheme",
    }
    assert (
        resolve_appauth_redirect_scheme(
            cli_scheme=None,
            get_pyproject=lambda key: values.get(key),
            config_platform="ios",
        )
        == "shared-scheme"
    )


def test_resolve_missing():
    assert (
        resolve_appauth_redirect_scheme(cli_scheme=None, get_pyproject=lambda key: None)
        is None
    )


def test_patch_android_gradle(tmp_path: Path):
    android_app = tmp_path / "android" / "app"
    android_app.mkdir(parents=True)
    gradle = android_app / "build.gradle"
    gradle.write_text(
        "android {\n    defaultConfig {\n        applicationId 'x'\n    }\n}\n",
        encoding="utf-8",
    )
    assert patch_android_appauth_scheme(tmp_path, "myapp") is True
    text = gradle.read_text(encoding="utf-8")
    assert "appAuthRedirectScheme" in text
    assert "myapp" in text


def test_patch_android_gradle_updates_existing(tmp_path: Path):
    android_app = tmp_path / "android" / "app"
    android_app.mkdir(parents=True)
    gradle = android_app / "build.gradle"
    gradle.write_text(
        "android {\n    defaultConfig {\n"
        "        manifestPlaceholders += [appAuthRedirectScheme: 'old']\n"
        "    }\n}\n",
        encoding="utf-8",
    )
    assert patch_android_appauth_scheme(tmp_path, "newscheme") is True
    text = gradle.read_text(encoding="utf-8")
    assert 'appAuthRedirectScheme: "newscheme"' in text
    assert "appAuthRedirectScheme: 'old'" not in text


def test_patch_android_missing_gradle_returns_false(tmp_path: Path):
    assert patch_android_appauth_scheme(tmp_path, "myapp") is False


def test_patch_ios_plist(tmp_path: Path):
    import plistlib

    runner = tmp_path / "ios" / "Runner"
    runner.mkdir(parents=True)
    plist_path = runner / "Info.plist"
    with plist_path.open("wb") as f:
        plistlib.dump({"CFBundleName": "Runner"}, f)

    assert patch_ios_appauth_scheme(tmp_path, "myapp") is True
    with plist_path.open("rb") as f:
        data = plistlib.load(f)
    schemes = data["CFBundleURLTypes"][0]["CFBundleURLSchemes"]
    assert schemes == ["myapp"]


def test_patch_ios_already_present_returns_true(tmp_path: Path):
    import plistlib

    runner = tmp_path / "ios" / "Runner"
    runner.mkdir(parents=True)
    plist_path = runner / "Info.plist"
    with plist_path.open("wb") as f:
        plistlib.dump(
            {
                "CFBundleURLTypes": [
                    {"CFBundleURLSchemes": ["myapp"]},
                ]
            },
            f,
        )

    assert patch_ios_appauth_scheme(tmp_path, "myapp") is True
