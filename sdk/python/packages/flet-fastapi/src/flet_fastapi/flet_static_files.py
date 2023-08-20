import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Tuple

import flet_fastapi
from fastapi.staticfiles import StaticFiles
from flet_core import WebRenderer
from flet_fastapi.flet_app_manager import flet_app_manager
from flet_runtime.utils import (
    get_package_web_dir,
    patch_index_html,
    patch_manifest_json,
)

logger = logging.getLogger(flet_fastapi.__name__)


class FletStaticFiles(StaticFiles):
    """Acts similar to the bripkens/connect-history-api-fallback
    NPM package."""

    def __init__(
        self,
        assets_dir: Optional[str] = None,
        app_mount_path: Optional[str] = None,
        app_name: Optional[str] = None,
        app_short_name: Optional[str] = None,
        app_description: Optional[str] = None,
        web_renderer: WebRenderer = WebRenderer.CANVAS_KIT,
        use_color_emoji: bool = False,
        route_url_strategy: str = "path",
        websocket_endpoint_path: Optional[str] = None,
    ) -> None:
        self.index = "index.html"
        self.manifest_json = "manifest.json"

        # where modified index.html is stored
        temp_dir = tempfile.mkdtemp()
        flet_app_manager.add_temp_dir(temp_dir)
        logger.info(f"Temp dir created for patched index and manifest: {temp_dir}")

        # "standard" web files
        web_dir = get_package_web_dir()
        logger.info(f"Web root: {web_dir}")

        # user-defined assets
        if assets_dir:
            if not Path(assets_dir).is_absolute():
                raise Exception("assets_dir must be absolute path.")
            elif not os.path.exists(assets_dir):
                raise Exception(f"assets_dir does not exists: {assets_dir}")

        logger.info(f"Assets dir: {assets_dir}")

        # copy index.html from assets_dir or web_dir
        if assets_dir and os.path.exists(os.path.join(assets_dir, self.index)):
            shutil.copyfile(
                os.path.join(assets_dir, self.index),
                os.path.join(temp_dir, self.index),
            )
        else:
            shutil.copyfile(
                os.path.join(web_dir, self.index),
                os.path.join(temp_dir, self.index),
            )

        # copy manifest.json from assets_dir or web_dir
        if assets_dir and os.path.exists(os.path.join(assets_dir, self.manifest_json)):
            shutil.copyfile(
                os.path.join(assets_dir, self.manifest_json),
                os.path.join(temp_dir, self.manifest_json),
            )
        else:
            shutil.copyfile(
                os.path.join(web_dir, self.manifest_json),
                os.path.join(temp_dir, self.manifest_json),
            )

        # replace variables in index.html and manifest.json
        patch_index_html(
            index_path=os.path.join(temp_dir, self.index),
            base_href=app_mount_path,
            websocket_endpoint_path=websocket_endpoint_path,
            app_name=app_name,
            app_description=app_description,
            web_renderer=WebRenderer(web_renderer),
            use_color_emoji=use_color_emoji,
            route_url_strategy=route_url_strategy,
        )

        patch_manifest_json(
            manifest_path=os.path.join(temp_dir, self.manifest_json),
            app_name=app_name,
            app_short_name=app_short_name,
            app_description=app_description,
        )

        # set html=True to resolve the index even when no
        # the base path is passed in
        super().__init__(directory=temp_dir, packages=None, html=True, check_dir=True)

        # add the rest of dirs
        if assets_dir:
            self.all_directories.append(assets_dir)

        self.all_directories.append(web_dir)

    def lookup_path(self, path: str) -> Tuple[str, Optional[os.stat_result]]:
        """Returns the index file when no match is found.

        Args:
            path (str): Resource path.

        Returns:
            [tuple[str, os.stat_result]]: Always retuens a full path and stat result.
        """
        full_path, stat_result = super().lookup_path(path)

        # if a file cannot be found
        if stat_result is None:
            return super().lookup_path(self.index)

        return (full_path, stat_result)
