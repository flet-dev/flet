import os
import shutil
import tempfile
import uuid
from pathlib import Path

import pefile
from PyInstaller.compat import win32api
from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo,
    StringFileInfo,
    StringStruct,
    StringTable,
    VarFileInfo,
    VarStruct,
    VSVersionInfo,
    decode,
)

import flet.__pyinstaller.config as hook_config

# raise Exception(f"icon_file: {hook_config.icon_file}")


def copy_bin():
    bin_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, "bin")
    )
    if not os.path.exists(bin_path):
        return None

    # create temp bin dir
    temp_bin_dir = Path(tempfile.gettempdir()).joinpath(str(uuid.uuid4()))
    shutil.copytree(bin_path, str(temp_bin_dir))
    return str(temp_bin_dir)


bin_path = copy_bin()
hook_config.temp_bin_dir = bin_path

if bin_path != None:
    # package "bin/fletd" only
    if os.getenv("PACKAGE_FLETD_ONLY"):
        bin_path = os.path.join(bin_path, "fletd*")

    datas = [(bin_path, "flet/bin")]
