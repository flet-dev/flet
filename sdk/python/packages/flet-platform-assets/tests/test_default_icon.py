from flet_platform_assets import (
    DEFAULT_ICON,
    IconOptions,
    SplashOptions,
    load_source,
    render_icons,
    render_splash,
    square,
)


def test_default_icon_is_bundled():
    assert DEFAULT_ICON.is_file()
    assert DEFAULT_ICON.suffix == ".svg"


def test_default_icon_renders_cleanly_on_every_platform():
    """`flet build` uses it for every app without an icon, so a warning here
    would show up in every such build."""
    source, pre_rendered = load_source(DEFAULT_ICON)
    assert source.width == source.height
    for platform in ("ios", "macos", "android", "windows", "linux", "web"):
        result = render_icons(
            source,
            IconOptions(),
            platform=platform,
            pre_rendered=pre_rendered,
            derived=True,
        )
        assert result.assets or result.ico, platform
        assert result.warnings == [], platform


def test_default_icon_renders_a_splash_cleanly():
    light, warning = square(load_source(DEFAULT_ICON, svg_size=1024)[0])
    assert warning is None
    for platform in ("android", "ios", "web"):
        result = render_splash(
            light, None, SplashOptions(), platform=platform, derived=True
        )
        assert result.warnings == [], platform
