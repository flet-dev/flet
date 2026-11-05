import gzip
import os
import shutil

COMPRESSIBLE_EXTENSIONS = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".map",
    ".mjs",
    ".otf",
    ".svg",
    ".ttf",
    ".txt",
    ".wasm",
    ".xml",
}
"""
Extensions of files sent gzip-compressed to browsers that accept it.

Text and WebAssembly files shrink about 3x with gzip; images, archives and
`.woff2` fonts are already compressed.
"""

MIN_COMPRESSED_FILE_SIZE = 1024
"""
Size in bytes below which files are sent uncompressed, as compression saves less
than it costs.
"""


def is_compressible(path: str, stat_result: os.stat_result) -> bool:
    """
    Whether a static file is served gzip-compressed to browsers that accept it.

    Args:
        path: Path of the file.
        stat_result: The file's `os.stat()` result.
    """

    return (
        os.path.splitext(path)[1].lower() in COMPRESSIBLE_EXTENSIONS
        and stat_result.st_size >= MIN_COMPRESSED_FILE_SIZE
    )


def accepts_gzip(accept_encoding: str) -> bool:
    """
    Whether an `Accept-Encoding` request header allows a gzip response.

    Args:
        accept_encoding: Value of the header, e.g. `"gzip, deflate, br"`.

    Returns:
        `True` if `gzip`, or else `*`, is listed without `q=0`.
    """

    qualities = {}
    for coding in accept_encoding.split(","):
        name, *params = coding.split(";")
        quality = 1.0
        for param in params:
            key, _, value = param.partition("=")
            if key.strip().lower() == "q":
                try:
                    quality = float(value)
                except ValueError:
                    quality = 0.0
        qualities[name.strip().lower()] = quality
    return qualities.get("gzip", qualities.get("*", 0.0)) > 0


def write_gzip(source: str, target: str, stat_result: os.stat_result):
    """
    Write a gzip-compressed copy of a file.

    The copy gets the source's modification time, so that it is served with the
    same `Last-Modified` header. A copy left unfinished by an error is removed.

    Args:
        source: Path of the file to compress.
        target: Path of the compressed copy.
        stat_result: The source's `os.stat()` result.
    """

    temp = f"{target}.tmp"
    try:
        with (
            open(source, "rb") as src,
            open(temp, "wb") as raw,
            gzip.GzipFile(
                filename="", mode="wb", compresslevel=6, fileobj=raw, mtime=0
            ) as dst,
        ):
            shutil.copyfileobj(src, dst)
        os.utime(temp, ns=(stat_result.st_atime_ns, stat_result.st_mtime_ns))
        os.replace(temp, target)
    finally:
        if os.path.exists(temp):
            os.remove(temp)
