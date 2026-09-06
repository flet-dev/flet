# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pillow==12.1.1",
# ]
# ///
"""Render the icon illustrations used by `website/docs/publish/index.md`.

Run from the repo root:

    uv run .github/scripts/generate_icon_docs_images.py
    uv run .github/scripts/generate_icon_docs_images.py --verify

Every image is produced by the same `flet_platform_assets` calls `flet build`
makes, so the documentation cannot claim one thing while the generator does
another. The doc quotes specific numbers - 60% for iOS, 80% for a maskable
icon - and these are what those numbers actually look like.

Masks are drawn here rather than left to the reader's imagination: a launcher
crops an Android icon to a circle and a maskable icon to whatever shape the
installing platform picks, and neither is visible in the file on disk.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "sdk/python/packages/flet-platform-assets/src"))
from flet_platform_assets import (  # noqa: E402
    FRAMING,
    IconOptions,
    render_icons,
)
from flet_platform_assets._imaging import (  # noqa: E402
    scale_to_height,
    superellipse_mask,
)

OUT = REPO / "website/static/img/docs/icons"
MASTER = REPO / "media/logo/flet-icon-1024.png"

BRAND = (255, 0, 85)
TILE = 256  # every illustration is square and this wide

# A soft checkerboard, so "transparent" reads as transparent rather than white.
CHECKER_LIGHT = (245, 243, 244)
CHECKER_DARK = (226, 221, 225)
CHECKER_SQUARE = 16


def mark() -> Image.Image:
    """The Flet mark, cropped to its own bounds."""
    master = Image.open(MASTER).convert("RGBA")
    return master.crop(master.getchannel("A").getbbox())


def source(height_frac: float, *, opaque: bool = False) -> Image.Image:
    """A 1024px source icon with the mark at a given fraction of the height.

    Args:
        height_frac: Mark height as a fraction of the canvas.
        opaque: Fill the canvas with the brand colour and draw the mark in
            white, producing finished artwork rather than a bare glyph.

    Returns:
        A 1024x1024 `RGBA` source.
    """

    art = mark()
    if opaque:
        white = Image.new("RGBA", art.size, (255, 255, 255, 255))
        white.putalpha(art.getchannel("A"))
        art = white
    canvas = Image.new("RGBA", (1024, 1024), (*BRAND, 255) if opaque else (0, 0, 0, 0))
    scaled = scale_to_height(art, round(1024 * height_frac))
    canvas.alpha_composite(
        scaled, ((1024 - scaled.width) // 2, (1024 - scaled.height) // 2)
    )
    return canvas


def checkerboard(size: int) -> Image.Image:
    """A square of alternating light squares, to sit behind transparency."""

    board = Image.new("RGBA", (size, size), (*CHECKER_LIGHT, 255))
    draw = ImageDraw.Draw(board)
    for y in range(0, size, CHECKER_SQUARE):
        for x in range(0, size, CHECKER_SQUARE):
            if (x // CHECKER_SQUARE + y // CHECKER_SQUARE) % 2:
                draw.rectangle(
                    (x, y, x + CHECKER_SQUARE - 1, y + CHECKER_SQUARE - 1),
                    fill=(*CHECKER_DARK, 255),
                )
    return board


def on_checkerboard(img: Image.Image) -> Image.Image:
    """Composite onto a checkerboard so transparent areas are legible."""

    board = checkerboard(TILE)
    board.alpha_composite(img.convert("RGBA").resize((TILE, TILE), Image.LANCZOS))
    return board


def circle_masked(img: Image.Image, backdrop: tuple[int, int, int]) -> Image.Image:
    """Crop to a circle, as an Android launcher does."""

    img = img.convert("RGBA").resize((TILE, TILE), Image.LANCZOS)
    plate = Image.new("RGBA", (TILE, TILE), (*backdrop, 255))
    plate.alpha_composite(img)
    circle = Image.new("L", (TILE, TILE), 0)
    ImageDraw.Draw(circle).ellipse((0, 0, TILE - 1, TILE - 1), fill=255)
    out = checkerboard(TILE)
    out.paste(plate, (0, 0), circle)
    return out


def rounded(img: Image.Image) -> Image.Image:
    """Round the corners, approximating the iOS home-screen mask."""

    img = img.convert("RGBA").resize((TILE, TILE), Image.LANCZOS)
    img.putalpha(superellipse_mask(TILE, 5.0))
    out = checkerboard(TILE)
    out.alpha_composite(img)
    return out


def android_foreground(src: Image.Image, derived: bool) -> Image.Image:
    """The adaptive foreground layer, cropped to what the launcher shows."""

    layer = next(
        a.image
        for a in render_icons(
            src, IconOptions(), platform="android", derived=derived
        ).assets
        if "xxxhdpi/ic_launcher_foreground" in a.relative_path
    )
    side = layer.width
    visible = round(side * 72 / 108)
    inset = (side - visible) // 2
    return layer.crop((inset, inset, inset + visible, inset + visible))


def web(src: Image.Image, name: str, derived: bool) -> Image.Image:
    """One rendered web icon by file name."""

    return next(
        a.image
        for a in render_icons(src, IconOptions(), platform="web", derived=derived).assets
        if a.relative_path.endswith(name)
    )


def platform_icon(src: Image.Image, platform: str, name: str, derived: bool):
    """One rendered icon for a native platform, by file name fragment."""

    return next(
        a.image
        for a in render_icons(
            src, IconOptions(), platform=platform, derived=derived
        ).assets
        if name in a.relative_path
    )


def safe_zone_overlay(src: Image.Image, fraction: float) -> Image.Image:
    """Show what a circular mask keeps and what it removes.

    Args:
        src: The rendered icon.
        fraction: Safe circle diameter as a fraction of the width.

    Returns:
        The icon with the area outside the circle dimmed and the circle drawn.
    """

    img = src.convert("RGBA").resize((TILE, TILE), Image.LANCZOS)
    out = Image.new("RGBA", (TILE, TILE), (255, 255, 255, 255))
    out.alpha_composite(img)
    # Dim everything the mask discards.
    veil = Image.new("RGBA", (TILE, TILE), (255, 255, 255, 190))
    keep = Image.new("L", (TILE, TILE), 255)
    radius = TILE * fraction / 2
    centre = TILE / 2
    ImageDraw.Draw(keep).ellipse(
        (centre - radius, centre - radius, centre + radius, centre + radius), fill=0
    )
    out.paste(veil, (0, 0), keep)
    ImageDraw.Draw(out).ellipse(
        (centre - radius, centre - radius, centre + radius, centre + radius),
        outline=(*BRAND, 255),
        width=3,
    )
    return out


def build() -> dict[str, Image.Image]:
    """Every illustration, keyed by file name."""

    full_bleed = source(1.0)
    padded = source(0.60)
    opaque = source(0.58, opaque=True)

    images = {
        # The three shapes a source can take.
        "source-full-bleed.png": on_checkerboard(full_bleed),
        "source-padded.png": on_checkerboard(padded),
        "source-opaque.png": on_checkerboard(opaque),
        # What one full-bleed source becomes on each platform.
        "result-favicon.png": on_checkerboard(web(full_bleed, "favicon.png", True)),
        "result-ios.png": rounded(
            platform_icon(full_bleed, "ios", "1024x1024", True)
        ),
        "result-macos.png": on_checkerboard(
            platform_icon(full_bleed, "macos", "app_icon_1024", True)
        ),
        "result-android.png": circle_masked(
            android_foreground(full_bleed, True), (255, 255, 255)
        ),
        "result-maskable.png": on_checkerboard(
            web(full_bleed, "Icon-maskable-512.png", True)
        ),
        # Framed versus used as supplied.
        "framing-derived.png": on_checkerboard(
            platform_icon(full_bleed, "macos", "app_icon_1024", True)
        ),
        "framing-explicit.png": on_checkerboard(
            platform_icon(full_bleed, "macos", "app_icon_1024", False)
        ),
        # Opaque artwork is never reframed, on any platform.
        "opaque-android.png": circle_masked(
            android_foreground(opaque, True), (255, 255, 255)
        ),
        "opaque-ios.png": rounded(platform_icon(opaque, "ios", "1024x1024", True)),
        # The maskable safe zone, with the crop made visible.
        "maskable-fitted.png": safe_zone_overlay(
            web(full_bleed, "Icon-maskable-512.png", True), FRAMING["maskable"][0]
        ),
        "maskable-cropped.png": safe_zone_overlay(
            web(full_bleed, "Icon-maskable-512.png", False), FRAMING["maskable"][0]
        ),
    }
    return images


def main() -> int:
    """Write the illustrations, or check the committed ones are current."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify", action="store_true", help="fail if any file is missing or stale"
    )
    args = parser.parse_args()

    images = build()
    OUT.mkdir(parents=True, exist_ok=True)
    failures = 0
    for name, image in images.items():
        path = OUT / name
        if args.verify:
            if not path.is_file():
                print(f"missing: {name}")
                failures += 1
                continue
            with Image.open(path) as existing:
                if existing.convert("RGBA").tobytes() != image.convert("RGBA").tobytes():
                    print(f"stale: {name}")
                    failures += 1
        else:
            image.save(path, format="PNG", optimize=True)

    if args.verify:
        print(f"{failures} failure(s)")
        return 1 if failures else 0
    print(f"wrote {len(images)} illustrations to {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
