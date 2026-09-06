"""Rendering splash screens for each platform Flet builds for.

Pure, like :mod:`._icons`: takes images, returns images.

Sizes follow the `width * density / 4` rule flutter_native_splash used, so a
splash keeps the on-screen size it has today - a 1024px source renders at
256 dp, pt or CSS px. Only the *pixels* are produced here; the XML, the
storyboard and the HTML that reference them are shipped as static template
files, so there is nothing to author at build time and nothing to drift.
"""

from __future__ import annotations

from PIL import Image

from ._icons import _frame
from ._imaging import (
    alpha_extent,
    density_size,
    parse_hex_color,
    place,
    scale_to_fit,
)
from ._models import RenderResult, SplashOptions

__all__ = [
    "ANDROID_12_VISIBLE_FRACTION",
    "ANDROID_DENSITIES",
    "IOS_SCALES",
    "WEB_SCALES",
    "render_splash",
]

ANDROID_DENSITIES = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
IOS_SCALES = {"": 1, "@2x": 2, "@3x": 3}
WEB_SCALES = {"1x": 1, "2x": 2, "3x": 3, "4x": 4}

# Android 12's splash icon is specified in dp, not derived from the source:
# 288dp square with a 192dp visible circle, or 240dp/160dp when an icon
# background is set. Both are the same 2/3 ratio.
ANDROID_12_CANVAS_DP = 288
ANDROID_12_CANVAS_DP_WITH_BACKGROUND = 240
ANDROID_12_VISIBLE_FRACTION = 2 / 3

_ANDROID_RES = "android/app/src/main/res"
_IOS_LAUNCH = "ios/Runner/Assets.xcassets/LaunchImage.imageset"
_IOS_BACKGROUND = "ios/Runner/Assets.xcassets/LaunchBackground.imageset"

# flutter_native_splash painted the launch background with a 1x1 PNG stretched
# to fill. Android now uses `@color/flet_splash_background` from a static
# resource file instead, so these are removed rather than rewritten.
_ANDROID_STALE = [
    f"{_ANDROID_RES}/{directory}/background.png"
    for directory in (
        "drawable",
        "drawable-v21",
        "drawable-night",
        "drawable-night-v21",
    )
]


def render_splash(
    light: Image.Image,
    dark: Image.Image | None = None,
    options: SplashOptions | None = None,
    *,
    platform: str,
    derived: bool = False,
) -> RenderResult:
    """Render every splash asset for one platform.

    Unlike :func:`~flet_platform_assets.render_icons` this takes no `spec`.
    An icon target list is the *project's* declaration, read from its
    `Contents.json` and `manifest.json`; a splash file list is fixed by
    convention, so there would be nothing for a caller to override.

    Args:
        light: The light-mode artwork, already normalised to `RGBA`.
        dark: Dark-mode artwork. When omitted, dark and light are not
            distinct: per-platform dark outputs are skipped where the
            platform treats them as optional, and reuse `light` where its
            asset catalog declares them unconditionally.
        options: Colours and fitting behaviour; defaults are used when
            omitted.
        platform: One of `android`, `ios`, `web`.
        derived: The artwork came from `icon.png` rather than a splash image,
            so it is framed - an app icon fills its canvas by design, and a
            splash drawn at that size reads as an oversized logo.

    Returns:
        The rendered assets, any diagnostics, and the stale files a previous
            generator left behind.

    Raises:
        ValueError: If `platform` is not recognised, or `icon_fit` is
            not a known mode.
    """

    options = options or SplashOptions()
    if options.icon_fit not in ("contain", "none"):
        raise ValueError(f"unknown splash icon_fit: {options.icon_fit!r}")

    if derived:
        light = _frame(light, "splash")
        if dark is not None:
            dark = _frame(dark, "splash")

    result = RenderResult()
    if platform == "android":
        _render_android(light, dark, options, result)
    elif platform == "ios":
        _render_ios(light, dark, options, result)
    elif platform == "web":
        _render_web(light, dark, result)
    else:
        raise ValueError(f"unknown platform: {platform!r}")
    return result


def _scaled(art: Image.Image, density: float) -> Image.Image:
    """Resample to the size `width * density / 4` gives, as Dart truncated it."""

    return scale_to_fit(art, density_size(art.width, art.height, density)[0])


