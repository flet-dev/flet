import asyncio
import logging
from typing import Any, Optional, Union

import uvicorn
from flet.controls.types import RouteUrlStrategy, WebRenderer

import flet_web.fastapi
import flet_web.fastapi as flet_fastapi

logger = logging.getLogger(flet_fastapi.__name__)


class WebServerHandle:
    def __init__(
        self, page_url: str, server: uvicorn.Server, serve_task: asyncio.Task
    ) -> None:
        self.page_url = page_url
        self.server = server
        self.serve_task = serve_task

    async def close(self):
        logger.info("Closing Flet web server...")
        await self.server.shutdown()


def get_fastapi_web_app(
    main,
    before_main,
    page_name: str,
    assets_dir: str,
    upload_dir: str,
    web_renderer: WebRenderer = WebRenderer.AUTO,
    route_url_strategy: RouteUrlStrategy = RouteUrlStrategy.PATH,
    no_cdn: bool = False,
):
    web_path = f"/{page_name.strip('/')}"
    app = flet_web.fastapi.FastAPI()
    app.mount(
        web_path,
        flet_web.fastapi.app(
            main,
            before_main=before_main,
            upload_dir=upload_dir,
            assets_dir=assets_dir,
            web_renderer=web_renderer,
            route_url_strategy=route_url_strategy,
            no_cdn=no_cdn,
        ),
    )

    return app


async def serve_fastapi_web_app(
    main,
    before_main,
    host: str,
    url_host: str,
    port: int,
    page_name: str,
    assets_dir: str,
    upload_dir: str,
    web_renderer: WebRenderer = WebRenderer.AUTO,
    route_url_strategy: RouteUrlStrategy = RouteUrlStrategy.PATH,
    no_cdn: bool = False,
    on_startup: Optional[Any] = None,
    log_level: Optional[Union[str, int]] = None,
) -> WebServerHandle:
    web_path = f"/{page_name.strip('/')}"
    page_url = f"http://{url_host}:{port}{web_path if web_path != '/' else ''}"

    def startup():
        if on_startup:
            on_startup(page_url)

    app = flet_web.fastapi.FastAPI(on_startup=[startup])

    app.mount(
        web_path,
        flet_web.fastapi.app(
            main,
            before_main=before_main,
            upload_dir=upload_dir,
            assets_dir=assets_dir,
            web_renderer=web_renderer,
            route_url_strategy=route_url_strategy,
            no_cdn=no_cdn,
        ),
    )
    config = uvicorn.Config(
        app, host=host, port=port, log_level=log_level, ws="websockets-sansio"
    )
    server = uvicorn.Server(config)

    return WebServerHandle(
        page_url=page_url, server=server, serve_task=asyncio.create_task(server.serve())
    )
