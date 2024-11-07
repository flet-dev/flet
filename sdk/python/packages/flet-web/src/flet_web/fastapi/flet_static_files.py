import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Tuple

import flet_web.fastapi as flet_fastapi
from fastapi.staticfiles import StaticFiles
from flet.core.types import WebRenderer
from flet.utils import Once, get_bool_env_var
from flet_web import get_package_web_dir, patch_index_html, patch_manifest_json
from flet_web.fastapi.flet_app_manager import app_manager
from starlette.types import Receive, Scope, Send

logger = logging.getLogger(flet_fastapi.__name__)


class FletStaticFiles(StaticFiles):
    """
    Serve Flet app static files.

    Parameters:

    * `app_mount_path` (str) - absolute URL of Flet app. Default is `/`.
    * `assets_dir` (str, optional) - an absolute path to app's assets directory.
    * `app_name` (str, optional) - PWA application name.
    * `app_short_name` (str, optional) - PWA application short name.
    * `app_description` (str, optional) - PWA application description.
    * `web_renderer` (WebRenderer) - web renderer defaulting to `WebRenderer.CANVAS_KIT`.
    * `use_color_emoji` (bool) - whether to load a font with color emoji. Default is `False`.
    * `route_url_strategy` (str) - routing URL strategy: `path` (default) or `hash`.
    * `websocket_endpoint_path` (str, optional) - absolute URL of Flet app WebSocket handler. Default is `{app_mount_path}/ws`.
    """

    def __init__(
        self,
        proxy_path: Optional[str] = None,
        assets_dir: Optional[str] = None,
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
        self.__proxy_path = proxy_path
        self.__assets_dir = assets_dir
        self.__app_name = app_name
        self.__app_short_name = app_short_name
        self.__app_description = app_description
        self.__web_renderer = web_renderer
        self.__use_color_emoji = use_color_emoji
        self.__route_url_strategy = route_url_strategy
        self.__websocket_endpoint_path = websocket_endpoint_path
        self.__once = Once()

        env_web_renderer = os.getenv("FLET_WEB_RENDERER")
        if env_web_renderer:
            self.__web_renderer = WebRenderer(env_web_renderer)

        env_use_color_emoji = get_bool_env_var("FLET_WEB_USE_COLOR_EMOJI")
        if env_use_color_emoji is not None:
            self.__use_color_emoji = env_use_color_emoji

        env_route_url_strategy = os.getenv("FLET_WEB_ROUTE_URL_STRATEGY")
        if env_route_url_strategy:
            self.__route_url_strategy = env_route_url_strategy

        logger.info(f"Web renderer configured: {self.__web_renderer}")
        logger.info(f"Use color emoji: {self.__use_color_emoji}")
        logger.info(f"Route URL strategy configured: {self.__route_url_strategy}")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.__once.do(self.__config, scope["root_path"])
        await super().__call__(scope, receive, send)

    def lookup_path(self, path: str) -> Tuple[str, Optional[os.stat_result]]:
        """Returns the index file when no match is found.

        Args:
            path (str): Resource path.

        Returns:
            [tuple[str, os.stat_result]]: Always retuens a full path and stat result.
        """
        logger.debug(f"StaticFiles.lookup_path: {self.__app_mount_path} {path}")
        full_path, stat_result = super().lookup_path(path)

        # if a file cannot be found
        if stat_result is None:
            return super().lookup_path(self.index)

        return full_path, stat_result

    async def __config(self, root_path: str):
        if self.__proxy_path:
            self.__app_mount_path = self.__proxy_path + root_path
        else:
            self.__app_mount_path = root_path

        # where modified index.html is stored
        temp_dir = tempfile.mkdtemp()
        app_manager.add_temp_dir(temp_dir)
        logger.info(f"Temp dir created for patched index and manifest: {temp_dir}")

        # "standard" web files
        web_dir = get_package_web_dir()
        logger.info(f"Web root: {web_dir}")

        if not os.path.exists(web_dir):
            raise Exception(f"Web root path not found: {web_dir}")

        # user-defined assets
        if self.__assets_dir:
            if not Path(self.__assets_dir).is_absolute():
                logger.warning("assets_dir must be absolute path.")
                self.__assets_dir = None
            elif not os.path.exists(self.__assets_dir):
                logger.info(f"assets_dir does not exist: {self.__assets_dir}")
                self.__assets_dir = None

        logger.info(f"Assets dir: {self.__assets_dir}")

        # copy index.html from assets_dir or web_dir
        if self.__assets_dir and os.path.exists(
            os.path.join(self.__assets_dir, self.index)
        ):
            shutil.copyfile(
                os.path.join(self.__assets_dir, self.index),
                os.path.join(temp_dir, self.index),
            )
        else:
            shutil.copyfile(
                os.path.join(web_dir, self.index),
                os.path.join(temp_dir, self.index),
            )

        # copy manifest.json from assets_dir or web_dir
        if self.__assets_dir and os.path.exists(
            os.path.join(self.__assets_dir, self.manifest_json)
        ):
            shutil.copyfile(
                os.path.join(self.__assets_dir, self.manifest_json),
                os.path.join(temp_dir, self.manifest_json),
            )
        else:
            shutil.copyfile(
                os.path.join(web_dir, self.manifest_json),
                os.path.join(temp_dir, self.manifest_json),
            )

        ws_path = self.__websocket_endpoint_path
        if not ws_path:
            ws_path = self.__app_mount_path.strip("/")
            ws_path = f"{'' if ws_path == '' else '/'}{ws_path}/ws"

        # replace variables in index.html and manifest.json
        patch_index_html(
            index_path=os.path.join(temp_dir, self.index),
            base_href=self.__app_mount_path,
            websocket_endpoint_path=ws_path,
            app_name=self.__app_name,
            app_description=self.__app_description,
            web_renderer=WebRenderer(self.__web_renderer),
            use_color_emoji=self.__use_color_emoji,
            route_url_strategy=self.__route_url_strategy,
        )

        patch_manifest_json(
            manifest_path=os.path.join(temp_dir, self.manifest_json),
            app_name=self.__app_name,
            app_short_name=self.__app_short_name,
            app_description=self.__app_description,
        )

        # set html=True to resolve the index even when no
        # the base path is passed in
        super().__init__(directory=temp_dir, packages=None, html=True, check_dir=True)

        # add the rest of dirs
        if self.__assets_dir:
            self.all_directories.append(self.__assets_dir)

        self.all_directories.append(web_dir)
