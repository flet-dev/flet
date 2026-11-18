"""
Extract the desktop client bundled by `flet pack` into a directory.

Usage: extract_packed_client.py <dist dir> <app name> <output dir>

Reads `flet_desktop/app/flet-windows.zip` from a one-folder bundle
(`<dist>/<name>/`, in any contents directory) or a one-file executable
(`<dist>/<name>.exe`) and unzips it into the output directory.
"""

import io
import sys
import zipfile
from pathlib import Path

ARCHIVE = "flet_desktop/app/flet-windows.zip"


def read_archive(dist: Path, name: str) -> bytes:
    onedir = dist / name
    if onedir.is_dir():
        # PyInstaller's contents directory is `_internal` unless
        # `--contents-directory` changes it, so search the whole bundle.
        found = [
            p
            for p in onedir.rglob("flet-windows.zip")
            if p.as_posix().endswith(ARCHIVE)
        ]
        if not found:
            raise SystemExit(f"{ARCHIVE} not found in {onedir}")
        return found[0].read_bytes()

    from PyInstaller.archive.readers import CArchiveReader

    reader = CArchiveReader(str(dist / f"{name}.exe"))
    for entry in reader.toc:
        if entry.replace("\\", "/") == ARCHIVE:
            return reader.extract(entry)
    raise SystemExit(f"{ARCHIVE} not found in {dist / name}.exe")


def main() -> None:
    dist, name, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    with zipfile.ZipFile(io.BytesIO(read_archive(dist, name))) as zf:
        zf.extractall(out)
    print(f"Extracted the packed client into {out}")


if __name__ == "__main__":
    main()
