"""Low-level image compositing shared by the icon and splash generators.

Pillow is the only dependency. Nothing here reads or writes anything except
through the two explicit `save_*` helpers, so the rest of the package stays
pure and testable.

Two rules the whole package depends on:

* **Resample once, from the full-resolution source.** Chained downscaling
  (192 -> 144 -> 96) is what makes small icons mushy.
* **Resample with premultiplied alpha.** Averaging non-premultiplied RGBA
  blends the invisible colour under transparent pixels into the visible edge,
  which leaves a dark halo around any logo with a soft edge.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from pathlib import Path

from PIL import Image, ImageFilter

__all__ = [
    "MACOS_SHADOW_ALPHA",
    "MACOS_SHADOW_BLUR",
    "MACOS_SHADOW_DY",
    "MACOS_SQUIRCLE_N",
    "MACOS_TILE_RATIO",
    "WEB_TILE_INSET",
    "WEB_TILE_N",
    "WHITE",
    "alpha_extent",
    "apple_grid",
    "density_size",
    "has_transparent_corners",
    "parse_hex_color",
    "place",
    "save_ico",
    "save_png",
    "scale_to_fit",
    "scale_to_height",
    "superellipse_mask",
]

WHITE = (255, 255, 255)
"""Default flatten colour for surfaces that reject alpha."""

# The macOS icon grid: an 824x824 tile inset in a 1024 canvas, plus a drop
# shadow. Measured from Apple's own icons and from Flutter's template default;
# see the package README for why the shape is baked in rather than left to the
# system.
MACOS_TILE_RATIO = 824 / 1024
MACOS_SQUIRCLE_N = 5.0
MACOS_SHADOW_BLUR = 11
MACOS_SHADOW_DY = 8
MACOS_SHADOW_ALPHA = 64

# Web PWA "any" icons sit on a tile inset slightly from the canvas edge.
WEB_TILE_INSET = 0.953
WEB_TILE_N = 4.0


def parse_hex_color(value: str) -> tuple[int, int, int]:
    """Parse `#rrggbb` (or `rrggbb`, or the 3-digit short form) into RGB.

    Args:
        value: The colour string.

    Returns:
        An `(r, g, b)` tuple.

    Raises:
        ValueError: If the string is not a 3- or 6-digit hex colour.
    """

    text = value.strip().lstrip("#")
    if len(text) == 3:
        text = "".join(c * 2 for c in text)
    if len(text) != 6:
        raise ValueError(f"not a hex colour: {value!r}")
    try:
        return (int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16))
    except ValueError as e:
        raise ValueError(f"not a hex colour: {value!r}") from e


def density_size(width: int, height: int, density: float) -> tuple[int, int]:
    """Scale a 4x source down to a given screen density.

    Reproduces Dart's `w * density ~/ 4`, which truncates the float product
    toward zero. Python's `//` on a float floors instead, which differs for
    the 1.5 (hdpi) case, so the multiplication is done in float and truncated
    explicitly.

    Args:
        width: Source width in pixels.
        height: Source height in pixels.
        density: Target density, where 4 means "same size as the source".

    Returns:
        The `(width, height)` for that density, never smaller than 1x1.
    """

    return (
        max(1, int(width * density / 4)),
        max(1, int(height * density / 4)),
    )


def scale_to_height(art: Image.Image, height: int) -> Image.Image:
    """Resample `art` to an exact height, preserving its aspect ratio."""

    height = max(1, height)
    width = max(1, round(art.width * height / art.height))
    return _resample(art, (width, height))


def scale_to_fit(art: Image.Image, box: int) -> Image.Image:
    """Resample `art` to fit inside a `box`x`box` square, preserving aspect."""

    box = max(1, box)
    if art.width >= art.height:
        return _resample(art, (box, max(1, round(art.height * box / art.width))))
    return _resample(art, (max(1, round(art.width * box / art.height)), box))


def _resample(art: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize with premultiplied alpha, in one LANCZOS step.

    `RGBa` is Pillow's premultiplied mode. Resizing there and converting back
    is what keeps a soft edge from picking up the colour hiding under the
    transparent pixels. `Image.resize` is used rather than `Image.thumbnail`,
    whose default `reducing_gap=2.0` does a two-step reduce that softens small
    sizes.

    A resample to the image's existing size is skipped rather than performed:
    the premultiply round-trip is lossy where alpha is near zero, since the
    colour cannot be recovered once it has been scaled into the noise, so an
    identity resize would quietly rewrite the soft edge of an icon that was
    already the right size.
    """

    if art.mode != "RGBA":
        art = art.convert("RGBA")
    if art.size == size:
        return art
    return art.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")


