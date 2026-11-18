import os

from PyInstaller.config import CONF
from PyInstaller.utils.hooks import collect_data_files

import flet_cli.__pyinstaller.config as hook_config
from flet_cli.__pyinstaller.utils import archive_flet_bin

client_files = hook_config.client_files
if client_files is None:
    # A plain `pyinstaller` run, not `flet pack`: bundle the client archive
    # so the app doesn't download the client on its first start. It is kept
    # in the work directory, next to the cached analysis that lists it.
    client_files = archive_flet_bin(os.path.join(CONF["workpath"], "flet-client"))

datas = []
datas += collect_data_files("flet.controls.material", includes=["icons.json"])
datas += collect_data_files(
    "flet.controls.cupertino", includes=["cupertino_icons.json"]
)

for path in client_files or []:
    datas.append((path, "flet_desktop/app"))
