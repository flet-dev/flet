"""Rendering app icons for each platform Flet builds for.

Pure: takes an image, returns images. Nothing here reads or writes the
filesystem, so the same code serves a build and a live preview.

Artwork the author framed for a platform is placed **full-bleed** and left
alone: its padding is a design decision, and re-framing it would silently
change their icon. Only transforms a platform actually requires are applied -
flattening where alpha is rejected, the macOS icon grid, a multi-size `.ico`,
opaque maskable icons.

A *generic* `icon.png` is different, because no single framing can satisfy
every platform: web, Windows and Linux apply no mask and want every pixel,
while iOS, macOS and Android each mask the edges away and need margin.
Rather than make the user choose which platform to serve, a generic source is
shrunk to each platform's margin - never enlarged, and never when the source
is opaque, since an opaque image is a finished icon rather than a glyph on a
canvas. See :data:`FRAMING` and the `derived` argument to
:func:`render_icons`.
"""

from __future__ import annotations

from PIL import Image

from ._imaging import (
    MACOS_TILE_RATIO,
    alpha_extent,
    apple_grid,
    looks_pre_shaped,
    place,
    radial_extent,
    scale_to_fit,
)
from ._models import AssetSpec, IconOptions, RenderResult, Target

__all__ = [
    "ANDROID_ADAPTIVE_SIZES",
    "ANDROID_MIPMAP_SIZES",
    "DEFAULT_SPECS",
    "FRAMING",
    "FRAMING_TOLERANCE",
    "LINUX_HICOLOR_SIZES",
    "WINDOWS_ICO_SIZES",
    "linux_targets",
    "render_icons",
]

# The fraction of an adaptive icon's foreground layer Android guarantees is
# visible; the rest can be cropped by the launcher's mask.
ADAPTIVE_SAFE_FRACTION = 72 / 108

ANDROID_MIPMAP_SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

ANDROID_ADAPTIVE_SIZES = {
    "drawable-mdpi": 108,
    "drawable-hdpi": 162,
    "drawable-xhdpi": 216,
    "drawable-xxhdpi": 324,
    "drawable-xxxhdpi": 432,
}

# Explorer, the taskbar and alt-tab each pick a different entry; shipping one
# 256 and letting Windows downscale is why single-entry icons look mushy.
WINDOWS_ICO_SIZES = (16, 32, 48, 256)

# Every size here is one the hicolor theme index declares. A file installed
# into an undeclared directory is never found, and a file whose pixels do not
# match the directory it sits in is scaled wrongly by the icon cache.
LINUX_HICOLOR_SIZES = (16, 24, 32, 48, 64, 128, 256, 512)

_IOS_ICONS = {
    "Icon-App-20x20@1x.png": 20,
    "Icon-App-20x20@2x.png": 40,
    "Icon-App-20x20@3x.png": 60,
    "Icon-App-29x29@1x.png": 29,
    "Icon-App-29x29@2x.png": 58,
    "Icon-App-29x29@3x.png": 87,
    "Icon-App-40x40@1x.png": 40,
    "Icon-App-40x40@2x.png": 80,
    "Icon-App-40x40@3x.png": 120,
    "Icon-App-60x60@2x.png": 120,
    "Icon-App-60x60@3x.png": 180,
    "Icon-App-76x76@1x.png": 76,
    "Icon-App-76x76@2x.png": 152,
    "Icon-App-83.5x83.5@2x.png": 167,
    "Icon-App-1024x1024@1x.png": 1024,
}

_MACOS_ICONS = {f"app_icon_{s}.png": s for s in (16, 32, 64, 128, 256, 512, 1024)}

_IOS_DIR = "ios/Runner/Assets.xcassets/AppIcon.appiconset"
_MACOS_DIR = "macos/Runner/Assets.xcassets/AppIcon.appiconset"
_ANDROID_RES = "android/app/src/main/res"