def _render_android(
    light: Image.Image,
    dark: Image.Image | None,
    options: SplashOptions,
    result: RenderResult,
) -> None:
    """Splash bitmaps per density, plus the Android 12 icon canvas.

    The `-night` variants are written only when a distinct dark image was
    supplied. When one is not, they are listed as stale so a build that used
    to have dark artwork does not keep serving it - cookiecutter overwrites
    but never deletes.
    """

    for directory, density in ANDROID_DENSITIES.items():
        result.add(
            f"{_ANDROID_RES}/drawable-{directory}/splash.png", _scaled(light, density)
        )
        result.add(
            f"{_ANDROID_RES}/drawable-{directory}/android12splash.png",
            _android_12(light, density, options.icon_background, options),
        )

    for directory, density in ANDROID_DENSITIES.items():
        night = f"{_ANDROID_RES}/drawable-night-{directory}"
        if dark is None:
            result.stale.extend((f"{night}/splash.png", f"{night}/android12splash.png"))
            continue
        result.add(f"{night}/splash.png", _scaled(dark, density))
        result.add(
            f"{night}/android12splash.png",
            _android_12(
                dark,
                density,
                options.icon_dark_background or options.icon_background,
                options,
            ),
        )

    result.stale.extend(_ANDROID_STALE)
    _warn_android_12_crop(light, options, result)


def _android_12(
    art: Image.Image,
    density: float,
    background: str | None,
    options: SplashOptions,
) -> Image.Image:
    """Fit artwork into the circle Android 12 guarantees is visible.

    This is the one place a source is deliberately reframed, and it is not an
    exception to the rule that a user's composition is theirs: the canvas is
    a platform-specified frame whose outer third is *always* cropped, so
    fitting honours the contract rather than re-deciding their padding.

    Artwork that already sits inside the circle is scaled to the whole canvas
    instead, so a user who followed the platform guidance and padded their
    own icon is not shrunk a second time.
    """

    dp = ANDROID_12_CANVAS_DP_WITH_BACKGROUND if background else ANDROID_12_CANVAS_DP
    canvas = round(dp * density)

    extent = alpha_extent(art)
    already_fits = extent is not None and extent <= ANDROID_12_VISIBLE_FRACTION
    if options.icon_fit == "none" or already_fits:
        scaled = scale_to_fit(art, canvas)
    else:
        scaled = scale_to_fit(art, round(canvas * ANDROID_12_VISIBLE_FRACTION))

    return place(scaled, canvas, bg=parse_hex_color(background) if background else None)


def _warn_android_12_crop(
    art: Image.Image, options: SplashOptions, result: RenderResult
) -> None:
    """Warn when passing artwork through will let the launcher crop it."""

    if options.icon_fit != "none":
        return
    extent = alpha_extent(art)
    if extent is None or extent > ANDROID_12_VISIBLE_FRACTION:
        result.warn(
            'splash icon_fit is "none", so the icon is not fitted to the '
            f"circle Android 12 crops it to. Artwork outside the central "
            f"{ANDROID_12_VISIBLE_FRACTION:.0%} will be cut off."
        )


def _render_ios(
    light: Image.Image,
    dark: Image.Image | None,
    options: SplashOptions,
    result: RenderResult,
) -> None:
    """Launch images at 1x/2x/3x, plus the two solid background swatches.

    Both the light and the dark set are always written, because the shipped
    `Contents.json` declares all six unconditionally. A missing file there is
    an asset-catalog error, not a silently absent image.
    """

    for suffix, density in IOS_SCALES.items():
        result.add(f"{_IOS_LAUNCH}/LaunchImage{suffix}.png", _scaled(light, density))
        result.add(
            f"{_IOS_LAUNCH}/LaunchImageDark{suffix}.png",
            _scaled(dark if dark is not None else light, density),
        )

    # A 1x1 PNG stretched by the storyboard. Kept in preference to a
    # `.colorset`, whose `<namedColor>` needs a newer `toolsVersion` than the
    # storyboard declares, and a storyboard that fails to compile breaks
    # every iOS build.
    result.add(f"{_IOS_BACKGROUND}/background.png", _swatch(options.color))
    result.add(
        f"{_IOS_BACKGROUND}/darkbackground.png",
        _swatch(options.dark_color if dark is not None else options.color),
    )


def _swatch(color: str) -> Image.Image:
    """A 1x1 opaque PNG of one colour."""

    return Image.new("RGB", (1, 1), parse_hex_color(color))


def _render_web(
    light: Image.Image, dark: Image.Image | None, result: RenderResult
) -> None:
    """Light and dark splash images at 1x through 4x.

    Always written as `.png`, whatever the source extension. FNS named these
    after the source, so a `.webp` icon produced a `<picture>` srcset
    pointing at files it had never written.
    """

    for name, density in WEB_SCALES.items():
        result.add(f"web/splash/img/light-{name}.png", _scaled(light, density))
        result.add(
            f"web/splash/img/dark-{name}.png",
            _scaled(dark if dark is not None else light, density),
        )
        # A previous build with a .webp source left these behind, and the
        # generated <picture> would still resolve them ahead of the .png.
        result.stale.extend(
            (f"web/splash/img/light-{name}.webp", f"web/splash/img/dark-{name}.webp")
        )
