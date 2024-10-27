import os

import flet.__pyinstaller.config as hook_config
from flet.__pyinstaller.utils import get_flet_bin_path

bin_path = hook_config.temp_bin_dir
if not bin_path:
    bin_path = get_flet_bin_path()

if bin_path:
    # package "bin/fletd" only
    if os.getenv("PACKAGE_FLETD_ONLY"):
        bin_path = os.path.join(bin_path, "fletd*")

    datas = [(bin_path, "flet/bin")]
