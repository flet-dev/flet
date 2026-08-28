"""Write a solid-colour PNG of a given size, using only the stdlib.

TEMPORARY -- part of the issue #2269 Linux icon verification harness.

Deterministic output, so a CI assertion can compare the bundled copies of an
icon against its source byte for byte.

Usage: make_png.py <path> <width> <height> <r> <g> <b>
"""

import struct
import sys
import zlib


def chunk(tag: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + tag
        + data
        + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    )


def main() -> int:
    path, width, height, r, g, b = (
        sys.argv[1],
        int(sys.argv[2]),
        int(sys.argv[3]),
        int(sys.argv[4]),
        int(sys.argv[5]),
        int(sys.argv[6]),
    )
    # One filter byte (0 = None) per scanline, then RGB triplets.
    raw = b"".join(b"\x00" + bytes([r, g, b]) * width for _ in range(height))
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    with open(path, "wb") as f:
        f.write(png)
    print(f"wrote {path} ({width}x{height}, {len(png)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
