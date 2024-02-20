import asyncio
from asyncio import Task
from typing import Optional

import flet.fastapi
import uvicorn
from flet_core.types import WebRenderer


class WebServerHandle:
    def __init__(self, page_url: str, server: uvicorn.Server) -> None:
        self.page_url = page_url
        self.server = server

    async def close(self):
        await self.server.shutdown()


async def start_fastapi_web_app(
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
    log_level,
):
    app = flet.fastapi.FastAPI()
    web_path = f"/{page_name.strip('/')}"
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
    asyncio.create_task(server.serve())

    return WebServerHandle(
        page_url=f"http://{url_host}:{port}{web_path if web_path != '/' else ''}",
        server=server,
    )
