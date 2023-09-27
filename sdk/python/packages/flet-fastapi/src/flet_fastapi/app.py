from typing import Awaitable, Callable, Optional

from fastapi import Request, WebSocket
from flet import WebRenderer
from flet_core.page import Page
from flet_fastapi.flet_app import (
    DEFAULT_FLET_OAUTH_STATE_TIMEOUT,
    DEFAULT_FLET_SESSION_TIMEOUT,
    FletApp,
)
from flet_fastapi.flet_fastapi import FastAPI
from flet_fastapi.flet_oauth import FletOAuth
from flet_fastapi.flet_static_files import FletStaticFiles
from flet_fastapi.flet_upload import FletUpload


def app(
    session_handler: Callable[[Page], Awaitable],
    proxy_path: Optional[str] = None,
    assets_dir: Optional[str] = None,
    app_name: Optional[str] = None,
    app_short_name: Optional[str] = None,
    app_description: Optional[str] = None,
    web_renderer: WebRenderer = WebRenderer.CANVAS_KIT,
    use_color_emoji: bool = False,
    route_url_strategy: str = "path",
    upload_dir: Optional[str] = None,
    max_upload_size: Optional[int] = None,
    secret_key: Optional[str] = None,
    session_timeout_seconds: int = DEFAULT_FLET_SESSION_TIMEOUT,
    oauth_state_timeout_seconds: int = DEFAULT_FLET_OAUTH_STATE_TIMEOUT,
):
    """
    Mount all Flet FastAPI handlers in one call.

    Parameters:
    * `fastapi_app` (FastAPI) - FastAPI application instance.
    * `session_handler` (Coroutine) - application entry point - an async method called for newly connected user. Handler coroutine must have 1 parameter: `page` - `Page` instance.
    * `assets_dir` (str, optional) - an absolute path to app's assets directory.
    * `app_name` (str, optional) - PWA application name.
    * `app_short_name` (str, optional) - PWA application short name.
    * `app_description` (str, optional) - PWA application description.
    * `web_renderer` (WebRenderer) - web renderer defaulting to `WebRenderer.CANVAS_KIT`.
    * `use_color_emoji` (bool) - whether to load a font with color emoji. Default is `False`.
    * `route_url_strategy` (str) - routing URL strategy: `path` (default) or `hash`.
    * `upload_dir` (str) - an absolute path to a directory with uploaded files.
    * `max_upload_size` (str, int) - maximum size of a single upload, bytes. Unlimited if `None`.
    * `secret_key` (str, optional) - secret key to sign and verify upload requests.
    * `session_timeout_seconds` (int, optional)- session lifetime, in seconds, after user disconnected.
    * `oauth_state_timeout_seconds` (int, optional) - OAuth state lifetime, in seconds, which is a maximum allowed time between starting OAuth flow and redirecting to OAuth callback URL.
    """

    fastapi_app = FastAPI()

    @fastapi_app.websocket("/ws")
    async def app_handler(websocket: WebSocket):
        await FletApp(
            session_handler,
            session_timeout_seconds=session_timeout_seconds,
            oauth_state_timeout_seconds=oauth_state_timeout_seconds,
            secret_key=secret_key,
        ).handle(websocket)

    if upload_dir:

        @fastapi_app.put("/upload")
        async def upload_handler(request: Request):
            if not upload_dir:
                return
            await FletUpload(
                upload_dir=upload_dir,
                max_upload_size=max_upload_size,
                secret_key=secret_key,
            ).handle(request)

    @fastapi_app.get("/oauth_callback")
    async def oauth_redirect_handler(request: Request):
        return await FletOAuth().handle(request)

    fastapi_app.mount(
        path="/",
        app=FletStaticFiles(
            proxy_path=proxy_path,
            assets_dir=assets_dir,
            app_name=app_name,
            app_short_name=app_short_name,
            app_description=app_description,
            web_renderer=web_renderer,
            use_color_emoji=use_color_emoji,
            route_url_strategy=route_url_strategy,
        ),
    )

    return fastapi_app
