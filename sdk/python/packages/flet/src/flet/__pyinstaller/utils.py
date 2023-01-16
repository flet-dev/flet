import os
import shutil
import tempfile
import uuid
from pathlib import Path


def get_flet_bin_path():
    bin_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, "bin")
    )
    if not os.path.exists(bin_path):
        return None
    return bin_path


def copy_flet_bin():
    bin_path = get_flet_bin_path()
    if not bin_path:
        return None

    # create temp bin dir
    temp_bin_dir = Path(tempfile.gettempdir()).joinpath(str(uuid.uuid4()))
    shutil.copytree(bin_path, str(temp_bin_dir))
    return str(temp_bin_dir)
