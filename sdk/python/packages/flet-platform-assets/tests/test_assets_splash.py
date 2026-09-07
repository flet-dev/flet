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

    @pytest.mark.parametrize("light_background", [None, "#ffffff"])
    def test_dark_background_reuses_light_artwork(
        self, art, tmp_path, light_background
    ):
        result = render_splash(
            art,
            options=SplashOptions(
                icon_background=light_background,
                icon_dark_background="#112233",
            ),
            platform="android",
        )
        write(result, tmp_path, declared_only=False)
        for density, multiplier in ANDROID_DENSITIES.items():
            night = f"{ANDROID_RES}/drawable-night-{density}"
            path = tmp_path / night / "android12splash.png"
            with Image.open(path) as image:
                assert image.size == (round(240 * multiplier),) * 2
                assert image.getpixel((0, 0)) == (17, 34, 51)
                assert image.getpixel((image.width // 2, image.height // 2)) == (
                    255,
                    0,
                    85,
                )
            assert not (tmp_path / night / "splash.png").exists()

        # Removing the override must remove the generated night icons too.
        write(render_splash(art, platform="android"), tmp_path, declared_only=False)
        assert not list(tmp_path.glob(f"{ANDROID_RES}/drawable-night-*/*.png"))

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

    @pytest.mark.parametrize("separate_dark_artwork", [False, True])
    def test_background_swatches_are_1x1_solids(
        self, art, dark_art, separate_dark_artwork
    ):
        images = by_path(
            render_splash(
                art,
                dark_art if separate_dark_artwork else None,
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


class TestOpaqueArtwork:
    """Opaque artwork is a finished composition, on splash as on icons.

    The extent measures return `None` for it, which is the answer rather than
    a missing measurement: there is no glyph floating on a canvas to reframe,
    and its colour is meant to reach the edges.
    """

    @pytest.fixture
    def finished(self):
        img = Image.new("RGBA", (1024, 1024), (66, 133, 244, 255))
        img.paste(Image.new("RGBA", (600, 600), (255, 255, 255, 255)), (212, 212))
        return img

    def test_not_framed_even_when_derived_from_an_icon(self, finished):
        images = by_path(render_splash(finished, platform="web", derived=True))
        assert images["web/splash/img/light-4x.png"].size == (1024, 1024)
        assert alpha_extent(images["web/splash/img/light-4x.png"]) is None

    def test_placed_whole_on_the_android_12_canvas(self, finished):
        """Shrinking it into the middle of the circle would ring a finished
        design with background colour; letting it bleed is the intent."""
        images = by_path(render_splash(finished, platform="android", derived=True))
        icon = images[f"{ANDROID_RES}/drawable-mdpi/android12splash.png"]
        assert icon.size == (288, 288)
        assert icon.convert("RGBA").getpixel((4, 144))[:3] == (66, 133, 244)

    def test_no_warning(self, finished):
        """Filling the frame is what opaque artwork is for."""
        assert not render_splash(finished, platform="android", derived=True).warnings

    def test_a_transparent_glyph_is_still_fitted(self):
        glyph = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        glyph.paste(Image.new("RGBA", (1024, 1024), (255, 0, 85, 255)), (0, 0))
        glyph.putalpha(
            Image.new("L", (1024, 1024), 0)
        )  # fully transparent -> nothing to place
        solid = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        solid.paste(Image.new("RGBA", (900, 900), (255, 0, 85, 255)), (62, 62))
        images = by_path(render_splash(solid, platform="android", derived=True))
        icon = images[f"{ANDROID_RES}/drawable-mdpi/android12splash.png"]
        assert alpha_extent(icon) <= ANDROID_12_VISIBLE_FRACTION + 0.02


class TestRenamedKeysStillWork:
    """`icon_bgcolor` and friends were renamed; the old spellings still read."""

    @staticmethod
    def _command(pyproject):
        from types import SimpleNamespace

        from flet_cli.commands.build_base import BaseBuildCommand

        cmd = BaseBuildCommand.__new__(BaseBuildCommand)
        cmd.config_platform = "android"
        cmd.get_pyproject = lambda key=None: pyproject.get(key)
        cmd.options = SimpleNamespace()
        return cmd

    @pytest.mark.parametrize(
        ("old", "new"),
        [
            ("icon_bgcolor", "icon_background"),
            ("icon_dark_bgcolor", "icon_dark_background"),
            ("android_12_fit", "icon_fit"),
        ],
    )
    def test_the_former_name_is_read(self, old, new):
        cmd = self._command({f"tool.flet.splash.{old}": "#abcdef"})
        assert cmd.splash_setting(new) == "#abcdef"

    def test_the_current_name_wins(self):
        cmd = self._command(
            {
                "tool.flet.splash.icon_bgcolor": "#111111",
                "tool.flet.splash.icon_background": "#222222",
            }
        )
        assert cmd.splash_setting("icon_background") == "#222222"

    def test_a_platform_override_applies_to_the_former_name_too(self):
        cmd = self._command(
            {
                "tool.flet.splash.icon_bgcolor": "#111111",
                "tool.flet.android.splash.icon_bgcolor": "#333333",
            }
        )
        assert cmd.splash_setting("icon_background") == "#333333"
