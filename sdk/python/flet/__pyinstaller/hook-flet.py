import os

import flet.__pyinstaller.config as hook_config

# raise Exception(f"icon_file: {hook_config.icon_file}")

# package entire "bin" folder
bin_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "bin"))

# package "bin/fletd" only
if os.getenv("PACKAGE_FLETD_ONLY"):
    bin_path = os.path.join(bin_path, "fletd*")

datas = [(bin_path, "flet/bin")]
