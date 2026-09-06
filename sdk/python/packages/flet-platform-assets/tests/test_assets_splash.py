"""Tests concerning splash screen rendering.

The sizes asserted here were measured from a real flutter_native_splash
build, so a change to them is a change to how every existing app looks on
launch, not just a refactor.
"""

import pytest
from flet_platform_assets import (
    ANDROID_12_VISIBLE_FRACTION,
    ANDROID_DENSITIES,
    SplashOptions,
    render_splash,
    write,
)
from flet_platform_assets._imaging import alpha_extent
from PIL import Image

ANDROID_RES = "android/app/src/main/res"
IOS_LAUNCH = "ios/Runner/Assets.xcassets/LaunchImage.imageset"

# Measured from sdk/python/playground/v1/abc1, built by flutter_native_splash
# from a 1024px source.
FNS_SPLASH_SIZES = {
    "mdpi": 256,
    "hdpi": 384,
    "xhdpi": 512,
    "xxhdpi": 768,
    "xxxhdpi": 1024,
}


@pytest.fixture
def art():
    """1024px artwork with transparent margins, like a real icon."""
    img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    img.paste(Image.new("RGBA", (900, 900), (255, 0, 85, 255)), (62, 62))
    return img


@pytest.fixture
def dark_art():
    img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    img.paste(Image.new("RGBA", (900, 900), (0, 85, 255, 255)), (62, 62))
    return img


def by_path(result):
    return {a.relative_path: a.image for a in result.assets}


class TestAndroidSplash:
    """Sizes must not drift: they set the on-screen size of every splash."""

    def test_splash_sizes_match_flutter_native_splash(self, art):
        images = by_path(render_splash(art, platform="android"))
        for density, size in FNS_SPLASH_SIZES.items():
            path = f"{ANDROID_RES}/drawable-{density}/splash.png"
            assert images[path].size == (size, size)

    def test_dark_variants_are_written_when_distinct(self, art, dark_art):
        images = by_path(render_splash(art, dark_art, platform="android"))
        for density, size in FNS_SPLASH_SIZES.items():
            path = f"{ANDROID_RES}/drawable-night-{density}/splash.png"
            assert images[path].size == (size, size)

    def test_dark_variants_are_pruned_when_not_distinct(self, art):
        """Cookiecutter overwrites but never deletes, so turning dark mode off
        would otherwise keep serving the old dark splash."""
        result = render_splash(art, platform="android")
        assert not any("night" in a.relative_path for a in result.assets)
        assert f"{ANDROID_RES}/drawable-night-xxxhdpi/splash.png" in result.stale

    def test_flutter_native_splash_background_pngs_are_pruned(self, art):
        """Replaced by @color/flet_splash_background in a static resource."""
        result = render_splash(art, platform="android")
        assert f"{ANDROID_RES}/drawable/background.png" in result.stale
        assert f"{ANDROID_RES}/drawable-night-v21/background.png" in result.stale


class TestAndroid12Splash:
    """The one place artwork is deliberately reframed.

    Android crops this canvas to a circle covering the central two thirds,
    always. flutter_native_splash passed the source through at the ordinary
    splash sizes and told users to pad it themselves.
    """

    def test_canvas_follows_the_platform_spec_not_the_splash_size(self, art):
        images = by_path(render_splash(art, platform="android"))
        for density, multiplier in ANDROID_DENSITIES.items():
            path = f"{ANDROID_RES}/drawable-{density}/android12splash.png"
            assert images[path].size == (round(288 * multiplier),) * 2

    def test_icon_background_switches_to_the_smaller_canvas(self, art):
        images = by_path(
            render_splash(
                art,
                options=SplashOptions(icon_background="#ff0055"),
                platform="android",
            )
        )
        path = f"{ANDROID_RES}/drawable-xxxhdpi/android12splash.png"
        assert images[path].size == (960, 960)
        assert images[path].mode == "RGB", "an icon background must be opaque"

    def test_artwork_is_fitted_inside_the_visible_circle(self, art):
        images = by_path(render_splash(art, platform="android"))
        big = images[f"{ANDROID_RES}/drawable-xxxhdpi/android12splash.png"]
        assert alpha_extent(big) <= ANDROID_12_VISIBLE_FRACTION + 0.01

    def test_pre_padded_artwork_is_not_shrunk_twice(self):
        """A user who followed the platform guidance already fits the circle."""
        padded = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        padded.paste(Image.new("RGBA", (600, 600), (255, 0, 85, 255)), (212, 212))
        before = alpha_extent(padded)

        images = by_path(render_splash(padded, platform="android"))
        big = images[f"{ANDROID_RES}/drawable-xxxhdpi/android12splash.png"]

        assert alpha_extent(big) == pytest.approx(before, abs=0.02)

    def test_fit_none_passes_through_and_warns(self, art):
        result = render_splash(
            art, options=SplashOptions(icon_fit="none"), platform="android"
        )
        big = by_path(result)[f"{ANDROID_RES}/drawable-xxxhdpi/android12splash.png"]
        assert alpha_extent(big) > ANDROID_12_VISIBLE_FRACTION
        assert any("will be cut off" in w for w in result.warnings)

    def test_unknown_fit_is_rejected(self, art):
        with pytest.raises(ValueError, match="icon_fit"):
            render_splash(
                art, options=SplashOptions(icon_fit="cover"), platform="android"
            )


