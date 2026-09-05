"""Rendering app icons for each platform Flet builds for.

Pure: takes an image, returns images. Nothing here reads or writes the
filesystem, so the same code serves a build and a live preview.

The governing rule is that a user's icon is placed **full-bleed**. Its
internal padding is a design decision, and re-framing it would silently
change their artwork. Only transforms a platform actually requires are
applied - flattening where alpha is rejected, the macOS icon grid, a
multi-size `.ico`, opaque maskable icons.
"""

from __future__ import annotations

from PIL import Image

from ._imaging import (
    MACOS_TILE_RATIO,
    alpha_extent,
    apple_grid,
    looks_pre_shaped,
    place,
    scale_to_fit,
)
from ._models import AssetSpec, IconOptions, RenderResult, Target

__all__ = [
    "ANDROID_ADAPTIVE_SIZES",
    "ANDROID_MIPMAP_SIZES",
    "DEFAULT_SPECS",
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
                Target("web/icons/Icon-maskable-192.png", 192, opaque=True),
                Target("web/icons/Icon-maskable-512.png", 512, opaque=True),
                # flutter_launcher_icons never generated this, yet the
                # template's index.html links to it.
                Target("web/icons/apple-touch-icon-192.png", 192, opaque=True),
            ]
        ),
        "linux": AssetSpec(),
    }


DEFAULT_SPECS = _default_specs()
"""Per-platform defaults, matching a stock Flutter project."""


def render_icons(
    source: Image.Image,
    options: IconOptions | None = None,
    spec: AssetSpec | None = None,
    *,
    platform: str,
    pre_rendered: bool = False,
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

    if platform == "macos":
        _render_macos(source, options, spec, result, pre_rendered)
    elif platform == "linux":
        _render_linux(source, options, spec, result)
    else:
        for target in spec.targets:
            result.add(target.relative_path, _plain(source, target, options))

    if platform == "android":
        _warn_adaptive_safe_zone(source, result)
    if spec.ico_sizes:
        result.ico["windows/runner/resources/app_icon.ico"] = {
            size: _plain(source, Target("", size), options) for size in spec.ico_sizes
        }

    return result


def _plain(source: Image.Image, target: Target, options: IconOptions) -> Image.Image:
    """Full-bleed placement, flattened when the target rejects alpha."""

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
        result.add(target.relative_path, _plain(source, target, options))


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
        targets.append(Target(f"web/{src}", size, opaque=maskable))
    targets.append(Target("web/icons/apple-touch-icon-192.png", 192, opaque=True))
    return AssetSpec(targets=targets)
