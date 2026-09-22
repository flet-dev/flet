"""Loading and normalising a user-supplied source image."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

__all__ = ["MAX_SOURCE_SIZE", "SourceError", "load_source"]

MAX_SOURCE_SIZE = 2048
"""Sources larger than this are reduced once, rather than per output.

Every target is resampled from the source, so an 8000px original would be
downscaled a dozen times over. One reduction to a size comfortably above the
largest target (1024) costs nothing visible and bounds the work.
"""


class SourceError(Exception):
    """A source image could not be read."""


def load_source(path: str | Path) -> tuple[Image.Image, bool]:
    """Read an image and normalise it into something safe to composite.

    Handles the awkward inputs a real user supplies: a phone photo with an
    EXIF rotation, a palette or CMYK PNG, an animated GIF, a non-square
    banner, or a pre-made `.ico`/`.icns` holding several resolutions.

    Args:
        path: The image to read.

    Returns:
        A tuple of the normalised `RGBA` image and whether it was
            pre-rendered - true for `.ico`/`.icns`, whose author has already
            applied whatever platform shaping they wanted.

    Raises:
        SourceError: If the file is missing, not an image, or truncated.
    """

    path = Path(path)
    try:
        img = Image.open(path)
        img.load()
    except FileNotFoundError as e:
        raise SourceError(f"icon source not found: {path}") from e
    except (UnidentifiedImageError, OSError, ValueError) as e:
        raise SourceError(f"could not read image {path.name}: {e}") from e

    pre_rendered = path.suffix.lower() in (".ico", ".icns")
    if pre_rendered:
        img = _largest_frame(img)

    # An EXIF-rotated source would otherwise be composited sideways.
    img = ImageOps.exif_transpose(img) or img

    # Animated sources: the first frame is the only sensible icon.
    if getattr(img, "n_frames", 1) > 1:
        img.seek(0)

    if img.mode != "RGBA":
        img = img.convert("RGBA")

    if max(img.size) > MAX_SOURCE_SIZE:
        scale = MAX_SOURCE_SIZE / max(img.size)
        img = (
            img.convert("RGBa")
            .resize(
                (max(1, round(img.width * scale)), max(1, round(img.height * scale))),
                Image.LANCZOS,
            )
            .convert("RGBA")
        )

    return img, pre_rendered


def square(img: Image.Image) -> tuple[Image.Image, str | None]:
    """Pad a non-square image to a square canvas, centred.

    Stretching would distort the artwork, and cropping would discard part of
    it, so the shorter axis is padded with transparency instead.

    Args:
        img: The image to square off.

    Returns:
        A tuple of the squared image and a warning, or `None` when the input
            was already square.
    """

    if img.width == img.height:
        return img, None
    side = max(img.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.alpha_composite(img, ((side - img.width) // 2, (side - img.height) // 2))
    return canvas, (
        f"source is {img.width}x{img.height}, not square: padded to {side}x{side}. "
        "Supply a square image to control the framing yourself."
    )


def _largest_frame(img: Image.Image) -> Image.Image:
    """Pick the highest-resolution frame of a multi-resolution container."""

    sizes = getattr(getattr(img, "ico", None), "sizes", None)
    if callable(sizes):
        try:
            return img.ico.getimage(max(sizes()))
        except Exception:  # noqa: BLE001 - fall back to whatever Pillow opened
            return img
    return img