def superellipse_mask(size: int, n: float, supersample: int = 4) -> Image.Image:
    """Build an `L`-mode mask of a superellipse, antialiased by supersampling.

    `|u|^n + |v|^n <= 1` over `u, v` in `[-1, 1]`. `n = 2` is a circle and
    large `n` approaches a square; around 5 approximates the continuous-
    curvature corner Apple uses, which a plain rounded rectangle does not
    match.

    Rows are filled by solving the inequality for `u` rather than testing
    every pixel, then correcting the two boundary pixels against the exact
    predicate so the result is identical to the naive scan.

    Args:
        size: Side length of the returned mask.
        n: Superellipse exponent.
        supersample: Factor to render at before downsampling.

    Returns:
        An `L`-mode image, 255 inside the shape and 0 outside.
    """

    t = max(1, size * supersample)
    if t == 1:
        return Image.new("L", (size, size), 255)

    span = t - 1
    half = span / 2.0
    data = bytearray(t * t)
    row = b"\xff"

    for y in range(t):
        v = abs((2 * y - span) / span)
        remainder = 1.0 - v**n
        if remainder < 0.0:
            continue
        u = remainder ** (1.0 / n)
        lo = math.ceil(half - u * half)
        hi = math.floor(half + u * half)

        # The analytic bounds can be off by one where the float maths lands
        # exactly on the boundary; settle it with the predicate itself.
        def inside(x: int, _v: float = v**n) -> bool:
            """Whether column `x` satisfies the superellipse inequality."""
            return abs((2 * x - span) / span) ** n + _v <= 1.0

        while lo > 0 and inside(lo - 1):
            lo -= 1
        while lo <= hi and not inside(lo):
            lo += 1
        while hi < span and inside(hi + 1):
            hi += 1
        while hi >= lo and not inside(hi):
            hi -= 1

        if lo <= hi:
            base = y * t
            data[base + lo : base + hi + 1] = row * (hi - lo + 1)

    mask = Image.frombytes("L", (t, t), bytes(data))
    return mask.resize((size, size), Image.LANCZOS)


