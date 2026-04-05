import os
import tempfile
import uuid
from pathlib import Path

from flet.utils import copy_tree
from flet_desktop import ensure_client_cached


def get_flet_bin_path():
    """
    Return path to Flet desktop binaries, if available.

    Resolution order:

    1. FLET_VIEW_PATH environment variable.
    2. Cached / downloaded client from ~/.flet/client/.

    Returns:
        Absolute binaries directory path or `None` when not found.
    """

    # 1. Check FLET_VIEW_PATH (developer / custom build mode).
    flet_view_path = os.environ.get("FLET_VIEW_PATH")
    if flet_view_path and os.path.exists(flet_view_path):
        return flet_view_path

    # 2. Fall back to cached / downloaded client.
    cache_dir = ensure_client_cached()
    if cache_dir and cache_dir.exists():
        return str(cache_dir)

    return None


def copy_flet_bin():
    """
    Copy packaged Flet desktop binaries into a temporary directory.

    Returns:
        Path to the temporary copied binaries directory, or `None` when source
        binaries are unavailable.
    """

    bin_path = get_flet_bin_path()
    if not bin_path:
        return None

    # create temp bin dir
    temp_bin_dir = Path(tempfile.gettempdir()).joinpath(str(uuid.uuid4()))
    copy_tree(bin_path, str(temp_bin_dir))
    return str(temp_bin_dir)