def _default_specs() -> dict[str, AssetSpec]:
    """The stock Flutter project layout, used when no project is on hand."""

    return {
        # iOS rejects an alpha channel in the marketing icon, and Apple's
        # review tooling checks it, so every entry is flattened.
        "ios": AssetSpec(
            targets=[
                Target(f"{_IOS_DIR}/{name}", size, opaque=True)
                for name, size in _IOS_ICONS.items()
            ]
        ),
        "macos": AssetSpec(
            targets=[
                Target(f"{_MACOS_DIR}/{name}", size)
                for name, size in _MACOS_ICONS.items()
            ]
        ),
        "android": AssetSpec(
            targets=[
                Target(f"{_ANDROID_RES}/{d}/ic_launcher.png", s)
                for d, s in ANDROID_MIPMAP_SIZES.items()
            ]
            + [
                Target(f"{_ANDROID_RES}/{d}/ic_launcher_foreground.png", s)
                for d, s in ANDROID_ADAPTIVE_SIZES.items()
            ]
        ),
        "windows": AssetSpec(ico_sizes=WINDOWS_ICO_SIZES),
        "web": AssetSpec(
            targets=[
                Target("web/favicon.png", 32),
                Target("web/icons/Icon-192.png", 192),
                Target("web/icons/Icon-512.png", 512),
                # Maskable icons are cropped to an arbitrary shape by the
                # launcher and must be opaque; a transparent one renders with
                # black corners on some Android launchers.
                Target(
                    "web/icons/Icon-maskable-192.png",
                    192,
                    opaque=True,
                    frame="maskable",
                ),
                Target(
                    "web/icons/Icon-maskable-512.png",
                    512,
                    opaque=True,
                    frame="maskable",
                ),
                # flutter_launcher_icons never generated this, yet the
                # template's index.html links to it.
                Target(
                    "web/icons/apple-touch-icon-192.png",
                    192,
                    opaque=True,
                    frame="apple-touch",
                ),
            ]
        ),
        "linux": AssetSpec(),
    }


DEFAULT_SPECS = _default_specs()
"""Per-platform defaults, matching a stock Flutter project."""

# How much of its canvas the artwork may occupy when a generic `icon.png` is
# derived for a platform that frames its icons. A single source cannot satisfy
# all of them - the flat surfaces want every pixel, and these three want
# margin - so the margin is computed here rather than demanded of the user.
#
# Android is measured radially because its mask is a circle: artwork whose
# extremes sit off-axis clears the axis test and is still clipped. 0.567 puts
# the furthest point at 85% of the mask radius.
FRAMING = {
    "ios": (0.60, alpha_extent),
    "macos": (0.68, alpha_extent),
    "android": (0.567, radial_extent),
    # Per-target rules, for files whose mask differs from their platform's.
    # A maskable icon's safe zone is defined by spec as a circle 80% of the
    # icon's width, so the artwork's furthest point may reach 0.80 of half the
    # canvas. An apple-touch icon becomes an iOS home-screen icon, so it is
    # framed exactly like the native one.
    "maskable": (0.80, radial_extent),
    "apple-touch": (0.60, alpha_extent),
}

# Resampling lands the measured extent a hair either side of the target, so an
# exact comparison would shrink an already-framed icon a second time on every
# pass. The slack makes framing idempotent, and skips a resample - which is
# lossy at the soft edge - for artwork that is already close enough.
FRAMING_TOLERANCE = 1.02


def render_icons(
    source: Image.Image,
    options: IconOptions | None = None,
    spec: AssetSpec | None = None,
    *,
    platform: str,
    pre_rendered: bool = False,
    derived: bool = False,
) -> RenderResult:
    """Render every app icon for one platform.

    Args:
        source: The normalised `RGBA` source, from
            :func:`~flet_platform_assets.load_source`.
        options: Rendering options; defaults are used when omitted.
        spec: Which files to produce. Defaults to the stock Flutter layout,
            so a caller with no project on disk still gets output.
        platform: One of `ios`, `macos`, `android`, `windows`, `web`, `linux`.
        pre_rendered: The source already carries platform shaping, so the
            macOS grid is skipped rather than applied a second time.
        derived: The source is a generic `icon.png` rather than artwork
            authored for this platform, so it may be framed to suit the
            platform's mask - see :data:`FRAMING`. An icon supplied *as*
            `icon_<platform>.png` is the author's finished composition and is
            never reframed.

    Returns:
        The rendered assets and any diagnostics.

    Raises:
        ValueError: If `platform` is not recognised.
    """

    options = options or IconOptions()
    if platform not in DEFAULT_SPECS:
        raise ValueError(f"unknown platform: {platform!r}")
    spec = spec if spec is not None else DEFAULT_SPECS[platform]
    result = RenderResult()
    supplied = max(source.size)
    if derived:
        source = _frame(source, platform)

    if platform == "macos":
        _render_macos(source, options, spec, result, pre_rendered)
    elif platform == "linux":
        _render_linux(source, options, spec, result, derived)
    else:
        for target in spec.targets:
            result.add(target.relative_path, _plain(source, target, options, derived))

    if platform == "android":
        _warn_adaptive_safe_zone(source, result)
    if platform == "web":
        _warn_maskable_safe_zone(source, spec, result, derived)
    if spec.ico_sizes:
        result.ico["windows/runner/resources/app_icon.ico"] = {
            size: _plain(source, Target("", size), options) for size in spec.ico_sizes
        }

    _warn_low_resolution(supplied, result)
    return result


