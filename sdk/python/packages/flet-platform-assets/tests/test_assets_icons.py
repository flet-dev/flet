"""Tests concerning app icon rendering.

`render_icons` is pure, so almost everything here asserts on returned images
and warnings with no filesystem at all. Only `write` needs a temp project.
"""

import sys

import pytest
from flet_platform_assets import (
    ANDROID_ADAPTIVE_SIZES,
    ANDROID_MIPMAP_SIZES,
    LINUX_HICOLOR_SIZES,
    WINDOWS_ICO_SIZES,
    AssetSpec,
    IconOptions,
    RenderResult,
    Target,
    render_icons,
    web_targets_from_manifest,
    write,
)
from flet_platform_assets._imaging import alpha_extent, superellipse_mask
from PIL import Image


@pytest.fixture
def logo():
    """An ordinary logo: transparent margins, not a pre-shaped tile."""
    img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    img.paste(Image.new("RGBA", (600, 800), (255, 0, 85, 255)), (212, 112))
    return img


@pytest.fixture
def shaped_tile():
    """A source that already has a macOS-style shape baked in.

    Deliberately inset by a different fraction than `MACOS_TILE_RATIO`, so
    "the grid was applied" and "the source passed through" cannot produce the
    same measurement.
    """
    canvas = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    art = Image.new("RGBA", (900, 900), (255, 0, 85, 255))
    art.putalpha(superellipse_mask(900, 5.0))
    canvas.alpha_composite(art, (62, 62))
    return canvas


def macos_1024(result: RenderResult) -> Image.Image:
    return by_path(result)[
        "macos/Runner/Assets.xcassets/AppIcon.appiconset/app_icon_1024.png"
    ]


def by_path(result: RenderResult) -> dict[str, Image.Image]:
    return {a.relative_path: a.image for a in result.assets}


class TestImportIsolation:
    """Flet Studio depends on this package importing nothing but Pillow.

    A stray convenience import of `flet_cli` would drag in cookiecutter, rich
    and watchdog, and nothing else would notice.
    """

    def test_imports_only_pillow(self):
        for name in list(sys.modules):
            if name.startswith("flet_platform_assets"):
                del sys.modules[name]
        before = set(sys.modules)

        import flet_platform_assets  # noqa: F401

        pulled = {m.split(".")[0] for m in set(sys.modules) - before}
        assert not pulled & {"flet", "flet_cli", "rich", "cookiecutter", "yaml"}


class TestIOS:
    """The App Store rejects an alpha channel, and Apple's tooling checks."""

    def test_every_icon_is_opaque_rgb(self, logo):
        result = render_icons(logo, platform="ios")
        assert result.assets
        assert {a.image.mode for a in result.assets} == {"RGB"}

    def test_produces_fifteen_files_at_declared_sizes(self, logo):
        images = by_path(render_icons(logo, platform="ios"))
        assert len(images) == 15
        assert images[
            "ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-1024x1024@1x.png"
        ].size == (1024, 1024)

    def test_each_image_matches_its_declared_size(self, logo):
        spec = render_icons(logo, platform="ios")
        for asset in spec.assets:
            assert asset.image.width == asset.image.height


class TestMacOS:
    """The icon grid, and the two ways of bypassing it."""

    def test_grid_insets_the_artwork_and_adds_a_shadow(self, logo):
        big = macos_1024(render_icons(logo, platform="macos"))
        assert big.getpixel((0, 0))[3] == 0, "corners must be cut away"
        # The tile is inset; the shadow spreads slightly past it.
        assert 0.80 < alpha_extent(big) < 0.92

    def test_smaller_sizes_are_reductions_of_one_composition(self, logo):
        images = by_path(render_icons(logo, platform="macos"))
        sizes = {im.size[0] for im in images.values()}
        assert sizes == {16, 32, 64, 128, 256, 512, 1024}

    def test_pre_shaped_source_is_not_shaped_twice(self, shaped_tile):
        result = render_icons(shaped_tile, platform="macos")
        assert macos_1024(result).tobytes() == shaped_tile.tobytes(), (
            "a shaped source should pass through untouched, not be inset again"
        )
        assert any("already looks like a shaped icon" in w for w in result.warnings)

    def test_grid_style_overrides_the_detector(self, shaped_tile):
        """The escape hatch in the other direction."""
        result = render_icons(
            shaped_tile, IconOptions(macos_style="grid"), platform="macos"
        )
        assert macos_1024(result).tobytes() != shaped_tile.tobytes()
        assert alpha_extent(macos_1024(result)) < alpha_extent(shaped_tile)
        assert not result.warnings

    def test_raw_style_skips_the_grid_without_warning(self, logo):
        result = render_icons(logo, IconOptions(macos_style="raw"), platform="macos")
        assert not result.warnings

    def test_ico_source_skips_the_grid_silently(self, shaped_tile):
        """`pre_rendered` is the author's explicit choice, so it is not a warning."""
        result = render_icons(shaped_tile, platform="macos", pre_rendered=True)
        assert not result.warnings

    def test_unknown_style_is_rejected(self, logo):
        with pytest.raises(ValueError, match="macos_style"):
            render_icons(logo, IconOptions(macos_style="squircle"), platform="macos")


