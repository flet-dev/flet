import os
import tempfile
import uuid
from pathlib import Path

from flet.utils import copy_tree
from flet_desktop import get_package_bin_dir


def get_flet_bin_path():
    bin_path = get_package_bin_dir()
    if not os.path.exists(bin_path):
        return None
    return bin_path


def copy_flet_bin():
    bin_path = get_flet_bin_path()
    if not bin_path:
        return None

    # create temp bin dir
    temp_bin_dir = Path(tempfile.gettempdir()).joinpath(str(uuid.uuid4()))
    copy_tree(bin_path, str(temp_bin_dir))
    return str(temp_bin_dir)
