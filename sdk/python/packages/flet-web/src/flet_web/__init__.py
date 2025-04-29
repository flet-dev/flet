import os
from pathlib import Path

from flet_web.patch_index import (
    patch_font_manifest_json as patch_font_manifest_json,
)
from flet_web.patch_index import (
    patch_index_html as patch_index_html,
)
from flet_web.patch_index import (
    patch_manifest_json as patch_manifest_json,
)


def get_package_web_dir():
    web_root_dir = os.environ.get("FLET_WEB_PATH")
    return web_root_dir or str(Path(__file__).parent.joinpath("web"))
