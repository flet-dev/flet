import os
import tempfile
import uuid
from pathlib import Path

from flet.utils import copy_tree
from flet_desktop import ensure_client_cached, get_package_bin_dir


def get_flet_bin_path():
    """
    Return path to Flet desktop binaries, if available.

    Checks the package ``app/`` directory first (for PyInstaller-bundled
    builds), then falls back to the download cache at ``~/.flet/client/``,
    triggering a download if necessary.

    Returns:
        Absolute binaries directory path or ``None`` when not found.
    """

    # Check bundled binaries in the package (PyInstaller or legacy wheel).
    bin_path = get_package_bin_dir()
    if os.path.exists(bin_path) and os.listdir(bin_path):
        return bin_path

    # Fall back to cached / downloaded client.
    cache_dir = ensure_client_cached()
    if cache_dir and cache_dir.exists():
        return str(cache_dir)

    return None


def copy_flet_bin():
    """
    Copy packaged Flet desktop binaries into a temporary directory.

    Returns:
        Path to the temporary copied binaries directory, or ``None`` when source
        binaries are unavailable.
    """

    bin_path = get_flet_bin_path()
    if not bin_path:
        return None

    # create temp bin dir
    temp_bin_dir = Path(tempfile.gettempdir()).joinpath(str(uuid.uuid4()))
    copy_tree(bin_path, str(temp_bin_dir))
    return str(temp_bin_dir)