def _warn_low_resolution(supplied: int, result: RenderResult) -> None:
    """Warn when the source is smaller than the largest icon being made.

    Measured against what was actually produced rather than a fixed number,
    because each platform's largest differs - 1024 for iOS and macOS, 512 for
    the web, 256 for a Windows `.ico`. A source that is perfectly adequate for
    one is enlarged for another, and an enlarged icon is soft in exactly the
    place it is looked at most: Apple's 1024px marketing icon is what the App
    Store listing shows.

    Args:
        supplied: Longest side of the source, before any framing.
        result: The render to attach the warning to, and to measure.
    """

    produced = max(
        (asset.image.width for asset in result.assets),
        default=0,
    )
    for sizes in result.ico.values():
        produced = max(produced, max(sizes, default=0))
    if not produced or supplied >= produced:
        return
    result.warn(
        f"icon source is {supplied}px, but this platform needs one up to "
        f"{produced}px. The larger sizes are enlarged from it and will look "
        f"soft. Supply at least {produced}x{produced}."
    )


def _frame(source: Image.Image, rule: str) -> Image.Image:
    """Shrink artwork to the margin a platform's mask needs, never enlarging.

    Only shrinking makes this idempotent and safe to apply to anything: a
    full-bleed source is brought in, artwork that already clears the mask is
    untouched, and running it twice changes nothing.

    A fully opaque source is left alone. `alpha_extent` and
    :func:`~._imaging.radial_extent` both return `None` for one, which is the
    right answer rather than a missing measurement: an opaque image is a
    finished icon, not a glyph floating on a canvas, and shrinking it would
    ring a complete composition with a border of background colour.
    """

    framing = FRAMING.get(rule)
    if framing is None:
        return source
    target, measure = framing
    current = measure(source)
    if current is None or current <= target * FRAMING_TOLERANCE:
        return source
    # Measured against the longest side, so scaled and re-centred against it
    # too. Using the width would square a portrait source to its short edge
    # and land the radial rules short of their target.
    side = max(source.size)
    art = scale_to_fit(source, max(1, round(side * target / current)))
    return place(art, side)


def _plain(
    source: Image.Image,
    target: Target,
    options: IconOptions,
    derived: bool = False,
) -> Image.Image:
    """Full-bleed placement, flattened when the target rejects alpha."""

    if derived and target.frame:
        source = _frame(source, target.frame)
    art = scale_to_fit(source, target.size)
    return place(
        art,
        target.size,
        bg=options.background if target.opaque else None,
    )


def _render_macos(
    source: Image.Image,
    options: IconOptions,
    spec: AssetSpec,
    result: RenderResult,
    pre_rendered: bool,
) -> None:
    """Compose the Apple icon grid once, then downscale it.

    This is the one place chained downscaling is right: the tile, artwork and
    shadow have to shrink together, so smaller sizes are reductions of a
    single composition rather than separate compositions.
    """

    if options.macos_style not in ("auto", "grid", "raw"):
        raise ValueError(f"unknown macos_style: {options.macos_style!r}")

    detected = options.macos_style == "auto" and (
        pre_rendered or looks_pre_shaped(source)
    )
    if options.macos_style == "raw" or detected:
        if detected and not pre_rendered:
            result.warn(
                "macOS icon source already looks like a shaped icon - a filled, "
                "near-square tile with its corners cut away - so it was placed "
                "as-is instead of having the icon grid applied on top. Set "
                'macos.icon_style = "grid" to apply it anyway.'
            )
        # No `derived` here: macOS targets declare no per-target framing, and
        # the source was already framed for the platform before dispatch.
        for target in spec.targets:
            result.add(target.relative_path, _plain(source, target, options))
        return

    largest = max((t.size for t in spec.targets), default=1024)
    art = scale_to_fit(source, round(largest * MACOS_TILE_RATIO))
    composed = apple_grid(art, largest, tile_color=options.background)
    for target in spec.targets:
        image = (
            composed
            if target.size == largest
            else composed.resize((target.size, target.size), Image.LANCZOS)
        )
        result.add(target.relative_path, image)


