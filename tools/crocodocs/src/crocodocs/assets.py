"""Asset syncing helpers."""

from __future__ import annotations

import shutil
from pathlib import Path

# Directory names never worth syncing. These hold generated output, not authored
# assets, and an example that has been built locally carries a lot of it: a
# single `flet build ios` leaves ~1.4 GB under `build/`, including Swift Package
# Manager checkouts whose images match the include_exts filter and would
# otherwise be copied into the docs site.
SKIP_DIRS = frozenset(
    {
        ".dart_tool",
        ".git",
        ".venv",
        "__pycache__",
        "build",
        "node_modules",
    }
)


def bulk_copy_assets(
    source_root: Path,
    dest_root: Path,
    include_exts: set[str] | None = None,
) -> int:
    """Copy all matching files from *source_root* to *dest_root*.

    Directories named in :data:`SKIP_DIRS` are pruned, so build output under a
    source tree is never synced.

    Returns the number of files copied.
    """
    copied = 0
    for source_path in sorted(source_root.rglob("*")):
        if not source_path.is_file():
            continue
        if include_exts and source_path.suffix.lower() not in include_exts:
            continue
        relative = source_path.relative_to(source_root)
        if SKIP_DIRS.intersection(relative.parts[:-1]):
            continue
        dest_path = dest_root / relative
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        # Replace rather than write in place: copy2 preserves the source mode,
        # so a read-only source (SPM checkouts ship 0444) leaves a read-only
        # destination that the next run cannot reopen for writing.
        dest_path.unlink(missing_ok=True)
        shutil.copy2(source_path, dest_path)
        copied += 1
    return copied
