"""
Utility helpers for the flet-camera package.
"""

__all__ = ["detect_video_extension"]


def detect_video_extension(data: bytes) -> str:
    """
    Detects a likely video file extension from encoded bytes.

    Returns:
        One of `"webm"`, `"mov"`, `"mp4"`, or `"bin"` if unknown.
    """
    # Matroska/WebM EBML header.
    if data.startswith(b"\x1a\x45\xdf\xa3"):
        return "webm"

    # ISO BMFF (mp4/mov) starts with a box size + "ftyp".
    if len(data) >= 12 and data[4:8] == b"ftyp":
        brand = data[8:12]
        if brand == b"qt  ":
            return "mov"
        return "mp4"

    return "bin"