def place(
    art: Image.Image,
    canvas: int,
    *,
    bg: tuple[int, int, int] | None = None,
    tile: float | None = None,
    tile_n: float = WEB_TILE_N,
    tile_color: tuple[int, int, int] = WHITE,
    offset: tuple[int, int] = (0, 0),
) -> Image.Image:
    """Centre already-scaled `art` on a square canvas.

    Args:
        art: The artwork, scaled to its final size by the caller.
        canvas: Side length of the output.
        bg: Flatten onto this solid colour and return mode `RGB`. Used where
            a platform rejects alpha.
        tile: Draw a superellipse tile at this fraction of the canvas, leaving
            the area outside it transparent.
        tile_n: Superellipse exponent for `tile`.
        tile_color: Fill colour for `tile`.
        offset: Extra `(dx, dy)` applied to the artwork's position.

    Returns:
        Mode `RGB` when `bg` is given, otherwise `RGBA`.
    """

    if bg is not None:
        out = Image.new("RGB", (canvas, canvas), bg)
    else:
        out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
        if tile is not None:
            side = round(canvas * tile)
            plate = Image.new("RGBA", (side, side), (*tile_color, 255))
            plate.putalpha(superellipse_mask(side, tile_n))
            out.alpha_composite(plate, ((canvas - side) // 2, (canvas - side) // 2))

    if art.mode != "RGBA":
        art = art.convert("RGBA")
    x = (canvas - art.width) // 2 + offset[0]
    y = (canvas - art.height) // 2 + offset[1]
    if bg is not None:
        out.paste(art, (x, y), art)
    else:
        out.alpha_composite(art, (x, y))
    return out


def apple_grid(
    art: Image.Image,
    canvas: int = 1024,
    *,
    tile_ratio: float = MACOS_TILE_RATIO,
    n: float = MACOS_SQUIRCLE_N,
    blur: int = MACOS_SHADOW_BLUR,
    dy: int = MACOS_SHADOW_DY,
    shadow_alpha: int = MACOS_SHADOW_ALPHA,
    tile_color: tuple[int, int, int] = WHITE,
) -> Image.Image:
    """Compose the macOS icon grid: an inset squircle tile with a drop shadow.

    Compose once at the largest size and downscale the result for smaller
    ones. This is the one place chained downscaling is correct, because the
    tile, artwork and shadow have to shrink together.

    Args:
        art: Artwork already scaled to sit inside the tile.
        canvas: Side length of the output.
        tile_ratio: Tile size as a fraction of the canvas.
        n: Superellipse exponent for the tile corner.
        blur: Gaussian blur radius for the shadow.
        dy: Downward shadow offset.
        shadow_alpha: Shadow opacity, 0-255.
        tile_color: Tile fill colour.

    Returns:
        An `RGBA` image with transparent corners.
    """

    side = round(canvas * tile_ratio)
    mask = superellipse_mask(side, n)

    tile = Image.new("RGBA", (side, side), (*tile_color, 255))
    if art.mode != "RGBA":
        art = art.convert("RGBA")
    tile.alpha_composite(art, ((side - art.width) // 2, (side - art.height) // 2))
    tile.putalpha(mask)

    pos = ((canvas - side) // 2, (canvas - side) // 2)

    shadow = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    silhouette = Image.new("RGBA", (side, side), (0, 0, 0, shadow_alpha))
    silhouette.putalpha(mask.point(lambda value: value * shadow_alpha // 255))
    shadow.alpha_composite(silhouette, (pos[0], pos[1] + dy))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))

    out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    out.alpha_composite(shadow)
    out.alpha_composite(tile, pos)
    return out


def alpha_extent(img: Image.Image) -> float | None:
    """How far the opaque content reaches, as a fraction of the canvas.

    A value of 1.0 means the artwork touches an edge; 0.6 means it occupies
    the middle 60%. Used to tell whether artwork will survive a platform's
    guaranteed-visible area.

    Args:
        img: The image to measure.

    Returns:
        The fraction, or `None` when the image is fully opaque and so has no
            meaningful extent.
    """

    if img.mode != "RGBA":
        img = img.convert("RGBA")
    alpha = img.getchannel("A")
    if alpha.getextrema()[0] == 255:
        return None
    box = alpha.getbbox()
    if box is None:
        return 0.0
    left, top, right, bottom = box
    cx, cy = img.width / 2, img.height / 2
    reach = max(cx - left, right - cx, cy - top, bottom - cy)
    return 2 * reach / max(img.width, img.height)


def looks_pre_shaped(
    img: Image.Image, *, min_fill: float = 0.70, aspect_tolerance: float = 0.08
) -> bool:
    """Whether the artwork already has a platform icon shape baked into it.

    Used to avoid rounding an icon a second time. Transparent corners alone
    are not enough to tell: almost every logo with an alpha channel has them.
    A shaped icon is specifically a *filled, near-square tile* with its
    corners cut away, which separates cleanly from a logo in practice:

    ================================  ========  =============
    source                            aspect    fill in bbox
    ================================  ========  =============
    Flet brand mark                       0.77           0.56
    a generated macOS app icon            1.00           0.84
    GitHub Desktop's `electron.icns`      1.00           0.80
    ================================  ========  =============

    The corner check still matters, because a plain opaque square logo also
    scores 1.00 aspect and 1.00 fill, and that one does want a shape applied.

    Args:
        img: The image to inspect.
        min_fill: How much of its own bounding box the opaque content must
            cover.
        aspect_tolerance: How far from square the bounding box may be.

    Returns:
        `True` when the artwork looks like an already-shaped icon.
    """

    if img.mode != "RGBA":
        img = img.convert("RGBA")
    if not has_transparent_corners(img):
        return False
    box = img.getchannel("A").getbbox()
    if box is None:
        return False
    left, top, right, bottom = box
    width, height = right - left, bottom - top
    if not width or not height:
        return False
    if abs(width / height - 1.0) > aspect_tolerance:
        return False
    opaque = img.getchannel("A").crop(box).histogram()[255]
    return opaque / (width * height) >= min_fill


def has_transparent_corners(
    img: Image.Image, *, probe: float = 0.06, threshold: int = 8
) -> bool:
    """Whether all four corners are effectively transparent.

    A building block for :func:`looks_pre_shaped`; on its own it says only
    that the artwork is not a full-bleed rectangle.

    Args:
        img: The image to inspect.
        probe: Corner box size as a fraction of the image.
        threshold: Mean alpha below which a corner counts as transparent.

    Returns:
        `True` when every corner is effectively transparent.
    """

    if img.mode != "RGBA":
        img = img.convert("RGBA")
    alpha = img.getchannel("A")
    size = max(1, round(min(img.width, img.height) * probe))
    boxes = (
        (0, 0, size, size),
        (img.width - size, 0, img.width, size),
        (0, img.height - size, size, img.height),
        (img.width - size, img.height - size, img.width, img.height),
    )
    return all(_mean(alpha.crop(b)) < threshold for b in boxes)


def _mean(img: Image.Image) -> float:
    """Mean pixel value of a single-channel image, via its histogram."""
    histogram = img.histogram()
    total = sum(histogram)
    if not total:
        return 0.0
    return sum(value * count for value, count in enumerate(histogram)) / total


def save_png(img: Image.Image, path: Path) -> None:
    """Write a PNG, creating parent directories.

    `optimize=True` with no metadata keeps output deterministic for a given
    Pillow version, so regenerating produces byte-identical files.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG", optimize=True)


def save_ico(path: Path, images: Mapping[int, Image.Image]) -> None:
    """Write a multi-size ICO from one pre-rendered image per size.

    Pillow's ICO writer has two traps this avoids. It silently drops any
    requested size larger than the base image, so the base is the largest one;
    and for a size with no exact match it resamples from a leaked loop
    variable rather than the base, so every requested size is supplied.

    Args:
        path: Destination file.
        images: Pre-rendered square image per pixel size.

    Raises:
        ValueError: If `images` is empty.
    """

    if not images:
        raise ValueError("save_ico() needs at least one image")
    sizes = sorted(images)
    base = images[sizes[-1]]
    path.parent.mkdir(parents=True, exist_ok=True)
    base.save(
        path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=[images[s] for s in sizes[:-1]],
    )


def radial_extent(img: Image.Image, *, sample: int = 256) -> float | None:
    """How far opaque content reaches from the centre, as a fraction of half the canvas.

    The circular counterpart to :func:`alpha_extent`. A round mask cares about
    distance from the centre, not reach along either axis, so artwork whose
    extremes sit off-axis is measured correctly here and underestimated there:
    Flet's own mark reads 0.60 by axis and 0.97 against Android's mask radius.

    Only the leftmost and rightmost opaque pixel of each row can be furthest
    from the centre, so the scan is per row rather than per pixel, on a
    downscaled copy.

    Args:
        img: The image to measure.
        sample: Side length to measure at. Larger is slower and no more
            accurate than the artwork's own antialiasing.

    Returns:
        The fraction, or `None` when the image is fully opaque and so has no
            meaningful extent.
    """

    if img.mode != "RGBA":
        img = img.convert("RGBA")
    alpha = img.getchannel("A")
    if alpha.getextrema()[0] == 255:
        return None
    if max(alpha.size) > sample:
        # Preserve the aspect ratio. Resizing to a flat (sample, sample) would
        # squash a non-square source into a square before measuring it, and
        # report a distance the artwork never had.
        scale = sample / max(alpha.size)
        alpha = alpha.resize(
            (max(1, round(alpha.width * scale)), max(1, round(alpha.height * scale))),
            Image.BILINEAR,
        )
    width, height = alpha.size
    alpha = alpha.point(lambda v: 255 if v > 8 else 0)
    cx, cy = (width - 1) / 2, (height - 1) / 2
    half = max(cx, cy) or 1.0
    furthest = 0.0
    for y in range(height):
        row = alpha.crop((0, y, width, y + 1))
        box = row.getbbox()
        if box is None:
            continue
        dy = y - cy
        for x in (box[0], box[2] - 1):
            furthest = max(furthest, math.hypot(x - cx, dy))
    return furthest / half
