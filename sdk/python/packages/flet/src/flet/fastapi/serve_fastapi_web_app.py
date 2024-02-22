import asyncio
import logging
from typing import Optional

import flet.fastapi
import flet.fastapi as flet_fastapi
import uvicorn
from flet_core.types import WebRenderer

logger = logging.getLogger(flet_fastapi.__name__)


class WebServerHandle:
    def __init__(self, page_url: str, server: uvicorn.Server) -> None:
        self.page_url = page_url
        self.server = server

    async def close(self):
        logger.info("Closing Flet web server...")
        await self.server.shutdown()


def get_fastapi_web_app(
    session_handler,
    page_name: str,
    assets_dir,
    upload_dir,
    web_renderer: Optional[WebRenderer],
    use_color_emoji,
    route_url_strategy,
):
    web_path = f"/{page_name.strip('/')}"
    app = flet.fastapi.FastAPI()
    app.mount(
        web_path,
        flet.fastapi.app(
            session_handler,
            upload_dir=upload_dir,
            assets_dir=assets_dir,
            web_renderer=web_renderer if web_renderer else WebRenderer.AUTO,
            use_color_emoji=use_color_emoji,
            route_url_strategy=route_url_strategy,
        ),
    )

    return app


async def serve_fastapi_web_app(
    session_handler,
    host,
    url_host,
    port,
    page_name: str,
    assets_dir,
    upload_dir,
    web_renderer: Optional[WebRenderer],
    use_color_emoji,
    route_url_strategy,
    blocking,
    on_startup,
    log_level,
):

    web_path = f"/{page_name.strip('/')}"
    page_url = f"http://{url_host}:{port}{web_path if web_path != '/' else ''}"

    def startup():
        if on_startup:
            on_startup(page_url)

    app = flet.fastapi.FastAPI(on_startup=[startup])

    app.mount(
        web_path,
        flet.fastapi.app(
            session_handler,
            upload_dir=upload_dir,
            assets_dir=assets_dir,
            web_renderer=web_renderer if web_renderer else WebRenderer.AUTO,
            use_color_emoji=use_color_emoji,
            route_url_strategy=route_url_strategy,
        ),
    )
    config = uvicorn.Config(app, host=host, port=port, log_level=log_level)
    server = uvicorn.Server(config)

    if blocking:
        await server.serve()
    else:
        asyncio.create_task(server.serve())

    return WebServerHandle(page_url=page_url, server=server)
