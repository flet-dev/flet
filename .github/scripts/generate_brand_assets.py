# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pillow==12.1.1",
#   "numpy",
# ]
# ///
"""Derive every Flet brand raster from the masters in `media/logo/`.

Run from the repo root:

    uv run .github/scripts/generate_brand_assets.py
    uv run .github/scripts/generate_brand_assets.py --verify
    uv run .github/scripts/generate_brand_assets.py --contact-sheet out.png

Everything is derived from `media/logo/flet-icon-1024.png` (rasters) and
`media/logo/logo-symbol.svg` (the two SVG destinations). The master's own
padding is never trusted: it is cropped to its tight alpha bounding box and
re-framed to an explicit fraction per variant, so a future rebrand only needs
new masters dropped in and this script re-run.

Two rules the compose helper enforces, both of which the previous hand-made
assets violated:

* Every output is resampled from the full-resolution mark in one step. Chained
  downscaling (192 -> 144 -> 96) is what made the old mipmaps mushy.
* `Image.resize(..., LANCZOS)`, never `Image.thumbnail`, whose default
  `reducing_gap=2.0` does a two-step reduce that softens small sizes.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

REPO = Path(__file__).resolve().parents[2]
LOGO_DIR = REPO / "media" / "logo"
MASTER = LOGO_DIR / "flet-icon-1024.png"
SYMBOL_SVG = LOGO_DIR / "logo-symbol.svg"

TEMPLATE_BUILD = REPO / "sdk/python/templates/build/{{cookiecutter.out_dir}}"
TEMPLATE_APP = REPO / "sdk/python/templates/app/app/{{cookiecutter.out_dir}}"
CLIENT = REPO / "client"
EXAMPLES = REPO / "sdk/python/examples"
INTEGRATION = REPO / "sdk/python/packages/flet/integration_tests"
WEB_STATIC = REPO / "website/static/img"

# Flatten background for icons that must not carry alpha (iOS, maskable,
# apple-touch). Matches the existing assets and the template's
# `adaptive_icon_background`.
BRAND_BG = (255, 255, 255)

# Android's adaptive-icon foreground guarantees only the central 66.67% is
# visible, and the Android 12 splash clips to a circle of the same ratio.
# 0.60 sits inside both with margin and matches the iOS/web framing, so one
# number drives every derived output.
GLYPH_FRAC = 0.60
# `client/` ships legacy launcher icons only - no mipmap-anydpi-v26, no
# foreground/background layers - so the adaptive-icon safe zone does not apply
# to it and GLYPH_FRAC would render visibly smaller than neighbouring apps.
# This preserves the framing the hand-made client icons used.
CLIENT_ANDROID_FRAC = 0.88
# Favicons and .ico entries are tiny; padding there just wastes pixels.
TIGHT_FRAC = 0.94
# apple-touch-icon is composited by iOS onto a rounded tile with its own inset.
APPLE_TOUCH_FRAC = 0.729
LOADING_FRAC = 0.88

# macOS icon grid: an 824x824 tile inset in a 1024 canvas, plus a drop shadow.
MACOS_TILE = 824 / 1024
MACOS_GLYPH_FRAC = 0.55
# Apple's corner is a continuous-curvature squircle; a plain rounded rectangle
# reads visibly wrong next to system icons.
SQUIRCLE_N = 5.0

# Web PWA "any" icons sit on a white tile inset slightly from the canvas edge.
WEB_TILE_INSET = 0.953
WEB_TILE_N = 4.0

IOS_SIZES = {
    "Icon-App-20x20@1x.png": 20,
    "Icon-App-20x20@2x.png": 40,
    "Icon-App-20x20@3x.png": 60,
    "Icon-App-29x29@1x.png": 29,
    "Icon-App-29x29@2x.png": 58,
    "Icon-App-29x29@3x.png": 87,
    "Icon-App-40x40@1x.png": 40,
    "Icon-App-40x40@2x.png": 80,
    "Icon-App-40x40@3x.png": 120,
    "Icon-App-50x50@1x.png": 50,
    "Icon-App-50x50@2x.png": 100,
    "Icon-App-57x57@1x.png": 57,
    "Icon-App-57x57@2x.png": 114,
    "Icon-App-60x60@2x.png": 120,
    "Icon-App-60x60@3x.png": 180,
    "Icon-App-72x72@1x.png": 72,
    "Icon-App-72x72@2x.png": 144,
    "Icon-App-76x76@1x.png": 76,
    "Icon-App-76x76@2x.png": 152,
    "Icon-App-83.5x83.5@2x.png": 167,
    "Icon-App-1024x1024@1x.png": 1024,
}
# The build template ships a subset; `client/` carries six extra legacy names
# that its Contents.json no longer references but that are still committed.
TEMPLATE_IOS_NAMES = [
    n
    for n in IOS_SIZES
    if not n.startswith(("Icon-App-50x50", "Icon-App-57x57", "Icon-App-72x72"))
]

MIPMAP_SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

MACOS_SIZES = [16, 32, 64, 128, 256, 512, 1024]


# --------------------------------------------------------------------------
# mark handling
# --------------------------------------------------------------------------


def load_mark() -> Image.Image:
    """The master cropped to its tight alpha bounding box."""
    master = Image.open(MASTER).convert("RGBA")
    bbox = master.getchannel("A").getbbox()
    if bbox is None:
        raise SystemExit(f"{MASTER} is fully transparent")
    return master.crop(bbox)


MARK: Image.Image = load_mark()


def _scaled(height: int) -> Image.Image:
    """The mark at a given pixel height, resampled from the master in one step."""
    width = max(1, round(MARK.width * height / MARK.height))
    return MARK.resize((width, max(1, height)), Image.LANCZOS)


def _superellipse(size: int, n: float, supersample: int = 4) -> Image.Image:
    """An `L`-mode mask of a superellipse, antialiased by rendering large."""
    t = size * supersample
    yy, xx = np.mgrid[0:t, 0:t]
    u = (2 * xx - (t - 1)) / (t - 1)
    v = (2 * yy - (t - 1)) / (t - 1)
    inside = (np.abs(u) ** n + np.abs(v) ** n) <= 1.0
    mask = Image.fromarray((inside * 255).astype(np.uint8), mode="L")
    return mask.resize((size, size), Image.LANCZOS)


def compose(
    canvas: int,
    *,
    h_frac: float,
    bg: tuple[int, int, int] | None = None,
    tile: float | None = None,
    tile_n: float = WEB_TILE_N,
    offset: tuple[int, int] = (0, 0),
) -> Image.Image:
    """Place the mark on a canvas at an explicit height fraction.

    `bg` flattens onto a solid full-bleed colour and returns mode RGB.
    `tile` draws a white superellipse tile at that fraction of the canvas,
    leaving the area outside it transparent.
    """
    glyph = _scaled(max(1, round(canvas * h_frac)))

    if bg is not None:
        out = Image.new("RGB", (canvas, canvas), bg)
    else:
        out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
        if tile is not None:
            side = round(canvas * tile)
            mask = _superellipse(side, tile_n)
            plate = Image.new("RGBA", (side, side), (*BRAND_BG, 255))
            plate.putalpha(mask)
            pos = ((canvas - side) // 2, (canvas - side) // 2)
            out.alpha_composite(plate, pos)

    x = (canvas - glyph.width) // 2 + offset[0]
    y = (canvas - glyph.height) // 2 + offset[1]
    if bg is not None:
        out.paste(glyph, (x, y), glyph)
    else:
        out.alpha_composite(glyph, (x, y))
    return out


def compose_macos(canvas: int = 1024) -> Image.Image:
    """The macOS squircle tile with a drop shadow, composed once at 1024.

    This is the one place chained downscaling is correct: the tile, glyph and
    shadow must scale together, so smaller sizes are reductions of this
    composition rather than independent compositions.
    """
    side = round(canvas * MACOS_TILE)
    mask = _superellipse(side, SQUIRCLE_N)

    tile = Image.new("RGBA", (side, side), (*BRAND_BG, 255))
    glyph = _scaled(round(canvas * MACOS_GLYPH_FRAC))
    tile.alpha_composite(glyph, ((side - glyph.width) // 2, (side - glyph.height) // 2))
    tile.putalpha(mask)

    pos = ((canvas - side) // 2, (canvas - side) // 2)

    # Shadow: the tile silhouette, blurred, offset down, at ~25% black.
    # blur=11/dy=8 reproduces the spread of the previous hand-made asset
    # (alpha bbox 874 vs 870, L75/T83/B67 vs L77/T87/B67).
    shadow = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    silhouette = Image.new("RGBA", (side, side), (0, 0, 0, 64))
    silhouette.putalpha(mask.point(lambda v: v * 64 // 255))
    shadow.alpha_composite(silhouette, (pos[0], pos[1] + 8))
    shadow = shadow.filter(ImageFilter.GaussianBlur(11))

    out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    out.alpha_composite(shadow)
    out.alpha_composite(tile, pos)
    return out


def save_png(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG", optimize=True)


def save_ico(path: Path, sizes: list[int]) -> None:
    """Write a multi-size ICO with an explicit image for every entry.

    Pillow's ICO writer silently drops any requested size larger than the base
    image, and its fallback path reuses a leaked loop variable when a size has
    no exact match. Supplying every size explicitly avoids both.
    """
    images = {s: compose(s, h_frac=TIGHT_FRAC) for s in sizes}
    base = images[max(sizes)]
    path.parent.mkdir(parents=True, exist_ok=True)
    base.save(
        path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=[images[s] for s in sorted(sizes) if s != max(sizes)],
    )


# --------------------------------------------------------------------------
# manifest
# --------------------------------------------------------------------------


def build_manifest() -> list[tuple[str, Path, dict]]:
    """(variant, destination, kwargs) for every generated file."""
    m: list[tuple[str, Path, dict]] = []

    def glyph(size: int, *dests: Path) -> None:
        for d in dests:
            m.append(("glyph", d, {"canvas": size, "h_frac": GLYPH_FRAC}))

    def tight(size: int, *dests: Path) -> None:
        for d in dests:
            m.append(("glyph-tight", d, {"canvas": size, "h_frac": TIGHT_FRAC}))

    def tile_safe(size: int, *dests: Path) -> None:
        for d in dests:
            m.append(
                ("tile-safe", d, {"canvas": size, "h_frac": GLYPH_FRAC, "bg": BRAND_BG})
            )

    # --- masters consumed by flutter_launcher_icons -----------------------
    glyph(1024, CLIENT / "assets/icon/flet-ios-1024.png")
    m.append(
        (
            "glyph",
            CLIENT / "assets/icon/flet-android-192.png",
            {"canvas": 192, "h_frac": CLIENT_ANDROID_FRAC},
        )
    )
    glyph(
        1024,
        TEMPLATE_BUILD / "images/icon.png",
        TEMPLATE_APP / "src/assets/icon.png",
        EXAMPLES / "apps/counter_test_ios/assets/icon.png",
    )

    # --- Android launcher icons ------------------------------------------
    for folder, size in MIPMAP_SIZES.items():
        # The client ships legacy launcher icons only, so it is framed larger
        # than the template default (see CLIENT_ANDROID_FRAC).
        m.append(
            (
                "glyph",
                CLIENT / f"android/app/src/main/res/{folder}/ic_launcher.png",
                {"canvas": size, "h_frac": CLIENT_ANDROID_FRAC},
            )
        )
        glyph(
            size, TEMPLATE_BUILD / f"android/app/src/main/res/{folder}/ic_launcher.png"
        )

    # --- iOS: no alpha, flattened onto the brand background ---------------
    client_ios = CLIENT / "ios/Runner/Assets.xcassets/AppIcon.appiconset"
    template_ios = TEMPLATE_BUILD / "ios/Runner/Assets.xcassets/AppIcon.appiconset"
    for name, size in IOS_SIZES.items():
        tile_safe(size, client_ios / name)
    for name in TEMPLATE_IOS_NAMES:
        tile_safe(IOS_SIZES[name], template_ios / name)

    # --- macOS squircle ---------------------------------------------------
    for size in MACOS_SIZES:
        for base in (
            CLIENT / "macos/Runner/Assets.xcassets/AppIcon.appiconset",
            TEMPLATE_BUILD / "macos/Runner/Assets.xcassets/AppIcon.appiconset",
        ):
            m.append(("macos", base / f"app_icon_{size}.png", {"canvas": size}))

    # --- web --------------------------------------------------------------
    tight(32, CLIENT / "web/favicon.png", TEMPLATE_BUILD / "web/favicon.png")
    tight(48, TEMPLATE_BUILD / "images/favicon.png")
    tight(48, EXAMPLES / "apps/counter_test_ios/assets/favicon.png")

    for size in (192, 512):
        for dest in (
            CLIENT / f"web/icons/icon-{size}.png",
            TEMPLATE_BUILD / f"web/icons/Icon-{size}.png",
        ):
            m.append(
                (
                    "web-tile",
                    dest,
                    {"canvas": size, "h_frac": GLYPH_FRAC, "tile": WEB_TILE_INSET},
                )
            )
        # Maskable icons are cropped to arbitrary shapes by the launcher and
        # must be fully opaque; alpha corners render black on some Androids.
        tile_safe(
            size,
            CLIENT / f"web/icons/icon-maskable-{size}.png",
            TEMPLATE_BUILD / f"web/icons/Icon-maskable-{size}.png",
        )

    for dest in (
        CLIENT / "web/icons/apple-touch-icon-192.png",
        TEMPLATE_BUILD / "web/icons/apple-touch-icon-192.png",
    ):
        m.append(
            (
                "tile-large",
                dest,
                {"canvas": 192, "h_frac": APPLE_TOUCH_FRAC, "bg": BRAND_BG},
            )
        )

    # Shown while the Flutter engine boots, inside a CSS zoom/pulse animation.
    # Must stay transparent (no background is set behind it) and centred (the
    # animation scales about the element centre, so off-centre art drifts).
    for dest in (
        CLIENT / "web/icons/loading-animation.png",
        TEMPLATE_BUILD / "web/icons/loading-animation.png",
    ):
        m.append(("loading", dest, {"canvas": 512, "h_frac": LOADING_FRAC}))

    # --- Windows ----------------------------------------------------------
    m.append(
        (
            "ico",
            CLIENT / "windows/runner/resources/app_icon.ico",
            {"sizes": [16, 32, 48, 96, 256]},
        )
    )
    m.append(
        (
            "ico",
            TEMPLATE_BUILD / "windows/runner/resources/app_icon.ico",
            {"sizes": [16, 32, 48, 256]},
        )
    )
    m.append(("ico", WEB_STATIC / "favicon.ico", {"sizes": [16, 32, 48]}))

    # No `splash_android.png` is shipped. `flet create` used to include one, but
    # `icon.png` is framed at GLYPH_FRAC and so already fits the Android 12
    # splash circle, making it redundant - and worse, a user who replaced only
    # `icon.png` kept the stock splash, because `splash_android` wins the
    # fallback chain in `customize_splash_images`. Omitting it lets the splash
    # follow whatever icon the user supplies.

    # --- examples and test fixtures --------------------------------------
    glyph(
        192,
        EXAMPLES / "controls/core/layout_control/assets/icon-192.png",
        EXAMPLES / "controls/core/layout_control/bursting_flet/assets/icon-192.png",
        EXAMPLES / "controls/material/list_tile/list_tile/assets/assets/icon-192.png",
        INTEGRATION / "assets/assets/icon-192.png",
    )
    glyph(
        512,
        EXAMPLES / "controls/core/image/assets/app_icon_512.png",
        EXAMPLES / "controls/core/image/gallery/assets/app_icon_512.png",
    )

    # --- website ----------------------------------------------------------
    glyph(300, WEB_STATIC / "flet-logo-300.png")

    return m


SVG_COPIES = [
    (SYMBOL_SVG, WEB_STATIC / "logo.svg"),
    (SYMBOL_SVG, INTEGRATION / "assets/logo.svg"),
    (LOGO_DIR / "flet-logo.svg", WEB_STATIC / "flet-logo.svg"),
    (LOGO_DIR / "flet-logo-dark.svg", WEB_STATIC / "flet-logo-dark.svg"),
]


MASTER_SVGS = ["flet-logo.svg", "flet-logo-dark.svg", "logo-symbol.svg"]

# Old-palette presentation attributes that design tools leave behind on paths
# whose inline `style="fill:..."` overrides them. Correct per the CSS cascade,
# so they render fine, but any tool that reads the presentation attribute and
# ignores `style` would draw the previous brand.
STALE_FILL_ATTRS = ("#0098da", "#ee3167")


def normalize_masters() -> int:
    """Clean up freshly exported master SVGs in place.

    Design tools re-export with stale attributes and sub-pixel float noise that
    makes the light and dark lockups render at slightly different widths, which
    shows up as the navbar logo jumping on theme toggle. Run this after
    dropping in new artwork, before generating.
    """
    changed = 0
    for name in MASTER_SVGS:
        path = LOGO_DIR / name
        if not path.exists():
            print(f"  {name}: missing, skipped")
            continue
        src = path.read_text()
        out = src
        notes = []

        for colour in STALE_FILL_ATTRS:
            out, n = re.subn(r'\n?\s*fill="' + re.escape(colour) + r'"', "", out)
            if n:
                notes.append(f'stripped {n}x fill="{colour}"')
        out, n = re.subn(r'\n?\s*fill-opacity="0\.639"', "", out)
        if n:
            notes.append(f"stripped {n}x stale fill-opacity")

        # Screen readers spell all-caps strings out letter by letter, and the
        # symbol-only file contains no text at all.
        for pattern, repl, label in (
            (r'aria-label="FLET"', 'aria-label="Flet"', "aria-label"),
            (r"(<title[^>]*>)FLET(</title>)", r"\1Flet\2", "<title>"),
            (r"(<dc:title>)FLET(</dc:title>)", r"\1Flet\2", "dc:title"),
        ):
            out, n = re.subn(pattern, repl, out)
            if n:
                notes.append(f"{label} FLET -> Flet")

        if out != src:
            path.write_text(out)
            changed += 1
        print(f"  {name}: {'; '.join(notes) if notes else 'already clean'}")

    changed += _match_lockup_dimensions()
    return changed


def _match_lockup_dimensions(tolerance: float = 0.01) -> int:
    """Force the dark lockup's canvas to exactly match the light one's.

    Design tools export the two variants with sub-pixel differences
    (1861.5813 vs 1861.5814). At a fixed navbar height that makes the logo
    change size when the viewer toggles the theme. Only the root element's
    `viewBox`/`width`/`height` are touched - never path geometry - and only
    when the two already agree to within `tolerance`, so a genuine redesign
    is reported rather than silently overwritten.
    """
    light, dark = LOGO_DIR / "flet-logo.svg", LOGO_DIR / "flet-logo-dark.svg"
    if not (light.exists() and dark.exists()):
        return 0

    def canvas(text: str) -> tuple[str, str, str] | None:
        vb = re.search(r'viewBox="([^"]*)"', text)
        w = re.search(r'\swidth="([\d.]+)"', text)
        h = re.search(r'\sheight="([\d.]+)"', text)
        return (vb.group(1), w.group(1), h.group(1)) if vb and w and h else None

    light_text, dark_text = light.read_text(), dark.read_text()
    lc, dc = canvas(light_text), canvas(dark_text)
    if not lc or not dc:
        return 0
    if lc == dc:
        return 0

    lvb = [float(v) for v in lc[0].split()]
    dvb = [float(v) for v in dc[0].split()]
    if len(lvb) != 4 or any(abs(a - b) > tolerance for a, b in zip(lvb, dvb)):
        print("\n  WARNING: lockup canvases differ by more than float noise -")
        print("  left alone. The navbar logo will change size on theme toggle:")
        print(f"    flet-logo.svg:      {lc[0]}")
        print(f"    flet-logo-dark.svg: {dc[0]}")
        return 0

    out = dark_text.replace(f'viewBox="{dc[0]}"', f'viewBox="{lc[0]}"', 1)
    out = re.sub(r'(\swidth=")[\d.]+(")', rf"\g<1>{lc[1]}\g<2>", out, count=1)
    out = re.sub(r'(\sheight=")[\d.]+(")', rf"\g<1>{lc[2]}\g<2>", out, count=1)
    dark.write_text(out)
    print(f"  flet-logo-dark.svg: canvas matched to light ({dc[0]} -> {lc[0]})")
    return 1


def render(variant: str, kwargs: dict) -> Image.Image:
    if variant == "macos":
        size = kwargs["canvas"]
        full = compose_macos(1024)
        return full if size == 1024 else full.resize((size, size), Image.LANCZOS)
    return compose(**kwargs)


def generate() -> int:
    count = 0
    for variant, dest, kwargs in build_manifest():
        if variant == "ico":
            save_ico(dest, kwargs["sizes"])
        else:
            save_png(render(variant, kwargs), dest)
        count += 1
    for src, dest in SVG_COPIES:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        count += 1
    return count


# --------------------------------------------------------------------------
# verification
# --------------------------------------------------------------------------


def verify() -> int:
    failures: list[str] = []

    def check(cond: bool, msg: str) -> None:
        if not cond:
            failures.append(msg)

    for variant, dest, kwargs in build_manifest():
        rel = dest.relative_to(REPO)
        if not dest.exists():
            failures.append(f"missing: {rel}")
            continue

        if variant == "ico":
            got = sorted(w for w, _ in Image.open(dest).ico.sizes())
            want = sorted(kwargs["sizes"])
            check(got == want, f"{rel}: ico sizes {got} != {want}")
            continue

        img = Image.open(dest)
        size = kwargs["canvas"]
        check(img.size == (size, size), f"{rel}: size {img.size} != {(size, size)}")

        if variant in ("tile-safe", "tile-large"):
            check(
                img.mode == "RGB",
                f"{rel}: mode {img.mode} != RGB (must not carry alpha)",
            )
        else:
            rgba = img.convert("RGBA")
            lo, hi = rgba.getchannel("A").getextrema()
            check(lo == 0, f"{rel}: expected transparency, min alpha={lo}")

    for _, dest in SVG_COPIES:
        check(dest.exists(), f"missing: {dest.relative_to(REPO)}")

    a, b = WEB_STATIC / "logo.svg", INTEGRATION / "assets/logo.svg"
    if a.exists() and b.exists():
        check(
            a.read_bytes() == b.read_bytes(),
            "website/static/img/logo.svg and integration_tests/assets/logo.svg differ",
        )

    for f in failures:
        print(f"FAIL {f}")
    print(f"\n{len(failures)} failure(s)")
    return 1 if failures else 0


def contact_sheet(out: Path) -> None:
    """Every output over four backgrounds, so 90 files can be eyeballed at once."""
    entries = [
        (d, kwargs.get("canvas", max(kwargs.get("sizes", [256]))))
        for _, d, kwargs in build_manifest()
    ]
    cell, pad, cols = 128, 8, 12
    rows = (len(entries) + cols - 1) // cols
    band = rows * (cell + pad) + pad
    bands = [
        ("checker", None),
        ("white", (255, 255, 255)),
        ("dark", (34, 34, 34)),
        ("grey", (128, 128, 128)),
    ]
    sheet = Image.new("RGB", (cols * (cell + pad) + pad, band * len(bands)), (0, 0, 0))

    for bi, (_, colour) in enumerate(bands):
        if colour is None:
            bg = Image.new("RGB", (sheet.width, band), (255, 255, 255))
            px = bg.load()
            for y in range(band):
                for x in range(sheet.width):
                    if (x // 8 + y // 8) % 2:
                        px[x, y] = (204, 204, 204)
        else:
            bg = Image.new("RGB", (sheet.width, band), colour)
        for i, (dest, _) in enumerate(entries):
            if not dest.exists():
                continue
            img = Image.open(dest)
            if dest.suffix == ".ico":
                img = img.convert("RGBA")
            img = img.convert("RGBA")
            img.thumbnail((cell, cell), Image.LANCZOS)
            x = pad + (i % cols) * (cell + pad) + (cell - img.width) // 2
            y = pad + (i // cols) * (cell + pad) + (cell - img.height) // 2
            bg.paste(img, (x, y), img)
        sheet.paste(bg, (0, bi * band))

    sheet.save(out)
    print(f"contact sheet -> {out}  ({len(entries)} assets x {len(bands)} backgrounds)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--verify", action="store_true", help="check committed output")
    ap.add_argument(
        "--normalize",
        action="store_true",
        help="clean up freshly exported master SVGs in media/logo/ (run after new artwork)",
    )
    ap.add_argument("--contact-sheet", type=Path, metavar="PNG")
    args = ap.parse_args()

    if args.normalize:
        print(f"normalizing masters in {LOGO_DIR.relative_to(REPO)}/")
        n = normalize_masters()
        print(f"\n{n} file(s) changed")
        return 0
    if args.verify:
        return verify()
    if args.contact_sheet:
        contact_sheet(args.contact_sheet)
        return 0

    n = generate()
    print(f"generated {n} files from {MASTER.relative_to(REPO)}")
    print(f"mark: {MARK.width}x{MARK.height} (aspect {MARK.width / MARK.height:.3f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
