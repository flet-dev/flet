"""Generate the demo app's Linux icon.

Demo branch only. The PNG it writes is committed next to the app, so this
script only runs when the icon needs changing:

    python3 .github/demo/make_icon.py .github/demo/app/src/assets/icon_linux.png

The icon is deliberately loud -- a white "F" on a magenta-to-orange gradient.
A reviewer has to spot it in a dock next to the stock Flutter icon that an
unfixed build would show, so it must not look like anything else there.

Written with zlib and struct rather than Pillow: the repo has no image
dependency, and adding one for a throwaway branch is not worth it.
"""

import struct
import sys
import zlib

SIZE = 256
SS = 3  # supersampling factor, for antialiased corners and edges


def _rounded_square(x: float, y: float, side: float, radius: float) -> bool:
    """Whether (x, y) falls inside a rounded square centred on the canvas."""
    lo = (SIZE - side) / 2
    hi = lo + side
    if not (lo <= x <= hi and lo <= y <= hi):
        return False
    # Only the four corner boxes need the distance test.
    cx = lo + radius if x < lo + radius else (hi - radius if x > hi - radius else x)
    cy = lo + radius if y < lo + radius else (hi - radius if y > hi - radius else y)
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius**2


# Stem, top bar and middle bar of a sans-serif "F", as (x0, y0, x1, y1).
GLYPH = [(92, 62, 124, 194), (92, 62, 190, 94), (92, 118, 172, 150)]


def _in_glyph(x: float, y: float) -> bool:
    return any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in GLYPH)


def _sample(x: float, y: float):
    """Colour at one sample point, as (r, g, b, a)."""
    if not _rounded_square(x, y, side=232, radius=52):
        return (0, 0, 0, 0)
    if _in_glyph(x, y):
        return (255, 255, 255, 255)
    t = y / SIZE  # vertical gradient: magenta at the top, orange at the bottom
    return (
        int(214 + (247 - 214) * t),
        int(31 + (147 - 31) * t),
        int(122 + (30 - 122) * t),
        255,
    )


def render() -> bytes:
    """The icon as raw RGBA scanlines, each prefixed with a filter byte."""
    raw = bytearray()
    step = 1.0 / SS
    offset = step / 2
    for py in range(SIZE):
        raw.append(0)  # PNG filter type 0 (None)
        for px in range(SIZE):
            acc = [0, 0, 0, 0]
            for sy in range(SS):
                for sx in range(SS):
                    for i, v in enumerate(
                        _sample(px + sx * step + offset, py + sy * step + offset)
                    ):
                        acc[i] += v
            n = SS * SS
            # Premultiplied averaging would be correct in general, but every
            # opaque sample here is either white or gradient, and they only
            # meet well inside the shape where alpha is already 255.
            raw.extend(bytes(v // n for v in acc))
    return bytes(raw)


def write_png(path: str, raw: bytes) -> None:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0)  # 8-bit RGBA
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", header))
        f.write(chunk(b"IDAT", zlib.compress(raw, 9)))
        f.write(chunk(b"IEND", b""))


if __name__ == "__main__":
    out = sys.argv[1]
    write_png(out, render())
    print(f"wrote {out} ({SIZE}x{SIZE})")
