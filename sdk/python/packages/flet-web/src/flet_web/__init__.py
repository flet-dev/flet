import os
from pathlib import Path

from flet_web.patch_index import (
    patch_font_manifest_json,
    patch_index_html,
    patch_manifest_json,
)


def get_package_web_dir():
    """
    Returns directory containing bundled web runtime assets.

    If `FLET_WEB_PATH` environment variable is set, its value is returned.
    Otherwise, the package-local `web` directory is used.
    """

    web_root_dir = os.environ.get("FLET_WEB_PATH")
    return web_root_dir or str(Path(__file__).parent.joinpath("web"))


__all__ = [
    "get_package_web_dir",
    "patch_font_manifest_json",
    "patch_index_html",
    "patch_manifest_json",
]
