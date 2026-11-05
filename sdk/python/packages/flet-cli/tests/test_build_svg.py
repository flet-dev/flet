"""SVG sources through the build's real icon and splash generators."""

import os
import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image

from flet_cli.commands.build_base import ICON_PLATFORMS, BaseBuildCommand

BUILD_TEMPLATE = (
    Path(__file__).resolve().parents[3]
    / "templates"
    / "build"
    / "{{cookiecutter.out_dir}}"
)


def _svg(color="red"):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        f'<circle cx="12" cy="12" r="12" fill="{color}"/></svg>'
    )


def _command(tmp_path, target="web"):
    assets = tmp_path / "app" / "assets"
    assets.mkdir(parents=True)
    (assets / "icon.svg").write_text(_svg())
    flutter_dir = tmp_path / "flutter"
    shutil.copytree(BUILD_TEMPLATE, flutter_dir)

    cmd = BaseBuildCommand.__new__(BaseBuildCommand)
    cmd.package_app_path = assets.parent
    cmd.flutter_dir = flutter_dir
    cmd.build_dir = tmp_path / "build"
    cmd.target_platform = target
    cmd.config_platform = ICON_PLATFORMS[target]
    cmd.options = SimpleNamespace()
    cmd.template_data = {
        "bundle_id": "com.example.test_app",
        "splash": {
            "web": True,
            "android": True,
            "ios": True,
            "color": "#ffffff",
            "dark_color": "#121212",
        },
    }
    cmd.template_digest = "test-template"
    cmd.get_pyproject = lambda *_: None
    cmd.update_status = lambda *_: None
    cmd.verbose = 0
    cmd.emojis = {"checkmark": ""}

    def fail(code, message):
        raise SystemExit(message)

    cmd.cleanup = fail
    return cmd, assets


def _centre(path):
    with Image.open(path) as image:
        return image.convert("RGBA").getpixel((image.width // 2, image.height // 2))


@pytest.mark.parametrize(
    ("target", "output"),
    [
        ("web", "web/icons/Icon-512.png"),
        ("windows", "windows/runner/resources/app_icon.ico"),
        ("linux", "linux/app_icon.png"),
        ("macos", "macos/Runner/Assets.xcassets/AppIcon.appiconset/app_icon_1024.png"),
        (
            "ipa",
            "ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-1024x1024@1x.png",
        ),
        ("apk", "android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png"),
    ],
)
def test_svg_generates_platform_icons_without_a_raster_sibling(
    tmp_path, target, output
):
    cmd, assets = _command(tmp_path, target)
    cmd.customize_icons()
    assert _centre(cmd.flutter_dir / output)[:3] == (255, 0, 0)
    assert sorted(p.name for p in assets.iterdir()) == ["icon.svg"]


def test_platform_svg_overrides_generic_png(tmp_path):
    cmd, assets = _command(tmp_path)
    Image.new("RGBA", (1024, 1024), "blue").save(assets / "icon.png")
    (assets / "icon_web.svg").write_text(_svg("lime"))
    cmd.customize_icons()
    assert _centre(cmd.flutter_dir / "web/icons/Icon-512.png")[:3] == (0, 255, 0)


def test_svg_cache_detects_content_changes_and_skips_unchanged_source(tmp_path):
    cmd, assets = _command(tmp_path)
    cmd.customize_icons()
    output = cmd.flutter_dir / "web/icons/Icon-512.png"
    original_mtime = output.stat().st_mtime_ns
    cmd.customize_icons()
    assert output.stat().st_mtime_ns == original_mtime

    source = assets / "icon.svg"
    stat = source.stat()
    source.write_text(_svg("blue"))
    os.utime(source, ns=(stat.st_atime_ns, stat.st_mtime_ns))
    cmd.customize_icons()
    assert _centre(output)[:3] == (0, 0, 255)


def test_invalid_svg_stops_build_without_committing_cache(tmp_path):
    cmd, assets = _command(tmp_path)
    (assets / "icon.svg").write_text("not SVG")
    with pytest.raises(SystemExit, match="Could not generate app icons.*icon.svg"):
        cmd.customize_icons()
    assert not (cmd.build_dir / ".hash" / "icons").exists()


@pytest.mark.parametrize(
    ("target", "output"),
    [
        ("web", "web/splash/img/light-1x.png"),
        ("ipa", "ios/Runner/Assets.xcassets/LaunchImage.imageset/LaunchImage.png"),
        ("apk", "android/app/src/main/res/drawable-mdpi/splash.png"),
    ],
)
def test_svg_icon_splash_fallback_matches_png_display_size(tmp_path, target, output):
    cmd, assets = _command(tmp_path, target)
    cmd.customize_splash_images()
    path = cmd.flutter_dir / output
    with Image.open(path) as image:
        assert image.size == (256, 256)
    assert _centre(path)[:3] == (255, 0, 0)
    assert sorted(p.name for p in assets.iterdir()) == ["icon.svg"]


def test_svg_light_and_dark_splashes_override_icon_and_regenerate(tmp_path):
    cmd, assets = _command(tmp_path)
    (assets / "splash.svg").write_text(_svg("blue"))
    dark = assets / "splash_dark_web.svg"
    dark.write_text(_svg("lime"))
    cmd.customize_splash_images()
    light_output = cmd.flutter_dir / "web/splash/img/light-1x.png"
    dark_output = cmd.flutter_dir / "web/splash/img/dark-1x.png"
    assert _centre(light_output)[:3] == (0, 0, 255)
    assert _centre(dark_output)[:3] == (0, 255, 0)
    stat = dark.stat()
    dark.write_text(_svg("red"))
    os.utime(dark, ns=(stat.st_atime_ns, stat.st_mtime_ns))
    cmd.customize_splash_images()
    assert _centre(dark_output)[:3] == (255, 0, 0)


def test_invalid_dark_svg_stops_splash_generation(tmp_path):
    cmd, assets = _command(tmp_path)
    (assets / "splash_dark.svg").write_text("not SVG")
    with pytest.raises(
        SystemExit, match="Could not generate splash screens.*splash_dark"
    ):
        cmd.customize_splash_images()
    assert not (cmd.build_dir / ".hash" / "splashes").exists()
