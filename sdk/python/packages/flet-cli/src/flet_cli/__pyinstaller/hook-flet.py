from PyInstaller.utils.hooks import collect_data_files

import flet_cli.__pyinstaller.config as hook_config
from flet_cli.__pyinstaller.utils import get_flet_bin_path

bin_path = hook_config.temp_bin_dir
if not bin_path:
    bin_path = get_flet_bin_path()

datas = []
datas += collect_data_files("flet.controls.material", includes=["icons.json"])
datas += collect_data_files(
    "flet.controls.cupertino", includes=["cupertino_icons.json"]
)

if bin_path:
    datas.append((bin_path, "flet_desktop/app"))
