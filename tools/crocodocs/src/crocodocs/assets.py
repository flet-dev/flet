"""Asset syncing helpers."""

from __future__ import annotations

import shutil
from pathlib import Path


def bulk_copy_assets(
    source_root: Path,
    dest_root: Path,
    include_exts: set[str] | None = None,
) -> int:
    """Copy all matching files from *source_root* to *dest_root*.

    Returns the number of files copied.
    """
    copied = 0
    for source_path in sorted(source_root.rglob("*")):
        if not source_path.is_file():
            continue
        if include_exts and source_path.suffix.lower() not in include_exts:
            continue
        relative = source_path.relative_to(source_root)
        dest_path = dest_root / relative
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest_path)
        copied += 1
    return copied
