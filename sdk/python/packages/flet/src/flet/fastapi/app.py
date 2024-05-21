import asyncio
import os
from typing import Awaitable, Callable, Optional, Union

from fastapi import Request, WebSocket
from flet.fastapi.flet_app import (
    DEFAULT_FLET_OAUTH_STATE_TIMEOUT,
    DEFAULT_FLET_SESSION_TIMEOUT,
    FletApp,
)
from flet.fastapi.flet_fastapi import FastAPI
from flet.fastapi.flet_oauth import FletOAuth
from flet.fastapi.flet_static_files import FletStaticFiles
from flet.fastapi.flet_upload import FletUpload
from flet_core.page import Page
from flet_core.types import WebRenderer


def app(
    session_handler: Union[Callable[[Page], Awaitable], Callable[[Page], None]],
    proxy_path: Optional[str] = None,
    assets_dir: Optional[str] = None,
    app_name: Optional[str] = None,
    app_short_name: Optional[str] = None,
    app_description: Optional[str] = None,
    web_renderer: WebRenderer = WebRenderer.CANVAS_KIT,
    use_color_emoji: bool = False,
    route_url_strategy: str = "path",
    upload_dir: Optional[str] = None,
    upload_endpoint_path: Optional[str] = None,
    max_upload_size: Optional[int] = None,
    secret_key: Optional[str] = None,
    session_timeout_seconds: int = DEFAULT_FLET_SESSION_TIMEOUT,
    oauth_state_timeout_seconds: int = DEFAULT_FLET_OAUTH_STATE_TIMEOUT,
):
    """
    Mount all Flet FastAPI handlers in one call.

    Parameters:
    * `session_handler` (function or coroutine) - application entry point - a method called for newly connected user. Handler must have 1 parameter: `page` - `Page` instance.
    * `assets_dir` (str, optional) - an absolute path to app's assets directory.
    * `app_name` (str, optional) - PWA application name.
    * `app_short_name` (str, optional) - PWA application short name.
    * `app_description` (str, optional) - PWA application description.
    * `web_renderer` (WebRenderer) - web renderer defaulting to `WebRenderer.CANVAS_KIT`.
    * `use_color_emoji` (bool) - whether to load a font with color emoji. Default is `False`.
    * `route_url_strategy` (str) - routing URL strategy: `path` (default) or `hash`.
    * `upload_dir` (str) - an absolute path to a directory with uploaded files.
    * `upload_endpoint_path` (str, optional) - absolute URL of upload endpoint, e.g. `/upload`.
    * `max_upload_size` (str, int) - maximum size of a single upload, bytes. Unlimited if `None`.
    * `secret_key` (str, optional) - secret key to sign and verify upload requests.
    * `session_timeout_seconds` (int, optional)- session lifetime, in seconds, after user disconnected.
    * `oauth_state_timeout_seconds` (int, optional) - OAuth state lifetime, in seconds, which is a maximum allowed time between starting OAuth flow and redirecting to OAuth callback URL.
    """

    env_upload_dir = os.getenv("FLET_UPLOAD_DIR")
    if env_upload_dir:
        upload_dir = env_upload_dir

    env_websocket_endpoint = os.getenv("FLET_WEBSOCKET_HANDLER_ENDPOINT")
    websocket_endpoint = (
        "ws" if not env_websocket_endpoint else env_websocket_endpoint.strip("/")
    )

    env_upload_endpoint = os.getenv("FLET_UPLOAD_HANDLER_ENDPOINT")
    upload_endpoint = (
        "upload" if not env_upload_endpoint else env_upload_endpoint.strip("/")
    )

    env_oauth_callback_endpoint = os.getenv("FLET_OAUTH_CALLBACK_HANDLER_ENDPOINT")
    oauth_callback_endpoint = (
        "oauth_callback"
        if not env_oauth_callback_endpoint
        else env_oauth_callback_endpoint.strip("/")
    )

    fastapi_app = FastAPI()

    @fastapi_app.websocket(f"/{websocket_endpoint}")
    async def app_handler(websocket: WebSocket):
        await FletApp(
            asyncio.get_running_loop(),
            session_handler,
            session_timeout_seconds=session_timeout_seconds,
            oauth_state_timeout_seconds=oauth_state_timeout_seconds,
            upload_endpoint_path=upload_endpoint_path,
            secret_key=secret_key,
        ).handle(websocket)

    if upload_dir:

        @fastapi_app.put(
            f"/{upload_endpoint_path if upload_endpoint_path else upload_endpoint}"
        )
        async def upload_handler(request: Request):
            await FletUpload(
                upload_dir=upload_dir,
                max_upload_size=max_upload_size,
                secret_key=secret_key,
            ).handle(request)

    @fastapi_app.get(f"/{oauth_callback_endpoint}")
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
