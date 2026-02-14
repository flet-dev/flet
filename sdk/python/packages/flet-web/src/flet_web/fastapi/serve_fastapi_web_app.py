import asyncio
import logging
from typing import Any, Optional, Union

import uvicorn

import flet_web.fastapi
import flet_web.fastapi as flet_fastapi
from flet.controls.types import RouteUrlStrategy, WebRenderer

logger = logging.getLogger(flet_fastapi.__name__)


class WebServerHandle:
    """
    Runtime handle for a started FastAPI web server task.
    """

    def __init__(
        self, page_url: str, server: uvicorn.Server, serve_task: asyncio.Task
    ) -> None:
        self.page_url = page_url
        self.server = server
        self.serve_task = serve_task

    async def close(self):
        """
        Gracefully shut down the underlying Uvicorn server.
        """

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
    """
    Build and return a FastAPI app with a mounted Flet web application.

    Args:
        main: Flet app entry handler.
        before_main: Optional hook called before `main`.
        page_name: URL path prefix where app is mounted.
        assets_dir: Absolute path to static assets directory.
        upload_dir: Absolute path used for uploads.
        web_renderer: Flutter web renderer mode.
        route_url_strategy: Route URL strategy (`path` or `hash`).
        no_cdn: Whether CDN resources should be disabled.

    Returns:
        Configured FastAPI application instance.
    """

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
    """
    Start a mounted Flet FastAPI app with Uvicorn and return a server handle.

    Args:
        main: Flet app entry handler.
        before_main: Optional hook called before `main`.
        host: Interface to bind the server to.
        url_host: Host used to compose externally displayed page URL.
        port: TCP port to bind.
        page_name: URL path prefix where app is mounted.
        assets_dir: Absolute path to static assets directory.
        upload_dir: Absolute path used for uploads.
        web_renderer: Flutter web renderer mode.
        route_url_strategy: Route URL strategy (`path` or `hash`).
        no_cdn: Whether CDN resources should be disabled.
        on_startup: Optional callback invoked with resolved page URL.
        log_level: Uvicorn log level.

    Returns:
        `WebServerHandle` for controlling server lifecycle.
    """

    web_path = f"/{page_name.strip('/')}"
    page_url = f"http://{url_host}:{port}{web_path if web_path != '/' else ''}"

    def startup():
        """
        Invoke optional startup callback with resolved page URL.
        """

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
