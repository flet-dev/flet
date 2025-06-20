import asyncio
import os
from collections.abc import Awaitable
from typing import Callable, Optional, Union

from fastapi import Request, WebSocket
from flet.controls.page import Page
from flet.controls.types import RouteUrlStrategy, WebRenderer
from starlette.middleware.base import BaseHTTPMiddleware

from flet_web.fastapi.flet_app import (
    DEFAULT_FLET_OAUTH_STATE_TIMEOUT,
    DEFAULT_FLET_SESSION_TIMEOUT,
    FletApp,
    app_manager,
)
from flet_web.fastapi.flet_fastapi import FastAPI
from flet_web.fastapi.flet_oauth import FletOAuth
from flet_web.fastapi.flet_static_files import FletStaticFiles
from flet_web.fastapi.flet_upload import FletUpload


def app(
    main: Union[Callable[[Page], Awaitable], Callable[[Page], None]],
    before_main: Union[Callable[[Page], Awaitable], Callable[[Page], None]],
    proxy_path: Optional[str] = None,
    assets_dir: Optional[str] = None,
    app_name: Optional[str] = None,
    app_short_name: Optional[str] = None,
    app_description: Optional[str] = None,
    web_renderer: WebRenderer = WebRenderer.AUTO,
    route_url_strategy: RouteUrlStrategy = RouteUrlStrategy.PATH,
    no_cdn: bool = False,
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
    * `main` (function or coroutine) - application entry point - a method
       called for newly connected user. Handler must have 1 parameter: `page` - `Page`
       instance.
    * `before_main` - a function that is called after Page was created, but before
       calling `main`.
    * `assets_dir` (str, optional) - an absolute path to app's assets directory.
    * `app_name` (str, optional) - PWA application name.
    * `app_short_name` (str, optional) - PWA application short name.
    * `app_description` (str, optional) - PWA application description.
    * `web_renderer` (WebRenderer) - web renderer defaulting to `WebRenderer.AUTO`.
    * `route_url_strategy` (str) - routing URL strategy: `path` (default) or `hash`.
    * `no_cdn` (bool) - do not load resources from CDN.
    * `upload_dir` (str) - an absolute path to a directory with uploaded files.
    * `upload_endpoint_path` (str, optional) - absolute URL of upload endpoint,
       e.g. `/upload`.
    * `max_upload_size` (str, int) - maximum size of a single upload, bytes.
       Unlimited if `None`.
    * `secret_key` (str, optional) - secret key to sign and verify upload requests.
    * `session_timeout_seconds` (int, optional)- session lifetime, in seconds, after
       user disconnected.
    * `oauth_state_timeout_seconds` (int, optional) - OAuth state lifetime, in seconds,
       which is a maximum allowed time between starting OAuth flow and redirecting
       to OAuth callback URL.
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
            loop=asyncio.get_running_loop(),
            executor=app_manager.executor,
            main=main,
            before_main=before_main,
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
            route_url_strategy=route_url_strategy,
            websocket_endpoint_path=websocket_endpoint,
            no_cdn=no_cdn,
        ),
    )

    # Add middleware for custom headers
    class CustomHeadersMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            response = await call_next(request)
            response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
            response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response

    fastapi_app.add_middleware(CustomHeadersMiddleware)

    return fastapi_app
