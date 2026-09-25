import os
import stat
import sys
from collections.abc import Iterable
from pathlib import Path

PYVENV_CFG = "pyvenv.cfg"
PYCACHE_DIR = "__pycache__"


def _is_hidden(entry: os.DirEntry) -> bool:
    """
    Check whether a directory entry is hidden.

    An entry is hidden when its name starts with `.` (on every platform) or,
    on Windows, when it has the hidden file attribute.

    Args:
        entry: Directory entry to check.

    Returns:
        `True` if the entry is hidden, `False` otherwise.
    """

    if entry.name.startswith("."):
        return True
    if sys.platform != "win32":
        return False
    try:
        attributes = entry.stat(follow_symlinks=False).st_file_attributes
    except OSError:
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_HIDDEN)


def _is_venv(path: str) -> bool:
    return os.path.isfile(os.path.join(path, PYVENV_CFG))


def _normalize(paths: Iterable[str]) -> set[str]:
    return {os.path.normpath(p.replace("/", os.sep)) for p in paths}


def find_default_excludes(
    app_path: Path, include: Iterable[str] = (), exclude: Iterable[str] = ()
) -> list[str]:
    """
    Find app files and directories that are excluded from the package by default.

    Matched are:

    - hidden files and directories directly in `app_path` (a name starting
      with `.`, or the hidden attribute on Windows);
    - virtual environments (directories containing `pyvenv.cfg`) at any depth;
    - `__pycache__` directories at any depth.

    Args:
        app_path: Root directory of the Python app being packaged.
        include: Relative paths to keep even if matched by the rules above.
            Both `/` and `\\` separators are accepted.
        exclude: Relative paths already excluded from the package. They are
            not scanned and not returned.

    Returns:
        Sorted relative paths joined with `os.sep`, the form serious_python
        compares its exclude list against.
    """

    keep = _normalize(include)
    skip = _normalize(exclude)
    excludes: list[str] = []

    def add(rel_path: str) -> bool:
        if rel_path in keep:
            return False
        excludes.append(rel_path)
        return True

    # top-level hidden entries
    subdirs: list[str] = []
    with os.scandir(app_path) as entries:
        for entry in entries:
            if entry.name in skip:
                continue
            if _is_hidden(entry) and add(entry.name):
                continue
            if entry.is_dir(follow_symlinks=False):
                subdirs.append(entry.name)

    # virtual environments and __pycache__ at any depth
    for subdir in subdirs:
        for dirpath, dirnames, _ in os.walk(app_path / subdir):
            rel_dir = os.path.relpath(dirpath, app_path)
            if (os.path.basename(dirpath) == PYCACHE_DIR or _is_venv(dirpath)) and add(
                rel_dir
            ):
                dirnames.clear()
                continue
            dirnames[:] = [d for d in dirnames if os.path.join(rel_dir, d) not in skip]

    return sorted(excludes)