class TestAndroid:
    """Adaptive icons pass through full-bleed; we warn rather than reframe."""

    def test_produces_mipmaps_and_adaptive_layers(self, logo):
        images = by_path(render_icons(logo, platform="android"))
        assert len(images) == len(ANDROID_MIPMAP_SIZES) + len(ANDROID_ADAPTIVE_SIZES)
        for directory, size in ANDROID_ADAPTIVE_SIZES.items():
            path = f"android/app/src/main/res/{directory}/ic_launcher_foreground.png"
            assert images[path].size == (size, size)

    def test_artwork_is_never_inset(self, logo):
        """Rule 1: the user's padding is their design decision."""
        images = by_path(render_icons(logo, platform="android"))
        big = images[
            "android/app/src/main/res/drawable-xxxhdpi/ic_launcher_foreground.png"
        ]
        assert alpha_extent(big) == pytest.approx(alpha_extent(logo), abs=0.02)

    def test_full_bleed_artwork_warns_about_the_safe_zone(self, logo):
        result = render_icons(logo, platform="android")
        assert any("central 67%" in w for w in result.warnings)

    def test_artwork_inside_the_safe_zone_is_silent(self):
        img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        img.paste(Image.new("RGBA", (512, 512), (255, 0, 85, 255)), (256, 256))
        assert not render_icons(img, platform="android").warnings


class TestWindows:
    """A single 256px entry is why taskbar icons look mushy."""

    def test_ico_carries_every_size(self, logo):
        result = render_icons(logo, platform="windows")
        entries = result.ico["windows/runner/resources/app_icon.ico"]
        assert sorted(entries) == sorted(WINDOWS_ICO_SIZES)

    def test_each_entry_is_scaled_independently(self, logo):
        entries = render_icons(logo, platform="windows").ico[
            "windows/runner/resources/app_icon.ico"
        ]
        for size, image in entries.items():
            assert image.size == (size, size)


class TestWeb:
    """Maskables must be opaque; the favicon must not be 16px."""

    def test_favicon_is_32px(self, logo):
        images = by_path(render_icons(logo, platform="web"))
        assert images["web/favicon.png"].size == (32, 32)

    def test_maskable_icons_are_opaque_and_distinct(self, logo):
        images = by_path(render_icons(logo, platform="web"))
        maskable = images["web/icons/Icon-maskable-192.png"]
        plain = images["web/icons/Icon-192.png"]
        assert maskable.mode == "RGB", "a transparent maskable renders black corners"
        assert plain.mode == "RGBA"
        assert maskable.tobytes() != plain.convert("RGB").tobytes()

    def test_apple_touch_icon_is_produced(self, logo):
        """The template's index.html links to it; FLI never generated it."""
        images = by_path(render_icons(logo, platform="web"))
        assert images["web/icons/apple-touch-icon-192.png"].mode == "RGB"

    def test_manifest_drives_the_target_list(self):
        spec = web_targets_from_manifest(
            {
                "icons": [
                    {"src": "icons/Icon-192.png", "sizes": "192x192"},
                    {
                        "src": "icons/Icon-maskable-512.png",
                        "sizes": "512x512",
                        "purpose": "maskable",
                    },
                ]
            }
        )
        targets = {t.relative_path: t for t in spec.targets}
        assert targets["web/icons/Icon-192.png"].opaque is False
        assert targets["web/icons/Icon-maskable-512.png"].opaque is True

    def test_malformed_manifest_entries_are_skipped(self):
        spec = web_targets_from_manifest(
            {
                "icons": [
                    {"src": "a.png"},
                    {"sizes": "192x192"},
                    {"src": "b", "sizes": "x"},
                ]
            }
        )
        assert [t.relative_path for t in spec.targets] == [
            "web/favicon.png",
            "web/icons/apple-touch-icon-192.png",
        ]


class TestLinux:
    """flutter_launcher_icons has no Linux generator at all."""

    def test_every_hicolor_size_is_produced(self, logo):
        images = by_path(render_icons(logo, platform="linux"))
        for size in LINUX_HICOLOR_SIZES:
            path = f"linux/icons/hicolor/{size}x{size}/apps/com.example.app.png"
            assert images[path].size == (size, size), (
                "a directory claiming one size while holding another gets "
                "scaled wrongly by the icon cache"
            )

    def test_application_id_names_the_files(self, logo):
        images = by_path(
            render_icons(
                logo, IconOptions(application_id="com.flet.demo"), platform="linux"
            )
        )
        assert any("com.flet.demo.png" in p for p in images)

    def test_runner_window_icon_is_produced(self, logo):
        images = by_path(render_icons(logo, platform="linux"))
        assert images["linux/app_icon.png"].size == (256, 256)


class TestRenderIcons:
    """Cross-platform behaviour."""

    def test_unknown_platform_is_rejected(self, logo):
        with pytest.raises(ValueError, match="unknown platform"):
            render_icons(logo, platform="haiku")

    def test_spec_overrides_the_defaults(self, logo):
        spec = AssetSpec(targets=[Target("web/only.png", 48)])
        images = by_path(render_icons(logo, spec=spec, platform="web"))
        assert list(images) == ["web/only.png"]


class TestWrite:
    """The only function that touches the filesystem."""

    def test_declared_only_skips_files_the_project_does_not_have(self, logo, tmp_path):
        result = render_icons(logo, platform="web")
        (tmp_path / "web").mkdir()
        (tmp_path / "web" / "favicon.png").write_bytes(b"")

        written = write(result, tmp_path)

        assert [p.name for p in written] == ["favicon.png"]

    def test_declared_only_false_creates_missing_files(self, logo, tmp_path):
        result = render_icons(logo, platform="android")
        written = write(result, tmp_path, declared_only=False)
        assert len(written) == len(result.assets)
        assert all(p.exists() for p in written)

    def test_ico_is_written_as_one_file(self, logo, tmp_path):
        result = render_icons(logo, platform="windows")
        written = write(result, tmp_path, declared_only=False)
        assert [p.name for p in written] == ["app_icon.ico"]
        with Image.open(written[0]) as ico:
            assert sorted(w for w, _ in ico.ico.sizes()) == sorted(WINDOWS_ICO_SIZES)
