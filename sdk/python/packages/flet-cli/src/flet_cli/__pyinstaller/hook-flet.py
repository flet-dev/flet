import os

import flet_cli.__pyinstaller.config as hook_config
from flet_cli.__pyinstaller.utils import get_flet_bin_path

bin_path = hook_config.temp_bin_dir
if not bin_path:
    bin_path = get_flet_bin_path()

if bin_path:
    datas = [(bin_path, "flet_desktop/app")]
