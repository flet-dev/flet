import atexit
import shutil

from PyInstaller.utils.hooks import collect_data_files

import flet_cli.__pyinstaller.config as hook_config
from flet_cli.__pyinstaller.utils import archive_flet_bin

bin_path = hook_config.temp_bin_dir
if not bin_path:
    # A plain `pyinstaller` run, not `flet pack`: bundle the client archive
    # so the app doesn't download the client on its first start.
    bin_path = archive_flet_bin()
    if bin_path:
        atexit.register(shutil.rmtree, bin_path, ignore_errors=True)

datas = []
datas += collect_data_files("flet.controls.material", includes=["icons.json"])
datas += collect_data_files(
    "flet.controls.cupertino", includes=["cupertino_icons.json"]
)

if bin_path:
    datas.append((bin_path, "flet_desktop/app"))