def _render_linux(
    source: Image.Image,
    options: IconOptions,
    spec: AssetSpec,
    result: RenderResult,
    derived: bool = False,
) -> None:
    """Produce the freedesktop hicolor tree plus the runner's window icon.

    flutter_launcher_icons has no Linux generator at all, so `flet build`
    previously installed a single file - often a 1024px image - into
    `hicolor/256x256/`. A directory that claims one size while holding
    another is scaled wrongly by the icon cache, and small panel sizes were
    downscaled from it every time.
    """

    targets = spec.targets or linux_targets(options.application_id).targets
    for target in targets:
        result.add(target.relative_path, _plain(source, target, options, derived))


def _warn_adaptive_safe_zone(source: Image.Image, result: RenderResult) -> None:
    """Warn when an adaptive icon's artwork will be cropped by the launcher.

    Only meaningful for artwork with transparency: a fully opaque square
    reaches every edge by definition, so warning about it would fire on every
    build and mean nothing.
    """

    extent = alpha_extent(source)
    if extent is None or extent <= ADAPTIVE_SAFE_FRACTION:
        return
    result.warn(
        f"icon artwork reaches {extent:.0%} of the canvas, but Android only "
        f"guarantees the central {ADAPTIVE_SAFE_FRACTION:.0%} of an adaptive "
        "icon is visible. Add padding around the artwork, or a circular "
        "launcher mask will clip it."
    )


def linux_targets(application_id: str) -> AssetSpec:
    """Build the Linux target list for one application id.

    The hicolor tree is named after the desktop entry id, so unlike every
    other platform the file names are not fixed and cannot live in
    :data:`DEFAULT_SPECS`. Callers that need the list up front - to check
    whether a previous build's output is still present, say - build it here
    rather than re-deriving the naming rule.

    Args:
        application_id: The desktop entry id, e.g. `com.example.app`.

    Returns:
        A spec covering every hicolor size plus the runner's window icon.
    """

    return AssetSpec(
        targets=[
            Target(f"linux/icons/hicolor/{s}x{s}/apps/{application_id}.png", s)
            for s in LINUX_HICOLOR_SIZES
        ]
        # The GTK runner loads this one directly to set the window icon.
        + [Target("linux/app_icon.png", 256)]
    )


def _warn_maskable_safe_zone(
    source: Image.Image,
    spec: AssetSpec,
    result: RenderResult,
    derived: bool,
) -> None:
    """Warn when a maskable icon's artwork will be cropped by the installer.

    Only for artwork supplied as `icon_web.png`: a generic source has already
    been fitted, and framing an explicit one would overrule a composition the
    author made deliberately. Silence is the wrong answer either way, because
    unlike the other web icons this cropping is certain rather than possible.

    Opaque artwork is not warned about. Filling the frame is what a maskable
    icon is supposed to do - the colour bleeds past the mask on purpose, and
    keeping the glyph inside the safe zone is then the author's business.
    """

    if derived or not any(t.frame == "maskable" for t in spec.targets):
        return
    limit, measure = FRAMING["maskable"]
    extent = measure(source)
    if extent is None or extent <= limit * FRAMING_TOLERANCE:
        return
    # Both figures are diameters as a fraction of the icon's width, so they
    # compare directly: `radial_extent` is already normalised to half the
    # canvas, which makes it the enclosing circle's diameter over the width.
    result.warn(
        f"icon artwork spans {extent:.0%} of its width, but a maskable web "
        f"icon is cropped to a circle {limit:.0%} of that. The edges will be "
        "cut off. Pad the artwork, or supply it as icon.png rather than "
        "icon_web.png and Flet will fit it for you."
    )


def web_targets_from_manifest(manifest: dict, favicon_size: int = 32) -> AssetSpec:
    """Build a web spec from a rendered project's `manifest.json`.

    The manifest is the project's own declaration of which icons it uses, so
    following it means never writing a file nothing references.

    Args:
        manifest: The parsed `manifest.json`.
        favicon_size: Size for `web/favicon.png`, which the manifest does not
            declare.

    Returns:
        A spec covering the favicon, every manifest entry, and the
            apple-touch icon.
    """

    targets = [Target("web/favicon.png", favicon_size)]
    for entry in manifest.get("icons", []):
        src = entry.get("src")
        sizes = entry.get("sizes", "")
        if not src or "x" not in sizes:
            continue
        try:
            size = int(sizes.split("x")[0])
        except ValueError:
            continue
        maskable = "maskable" in entry.get("purpose", "")
        targets.append(
            Target(
                f"web/{src}",
                size,
                opaque=maskable,
                frame="maskable" if maskable else None,
            )
        )
    targets.append(
        Target(
            "web/icons/apple-touch-icon-192.png",
            192,
            opaque=True,
            frame="apple-touch",
        )
    )
    return AssetSpec(targets=targets)
