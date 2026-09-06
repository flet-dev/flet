"""Splash wiring in `flet build`: the static template files and the config.

Every risk here is silent when it goes wrong - the build succeeds and the app
simply launches wrong - and none of it had test coverage before the Dart
generators were replaced.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from flet_cli.commands.build_base import BaseBuildCommand

BUILD_TEMPLATE_DIR = (
    Path(__file__).resolve().parents[3]
    / "templates"
    / "build"
    / "{{cookiecutter.out_dir}}"
)
ANDROID_RES = "android/app/src/main/res"

SPLASH_TEMPLATES = [
    f"{ANDROID_RES}/values/colors.xml",
    f"{ANDROID_RES}/values-night/colors.xml",
    f"{ANDROID_RES}/values-v31/styles.xml",
    f"{ANDROID_RES}/values-night-v31/styles.xml",
    f"{ANDROID_RES}/values/styles.xml",
    f"{ANDROID_RES}/values-night/styles.xml",
    f"{ANDROID_RES}/drawable/launch_background.xml",
    f"{ANDROID_RES}/drawable-v21/launch_background.xml",
    "ios/Runner/Base.lproj/LaunchScreen.storyboard",
    "web/index.html",
]


def _context(**overrides: Any) -> dict:
    """The declared cookiecutter defaults, with nested templates resolved."""

    env = Environment(undefined=StrictUndefined)
    ctx = {
        k: v
        for k, v in json.loads(
            (BUILD_TEMPLATE_DIR.parent / "cookiecutter.json").read_text()
        ).items()
        if not k.startswith("_")
    }
    # cookiecutter resolves values that are themselves templates.
    for key, value in list(ctx.items()):
        if isinstance(value, str) and "{{" in value:
            ctx[key] = env.from_string(value).render(cookiecutter=ctx)
    ctx.update(overrides)
    return ctx


def _render(path: str, **overrides: Any) -> str:
    env = Environment(
        loader=FileSystemLoader(str(BUILD_TEMPLATE_DIR)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    return env.get_template(path).render(cookiecutter=_context(**overrides))


def _splash(enabled: bool, **extra: Any) -> dict:
    base = _context()["splash"]
    return {**base, "android": enabled, "ios": enabled, "web": enabled, **extra}


class TestSplashTemplatesRender:
    """Both branches must render, and the disabled branch must stay stock."""

    @pytest.mark.parametrize("enabled", [True, False])
    @pytest.mark.parametrize("path", SPLASH_TEMPLATES)
    def test_renders_without_leftover_jinja(self, path, enabled):
        out = _render(path, splash=_splash(enabled))
        assert "{%" not in out and "{{" not in out

    @pytest.mark.parametrize("enabled", [True, False])
    @pytest.mark.parametrize(
        "path", [p for p in SPLASH_TEMPLATES if p != "web/index.html"]
    )
    def test_renders_parseable_xml(self, path, enabled):
        """A storyboard or resource file that fails to compile breaks the
        whole platform build, which is the hardest thing here to catch in
        CI."""
        ET.fromstring(_render(path, splash=_splash(enabled)))


class TestViewportMeta:
    """R1: flutter_native_splash was the only source of this tag.

    Without it a mobile browser lays the page out at a 980px viewport and
    scales it down, so the whole app renders tiny. It has to survive the
    splash being turned off, which is why it lives outside the splash block.
    """

    @pytest.mark.parametrize("enabled", [True, False])
    def test_present_in_both_branches(self, enabled):
        out = _render("web/index.html", splash=_splash(enabled))
        assert 'name="viewport"' in out
        assert "width=device-width" in out


class TestAndroid12Splash:
    """R2: without values-v31 the splash disappears on Android 12 and later.

    These files existed only because flutter_native_splash created them, and
    nothing in the template shipped them.
    """

    def test_v31_styles_reference_the_splash_icon(self):
        out = _render(f"{ANDROID_RES}/values-v31/styles.xml", splash=_splash(True))
        assert "windowSplashScreenAnimatedIcon" in out
        assert "@drawable/android12splash" in out
        assert "@color/flet_splash_background" in out

    def test_v31_styles_fall_back_to_stock_when_disabled(self):
        out = _render(f"{ANDROID_RES}/values-v31/styles.xml", splash=_splash(False))
        assert "windowSplashScreenAnimatedIcon" not in out
        assert "@drawable/launch_background" in out

    def test_night_variant_uses_the_dark_parent(self):
        out = _render(
            f"{ANDROID_RES}/values-night-v31/styles.xml", splash=_splash(True)
        )
        assert "Theme.Black.NoTitleBar" in out


class TestLaunchBackground:
    """What Android below 12 actually reads."""

    @pytest.mark.parametrize(
        "path",
        [
            f"{ANDROID_RES}/drawable/launch_background.xml",
            f"{ANDROID_RES}/drawable-v21/launch_background.xml",
        ],
    )
    def test_references_the_splash_bitmap_and_colour(self, path):
        """Both variants must agree: cookiecutter never deletes, and a stale
        `-v21` wins on API 21 and up."""
        out = _render(path, splash=_splash(True))
        assert "@drawable/splash" in out
        assert "@color/flet_splash_background" in out

    def test_disabled_branch_is_the_stock_flutter_content(self):
        out = _render(
            f"{ANDROID_RES}/drawable/launch_background.xml", splash=_splash(False)
        )
        assert "@android:color/white" in out
        assert "@drawable/splash" not in out


class TestSplashColors:
    """The colour reaches the XML and the pixels from one place."""

    def test_colors_xml_carries_the_configured_colour(self):
        out = _render(
            f"{ANDROID_RES}/values/colors.xml", splash=_splash(True, color="#ff0055")
        )
        assert '<color name="flet_splash_background">#ff0055</color>' in out

    def test_night_colors_xml_carries_the_dark_colour(self):
        out = _render(
            f"{ANDROID_RES}/values-night/colors.xml",
            splash=_splash(True, dark_color="#001122"),
        )
        assert "#001122" in out


class TestIOSStoryboard:
    """The launch screen light and dark both come through the asset catalog."""

    def test_background_layer_is_added_when_enabled(self):
        out = _render(
            "ios/Runner/Base.lproj/LaunchScreen.storyboard", splash=_splash(True)
        )
        assert 'image="LaunchBackground"' in out
        assert 'contentMode="center"' in out

    def test_disabled_branch_has_no_background_layer(self):
        out = _render(
            "ios/Runner/Base.lproj/LaunchScreen.storyboard", splash=_splash(False)
        )
        assert "LaunchBackground" not in out

    def test_asset_catalog_declares_all_six_launch_images(self):
        """The catalog is static, so a re-render can no longer revert it to a
        light-only three-entry version while the dark files sit orphaned."""
        contents = json.loads(
            (
                BUILD_TEMPLATE_DIR
                / "ios/Runner/Assets.xcassets/LaunchImage.imageset/Contents.json"
            ).read_text()
        )
        names = [i["filename"] for i in contents["images"]]
        assert names == [
            "LaunchImage.png",
            "LaunchImageDark.png",
            "LaunchImage@2x.png",
            "LaunchImageDark@2x.png",
            "LaunchImage@3x.png",
            "LaunchImageDark@3x.png",
        ]
        for name in names:
            assert (
                BUILD_TEMPLATE_DIR
                / "ios/Runner/Assets.xcassets/LaunchImage.imageset"
                / name
            ).is_file(), f"{name} is declared but not shipped"

    def test_launch_background_image_set_is_shipped(self):
        base = (
            BUILD_TEMPLATE_DIR / "ios/Runner/Assets.xcassets/LaunchBackground.imageset"
        )
        assert (base / "Contents.json").is_file()
        assert (base / "background.png").is_file()
        assert (base / "darkbackground.png").is_file()


class TestAndroidAdaptiveIcon:
    """The adaptive icon has to be *declared*, not just generated.

    flutter_launcher_icons wrote `mipmap-anydpi-v26/ic_launcher.xml` from the
    `adaptive_icon_*` pubspec keys. Dropping the tool without replacing that
    file left the foreground layers on disk with nothing pointing at them, so
    `android:icon="@mipmap/ic_launcher"` resolved to the legacy square mipmap
    instead - and a launcher wraps a legacy icon in its own circle and scales
    it to roughly 70%, which makes a correctly sized icon look small.
    """

    def test_adaptive_icon_xml_is_shipped(self):
        xml = BUILD_TEMPLATE_DIR / ANDROID_RES / "mipmap-anydpi-v26" / "ic_launcher.xml"
        assert xml.is_file(), "without this the launcher falls back to the legacy icon"
        root = ET.fromstring(xml.read_text())
        assert root.tag == "adaptive-icon"
        drawables = {child.tag: list(child.attrib.values())[0] for child in root}
        assert drawables["foreground"] == "@drawable/ic_launcher_foreground"
        assert drawables["background"] == "@color/ic_launcher_background"

    def test_background_colour_resource_is_declared(self):
        """A dedicated file, not colors.xml, which a plugin could collide with."""
        out = _render(
            f"{ANDROID_RES}/values/ic_launcher_background.xml",
            adaptive_icon_background="#ff0055",
        )
        root = ET.fromstring(out)
        colour = root.find("color")
        assert colour.get("name") == "ic_launcher_background"
        assert colour.text == "#ff0055"

    def test_foreground_layers_the_xml_references_are_generated(self):
        """The drawable the XML names must be one render_icons produces."""
        from flet_platform_assets import DEFAULT_SPECS

        produced = {t.relative_path for t in DEFAULT_SPECS["android"].targets}
        assert any(p.endswith("/ic_launcher_foreground.png") for p in produced), (
            "the XML references a drawable nothing generates"
        )

    @pytest.mark.parametrize("density", ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"])
    def test_template_ships_the_foreground_for_apps_with_no_icon(self, density):
        """An app with no icon of its own generates nothing, by design, so the
        template has to ship these. Without them
        `@drawable/ic_launcher_foreground` is unresolved and Android resource
        linking fails the build outright - a hard error, not a cosmetic one."""
        layer = (
            BUILD_TEMPLATE_DIR
            / ANDROID_RES
            / f"drawable-{density}"
            / "ic_launcher_foreground.png"
        )
        assert layer.is_file(), f"missing {density} foreground breaks `flet build apk`"

    def test_shipped_foreground_fits_the_circular_mask(self):
        """The mask is a circle, so what matters is how far the artwork's
        furthest point sits from the centre, not its extent on either axis.
        Framed at GLYPH_FRAC the mark reached 97% of the mask radius -
        uncut, but filling the circle edge to edge."""
        import math

        from PIL import Image

        path = (
            BUILD_TEMPLATE_DIR
            / ANDROID_RES
            / "drawable-xxxhdpi"
            / "ic_launcher_foreground.png"
        )
        with Image.open(path) as opened:
            image = opened.convert("RGBA")
        visible = round(image.width * 72 / 108)
        offset = (image.width - visible) // 2
        alpha = image.crop(
            (offset, offset, offset + visible, offset + visible)
        ).getchannel("A")
        pixels = alpha.load()
        centre = (visible - 1) / 2
        radius = visible / 2
        furthest = max(
            math.hypot(x - centre, y - centre)
            for y in range(visible)
            for x in range(visible)
            if pixels[x, y] > 8
        )
        assert furthest / radius < 0.90, "artwork fills the mask with no margin"


class TestSplashPlaceholders:
    """`@drawable/splash` must always resolve, even when nothing is generated.

    A custom build template may ship no `images/icon.png`, leaving no source
    to derive a splash from. The generator returns early there, which used to
    leave `launch_background.xml` and `values-v31/styles.xml` pointing at
    drawables that did not exist - Android resource linking fails outright,
    which is not the graceful degradation the code claimed.
    """

    @pytest.mark.parametrize("name", ["splash.png", "android12splash.png"])
    def test_base_density_placeholder_is_shipped(self, name):
        placeholder = BUILD_TEMPLATE_DIR / ANDROID_RES / "drawable" / name
        assert placeholder.is_file(), f"{name} missing: @drawable would dangle"

    @pytest.mark.parametrize("name", ["splash.png", "android12splash.png"])
    def test_placeholder_is_invisible(self, name):
        """It backstops linking only. A device with generated density
        variants uses those; one without shows the splash background alone."""
        from PIL import Image

        with Image.open(BUILD_TEMPLATE_DIR / ANDROID_RES / "drawable" / name) as im:
            assert im.size == (1, 1)
            assert im.convert("RGBA").getpixel((0, 0))[3] == 0

    def test_generated_densities_do_not_collide_with_it(self):
        """The generator writes density-qualified names, which Android
        prefers, so the placeholder is never what a real device shows."""
        from flet_platform_assets import ANDROID_DENSITIES

        assert "drawable" not in {f"drawable-{d}" for d in ANDROID_DENSITIES}


class TestIconBackground:
    """The colour behind artwork wherever alpha cannot survive.

    `assets/icon.png` is expected to be transparent, so this is what a user
    actually sees on Apple platforms: iOS must be flattened because the App
    Store rejects an alpha channel, and the macOS tile must be opaque to read
    as a tile. Both were hardcoded white while Android's equivalent was
    configurable, so a dark-brand app had no way out of a white square.
    """

    @staticmethod
    def _command(pyproject=None, platform="macos"):
        cmd = BaseBuildCommand.__new__(BaseBuildCommand)
        cmd.config_platform = platform
        values = pyproject or {}
        cmd.get_pyproject = lambda key=None: values.get(key)
        return cmd

    def test_defaults_to_white(self):
        assert self._command()._resolve_icon_background() == (255, 255, 255)

    def test_global_key_is_used(self):
        cmd = self._command({"tool.flet.icon_background": "#1a1a1a"})
        assert cmd._resolve_icon_background() == (26, 26, 26)

    def test_platform_key_overrides_the_global_one(self):
        """Same precedence the splash colours already use."""
        cmd = self._command(
            {
                "tool.flet.icon_background": "#ffffff",
                "tool.flet.macos.icon_background": "#ff0055",
            }
        )
        assert cmd._resolve_icon_background() == (255, 0, 85)

    def test_another_platform_key_is_ignored(self):
        cmd = self._command(
            {"tool.flet.ios.icon_background": "#ff0055"}, platform="macos"
        )
        assert cmd._resolve_icon_background() == (255, 255, 255)

    def test_invalid_colour_warns_and_falls_back(self, capsys):
        """A typo in a colour must not stop a build that would otherwise
        succeed."""
        cmd = self._command({"tool.flet.icon_background": "octarine"})
        assert cmd._resolve_icon_background() == (255, 255, 255)
        assert "octarine" in "".join(capsys.readouterr())

    def test_it_reaches_every_surface_that_rejects_alpha(self):
        """One colour covers the iOS flatten, the macOS tile and the opaque
        web icons - the three places a transparent source cannot survive."""
        from flet_platform_assets import IconOptions, render_icons
        from PIL import Image

        # Deliberately not square: a filled square with transparent margins is
        # what `looks_pre_shaped` treats as an already-shaped icon, which would
        # bypass the macOS grid and take the tile colour out of the picture.
        glyph = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        glyph.paste(Image.new("RGBA", (300, 420), (0, 0, 0, 255)), (362, 302))
        options = IconOptions(background=(255, 0, 85))

        ios = next(
            a.image
            for a in render_icons(glyph, options, platform="ios").assets
            if "1024x1024" in a.relative_path
        )
        assert ios.getpixel((5, 5)) == (255, 0, 85)

        macos = next(
            a.image
            for a in render_icons(glyph, options, platform="macos").assets
            if a.image.size == (1024, 1024)
        )
        assert macos.getpixel((512, 130))[:3] == (255, 0, 85), "the tile"

        web = {
            a.relative_path: a.image
            for a in render_icons(glyph, options, platform="web").assets
        }
        assert web["web/icons/Icon-maskable-192.png"].getpixel((2, 2)) == (255, 0, 85)
        assert web["web/icons/Icon-192.png"].getpixel((2, 2))[3] == 0, "keeps alpha"


class TestPubspecHasNoAssetGenerators:
    """Both Dart tools are gone, config blocks and dev_dependencies alike."""

    def test_no_generator_config_or_dependency(self):
        text = (BUILD_TEMPLATE_DIR / "pubspec.yaml").read_text()
        assert "flutter_launcher_icons" not in text
        assert "flutter_native_splash" not in text


class TestResolveSplash:
    """Colours and toggles are resolved once, for the template and the pixels.

    `create_flutter_project` filters `None` out of the context, so a `None`
    here would leave the template referencing an undefined key.
    """

    @staticmethod
    def _command(pyproject=None, **options):
        cmd = BaseBuildCommand.__new__(BaseBuildCommand)
        cmd.config_platform = "android"
        defaults = {
            "no_android_splash": None,
            "no_ios_splash": None,
            "no_web_splash": None,
            "splash_color": None,
            "splash_dark_color": None,
        }
        cmd.options = SimpleNamespace(**{**defaults, **options})
        values = pyproject or {}
        cmd.get_pyproject = lambda key=None: values.get(key)
        return cmd

    def test_defaults_are_enabled_and_never_none(self):
        resolved = self._command()._resolve_splash()
        assert resolved == {
            "android": True,
            "ios": True,
            "web": True,
            "color": "#ffffff",
            "dark_color": "#222222",
        }
        assert None not in resolved.values()

    def test_cli_flag_disables_one_platform(self):
        resolved = self._command(no_web_splash=True)._resolve_splash()
        assert resolved["web"] is False
        assert resolved["android"] is True

    def test_pyproject_disables_one_platform(self):
        resolved = self._command({"tool.flet.splash.android": False})._resolve_splash()
        assert resolved["android"] is False

    def test_cli_flag_wins_over_pyproject(self):
        cmd = self._command({"tool.flet.splash.web": False}, no_web_splash=False)
        assert cmd._resolve_splash()["web"] is True

    def test_platform_colour_wins_over_the_global_one(self):
        cmd = self._command(
            {
                "tool.flet.splash.color": "#111111",
                "tool.flet.android.splash.color": "#222222",
            }
        )
        assert cmd._resolve_splash()["color"] == "#222222"

    def test_cli_colour_wins_over_everything(self):
        cmd = self._command({"tool.flet.splash.color": "#111111"}, splash_color="#abc")
        assert cmd._resolve_splash()["color"] == "#abc"


class TestWebRuntimeJsLiterals:
    """`index.html` had three `{% if no_cdn %}` blocks on the same condition
    interleaved into a JavaScript object literal. Deciding in Python puts the
    quoting in one testable place and leaves the template flat."""

    def test_cdn_mode_emits_nulls(self):
        js = BaseBuildCommand._resolve_web_runtime_js(False, "/", "0.28.0")
        assert js["no_cdn_js"] == "false"
        assert js["canvas_kit_base_url_js"] == "null"
        assert js["font_fallback_base_url_js"] == "null"
        assert "cdn.jsdelivr.net" in js["pyodide_url_js"]
        assert "0.28.0" in js["pyodide_url_js"]

    def test_no_cdn_mode_pins_local_copies(self):
        js = BaseBuildCommand._resolve_web_runtime_js(True, "/app/", "0.28.0")
        assert js["no_cdn_js"] == "true"
        assert js["canvas_kit_base_url_js"] == '"/app/canvaskit/"'
        assert js["pyodide_url_js"] == '"/app/pyodide/pyodide.mjs"'
        assert js["font_fallback_base_url_js"] == '"assets/fonts/"'

    @pytest.mark.parametrize("no_cdn", [True, False])
    def test_every_value_is_a_valid_js_literal(self, no_cdn):
        """json.dumps output is valid JavaScript for these shapes, which is
        the whole reason quoting moved out of the template."""
        for value in BaseBuildCommand._resolve_web_runtime_js(
            no_cdn, "/", "0.28.0"
        ).values():
            json.loads(value)  # null / true / false / "string" all round-trip

    @pytest.mark.parametrize("no_cdn", [True, False])
    def test_template_renders_them_without_conditionals(self, no_cdn):
        out = _render(
            "web/index.html",
            no_cdn=no_cdn,
            **BaseBuildCommand._resolve_web_runtime_js(no_cdn, "/", "0.28.0"),
        )
        literal = out[out.index("var flet = {") : out.index("flet.flutterAppLoaded")]
        assert "toLowerCase" not in literal
        assert f"noCdn: {str(no_cdn).lower()}," in literal