class TestIOSSplash:
    """The asset catalog declares all six launch images unconditionally."""

    def test_light_and_dark_are_always_written(self, art):
        images = by_path(render_splash(art, platform="ios"))
        for suffix, size in (("", 256), ("@2x", 512), ("@3x", 768)):
            assert images[f"{IOS_LAUNCH}/LaunchImage{suffix}.png"].size == (size, size)
            assert images[f"{IOS_LAUNCH}/LaunchImageDark{suffix}.png"].size == (
                size,
                size,
            )

    def test_dark_reuses_light_when_not_distinct(self, art):
        images = by_path(render_splash(art, platform="ios"))
        assert (
            images[f"{IOS_LAUNCH}/LaunchImage@2x.png"].tobytes()
            == images[f"{IOS_LAUNCH}/LaunchImageDark@2x.png"].tobytes()
        )

    def test_dark_differs_when_distinct(self, art, dark_art):
        images = by_path(render_splash(art, dark_art, platform="ios"))
        assert (
            images[f"{IOS_LAUNCH}/LaunchImage@2x.png"].tobytes()
            != images[f"{IOS_LAUNCH}/LaunchImageDark@2x.png"].tobytes()
        )

    def test_background_swatches_are_1x1_solids(self, art, dark_art):
        images = by_path(
            render_splash(
                art,
                dark_art,
                SplashOptions(color="#ff0055", dark_color="#001122"),
                platform="ios",
            )
        )
        base = "ios/Runner/Assets.xcassets/LaunchBackground.imageset"
        assert images[f"{base}/background.png"].size == (1, 1)
        assert images[f"{base}/background.png"].getpixel((0, 0)) == (255, 0, 85)
        assert images[f"{base}/darkbackground.png"].getpixel((0, 0)) == (0, 17, 34)


class TestWebSplash:
    """A .webp source used to produce a srcset pointing at missing files."""

    def test_sizes_cover_1x_through_4x(self, art):
        images = by_path(render_splash(art, platform="web"))
        for name, size in (("1x", 256), ("2x", 512), ("3x", 768), ("4x", 1024)):
            assert images[f"web/splash/img/light-{name}.png"].size == (size, size)
            assert images[f"web/splash/img/dark-{name}.png"].size == (size, size)

    def test_output_is_always_png(self, art):
        result = render_splash(art, platform="web")
        assert all(a.relative_path.endswith(".png") for a in result.assets)

    def test_stale_webp_from_an_earlier_build_is_pruned(self, art):
        result = render_splash(art, platform="web")
        assert "web/splash/img/light-4x.webp" in result.stale


class TestRenderSplash:
    def test_unknown_platform_is_rejected(self, art):
        with pytest.raises(ValueError, match="unknown platform"):
            render_splash(art, platform="linux")


class TestWriteRemovesStale:
    """Pruning is the half that cookiecutter cannot do."""

    def test_stale_files_are_deleted(self, art, tmp_path):
        stale = tmp_path / ANDROID_RES / "drawable-night-xxxhdpi" / "splash.png"
        stale.parent.mkdir(parents=True)
        stale.write_bytes(b"old")

        write(render_splash(art, platform="android"), tmp_path, declared_only=False)

        assert not stale.exists()

    def test_missing_stale_file_is_not_an_error(self, art, tmp_path):
        write(render_splash(art, platform="web"), tmp_path, declared_only=False)
        assert (tmp_path / "web/splash/img/light-1x.png").exists()
