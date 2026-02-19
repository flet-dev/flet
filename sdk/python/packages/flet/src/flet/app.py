import asyncio
import concurrent.futures
import contextlib
import inspect
import logging
import os
import signal
import traceback
from collections.abc import Awaitable
from pathlib import Path
from typing import Any, Callable, Optional, Union

from flet.controls.context import _context_page, context
from flet.controls.page import Page
from flet.controls.types import AppView, RouteUrlStrategy, WebRenderer
from flet.messaging.session import Session
from flet.utils import (
    get_bool_env_var,
    get_current_script_dir,
    get_free_tcp_port,
    is_embedded,
    is_linux_server,
    is_pyodide,
    open_in_browser,
)
from flet.utils.deprecated import deprecated
from flet.utils.pip import (
    ensure_flet_desktop_package_installed,
    ensure_flet_web_package_installed,
)

logger = logging.getLogger("flet")

AppCallable = Callable[[Page], Union[Any, Awaitable[Any]]]
"""Type alias for Flet app lifecycle callbacks.

Represents a callable (synchronous or asynchronous) that accepts a single argument of
type [`Page`][flet.]. The return value is ignored.

Used for both `main` and `before_main` handlers.
"""


@deprecated("Use run() instead.", version="0.80.0", show_parentheses=True)
def app(*args, **kwargs):
    new_args = list(args)
    if "target" in kwargs:
        new_args.insert(0, kwargs["target"])
    return run(*new_args, **kwargs)


@deprecated("Use run() instead.", version="0.80.0", show_parentheses=True)
def app_async(*args, **kwargs):
    new_args = list(args)
    if "target" in kwargs:
        new_args.insert(0, kwargs["target"])
    return run_async(*new_args, **kwargs)


def run(
    main: AppCallable,
    before_main: Optional[AppCallable] = None,
    name: str = "",
    host: Optional[str] = None,
    port: int = 0,
    view: Optional[AppView] = AppView.FLET_APP,
    assets_dir: Optional[str] = "assets",
    upload_dir: Optional[str] = None,
    web_renderer: WebRenderer = WebRenderer.AUTO,
    route_url_strategy: RouteUrlStrategy = RouteUrlStrategy.PATH,
    no_cdn: Optional[bool] = False,
    export_asgi_app: Optional[bool] = False,
    target=None,
):
    """
    Runs the Flet app.

    Args:
        main: Application entry point. Handler (function or coroutine) must
            have 1 parameter of instance [`Page`][flet.Page].
        before_main: Called after `Page` is created but before `main`.
        name: Page/app name used in web URL path when applicable.
        host: Host/IP to bind the web server to.
        port: TCP port to bind. If `0`, an available port is chosen when needed.
        view: Preferred app presentation mode.
        assets_dir: A path to app's assets directory.
        upload_dir: A path to a directory with uploaded files,
            or where uploaded files should be saved.
        web_renderer: The type of web renderer to use.
        route_url_strategy: The strategy to use for generating URLs.
        no_cdn: Whether not load CanvasKit, Pyodide, or fonts from CDN.
        export_asgi_app: If `True`, returns a configured ASGI app instead of
            running an event loop.
        target: Deprecated alias for `main`.

    Returns:
        When `export_asgi_app=True`, returns a FastAPI ASGI app.
            Otherwise, runs the app and returns `None`.
    """
    if is_pyodide():
        __run_pyodide(main=main or target, before_main=before_main)
        return

    if export_asgi_app:
        ensure_flet_web_package_installed()
        from flet_web.fastapi.serve_fastapi_web_app import get_fastapi_web_app

        return get_fastapi_web_app(
            main=main or target,
            before_main=before_main,
            page_name=__get_page_name(name),
            assets_dir=__get_assets_dir_path(assets_dir, relative_to_cwd=True),
            upload_dir=__get_upload_dir_path(upload_dir, relative_to_cwd=True),
            web_renderer=web_renderer,
            route_url_strategy=route_url_strategy,
            no_cdn=no_cdn,
        )

    if isinstance(web_renderer, str):
        web_renderer = WebRenderer(web_renderer)

    if isinstance(route_url_strategy, str):
        route_url_strategy = RouteUrlStrategy(route_url_strategy)

    return asyncio.run(
        run_async(
            main=main or target,
            before_main=before_main,
            name=name,
            host=host,
            port=port,
            view=view,
            assets_dir=assets_dir,
            upload_dir=upload_dir,
            web_renderer=web_renderer,
            route_url_strategy=route_url_strategy,
            no_cdn=no_cdn,
        )
    )


async def run_async(
    main: AppCallable,
    before_main: Optional[AppCallable] = None,
    name: str = "",
    host: Optional[str] = None,
    port: int = 0,
    view: Optional[AppView] = AppView.FLET_APP,
    assets_dir: Optional[str] = "assets",
    upload_dir: Optional[str] = None,
    web_renderer: WebRenderer = WebRenderer.AUTO,
    route_url_strategy: RouteUrlStrategy = RouteUrlStrategy.PATH,
    no_cdn: Optional[bool] = False,
    target=None,
):
    """
    Asynchronously run a Flet app using socket or web server transport.

    Args:
        main: Application entry point. Handler (function or coroutine) must
            have 1 parameter of instance [`Page`][flet.Page].
        before_main: Called after `Page` is created but before `main`.
        name: Page/app name used in web URL path when applicable.
        host: Host/IP to bind the web server to.
        port: TCP port to bind. If `0`, default/free port is selected.
        view: Preferred app presentation mode.
        assets_dir: Path to app assets directory.
        upload_dir: Path to upload directory.
        web_renderer: Web renderer type for web-hosted mode.
        route_url_strategy: Route URL strategy (`path` or `hash`).
        no_cdn: Whether to avoid loading CanvasKit, Pyodide, and fonts from CDN.
        target: Deprecated alias for `main`.
    """

    if is_pyodide():
        __run_pyodide(main=main or target, before_main=before_main)
        return

    if isinstance(view, str):
        view = AppView(view)

    if isinstance(web_renderer, str):
        web_renderer = WebRenderer(web_renderer)

    if isinstance(route_url_strategy, str):
        route_url_strategy = RouteUrlStrategy(route_url_strategy)

    force_web_server = get_bool_env_var("FLET_FORCE_WEB_SERVER") or is_linux_server()
    if force_web_server:
        view = AppView.WEB_BROWSER

    env_port = os.getenv("FLET_SERVER_PORT")
    if env_port is not None and env_port:
        port = int(env_port)

    if port == 0 and force_web_server:
        port = 8000

    env_host = os.getenv("FLET_SERVER_IP")
    if env_host is not None and env_host:
        host = env_host

    assets_dir = __get_assets_dir_path(assets_dir)
    upload_dir = __get_upload_dir_path(upload_dir)
    page_name = __get_page_name(name)

    is_socket_server = (
        is_embedded() or view in [AppView.FLET_APP, AppView.FLET_APP_HIDDEN, None]
    ) and not force_web_server

    url_prefix = os.getenv("FLET_DISPLAY_URL_PREFIX")

    def on_app_startup(page_url: str):
        """
        Handle app-start notification by logging/printing URL and optional browser open.

        Args:
            page_url: Resolved URL of the running app.
        """

        if url_prefix is not None:
            print(url_prefix, page_url)
        else:
            logger.info(f"App URL: {page_url}")

        if view == AppView.WEB_BROWSER and url_prefix is None and not force_web_server:
            open_in_browser(page_url)

    loop = asyncio.get_running_loop()

    terminate = asyncio.Event()

    if not is_embedded():

        def exit_gracefully(signum, frame):
            """
            Signal handler that requests graceful app termination.

            Args:
                signum: Received OS signal number.
                frame: Current stack frame (unused).
            """

            logger.debug("Gracefully terminating Flet app...")
            loop.call_soon_threadsafe(terminate.set)
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            signal.signal(signal.SIGTERM, signal.SIG_DFL)

        signal.signal(signal.SIGINT, exit_gracefully)
        signal.signal(signal.SIGTERM, exit_gracefully)

    conn = (
        await __run_socket_server(
            port=port,
            main=main or target,
            before_main=before_main,
            blocking=is_embedded(),
        )
        if is_socket_server
        else await __run_web_server(
            main=main or target,
            before_main=before_main,
            host=host,
            port=port,
            page_name=page_name,
            assets_dir=assets_dir,
            upload_dir=upload_dir,
            web_renderer=web_renderer,
            route_url_strategy=route_url_strategy,
            no_cdn=no_cdn,
            on_startup=on_app_startup,
        )
    )

    logger.info("Flet app has started...")

    try:
        if (
            (view in [AppView.FLET_APP, AppView.FLET_APP_HIDDEN, AppView.FLET_APP_WEB])
            and not force_web_server
            and not is_embedded()
            and url_prefix is None
        ):
            ensure_flet_desktop_package_installed()
            from flet_desktop import close_flet_view, open_flet_view_async

            on_app_startup(conn.page_url)

            fvp, pid_file = await open_flet_view_async(
                conn.page_url,
                assets_dir if view != AppView.FLET_APP_WEB else None,
                view == AppView.FLET_APP_HIDDEN,
            )
            with contextlib.suppress(Exception):
                await fvp.wait()

            close_flet_view(pid_file)

        elif url_prefix and is_socket_server:
            on_app_startup(conn.page_url)

            with contextlib.suppress(KeyboardInterrupt):
                await terminate.wait()

        elif view == AppView.WEB_BROWSER or view is None or force_web_server:
            with contextlib.suppress(KeyboardInterrupt):
                await terminate.wait()

    finally:
        await conn.close()


def __get_on_session_created(
    main: Optional[AppCallable],
) -> Callable[[Session], Awaitable[None]]:
    """
    Build session-start callback that executes the user `main` handler.

    Args:
        main: User-provided app entry handler.

    Returns:
        Async callback that initializes page context and runs `main`.
    """

    async def on_session_created(session: Session):
        """
        Initialize per-session context and execute app entry handler.

        Args:
            session: Active page session.
        """

        logger.info("App session started")
        try:
            assert main is not None
            _context_page.set(session.page)
            context.reset_auto_update()
            if inspect.iscoroutinefunction(main):
                await main(session.page)

            elif inspect.isasyncgenfunction(main):
                async for _ in main(session.page):
                    await session.after_event(session.page)

            elif inspect.isgeneratorfunction(main):
                for _ in main(session.page):
                    await session.after_event(session.page)
            else:
                # run synchronously
                main(session.page)

            await session.after_event(session.page)

        except Exception as e:
            logger.error("Unhandled error in main() handler", exc_info=True)
            session.error(f"{e}\n{traceback.format_exc()}")

    return on_session_created


async def __run_socket_server(
    port: int = 0,
    main: Optional[AppCallable] = None,
    before_main: Optional[AppCallable] = None,
    blocking: bool = False,
):
    """
    Start Flet socket server transport and return active connection object.

    Args:
        port: TCP port to bind (`0` lets OS choose).
        main: User app entry handler.
        before_main: Optional hook called before `main`.
        blocking: Whether server should run in blocking mode.

    Returns:
        Started socket-server connection instance.
    """

    from flet.messaging.flet_socket_server import FletSocketServer

    uds_path = os.getenv("FLET_SERVER_UDS_PATH")

    executor = concurrent.futures.ThreadPoolExecutor()

    conn = FletSocketServer(
        loop=asyncio.get_running_loop(),
        port=port,
        uds_path=uds_path,
        on_session_created=__get_on_session_created(main),
        before_main=before_main,
        blocking=blocking,
        executor=executor,
    )
    await conn.start()
    return conn


async def __run_web_server(
    main: Optional[AppCallable],
    before_main: Optional[AppCallable],
    host: Optional[str],
    port: int,
    page_name: str,
    assets_dir: str,
    upload_dir: Optional[str],
    web_renderer: Optional[WebRenderer],
    route_url_strategy: RouteUrlStrategy,
    no_cdn: Optional[bool],
    on_startup: Callable[[str], None],
):
    """
    Start FastAPI/uvicorn web transport for Flet and return server handle.

    Args:
        main: User app entry handler.
        before_main: Optional hook called before `main`.
        host: Host/IP to bind the server to.
        port: TCP port to bind.
        page_name: Web path segment used for page URL.
        assets_dir: Resolved assets directory path.
        upload_dir: Resolved upload directory path.
        web_renderer: Web renderer mode.
        route_url_strategy: Route URL strategy (`path` or `hash`).
        no_cdn: Whether to disable CDN resources.
        on_startup: Callback invoked with resolved page URL.

    Returns:
        Running web-server handle with `.page_url` and `.close()`.
    """

    ensure_flet_web_package_installed()
    from flet_web.fastapi.serve_fastapi_web_app import serve_fastapi_web_app

    url_host = "127.0.0.1" if host in [None, "", "*"] else host

    if port == 0:
        port = get_free_tcp_port()

    logger.info(f"Starting Flet web server on port {port}...")

    log_level = logging.getLogger("flet").getEffectiveLevel()
    if log_level == logging.CRITICAL or log_level == logging.NOTSET:
        log_level = logging.FATAL

    return await serve_fastapi_web_app(
        main,
        before_main=before_main,
        host=host,
        url_host=url_host,
        port=port,
        page_name=page_name,
        assets_dir=assets_dir,
        upload_dir=upload_dir,
        web_renderer=web_renderer,
        route_url_strategy=route_url_strategy,
        no_cdn=no_cdn,
        on_startup=on_startup,
        log_level=logging.getLevelName(log_level).lower(),
    )


def __run_pyodide(
    main: Optional[AppCallable] = None,
    before_main: Optional[AppCallable] = None,
):
    """
    Initialize Pyodide connection for browser-embedded execution.

    Args:
        main: User app entry handler.
        before_main: Optional hook called before `main`.
    """
    from flet.messaging.pyodide_connection import PyodideConnection

    PyodideConnection(
        on_session_created=__get_on_session_created(main), before_main=before_main
    )


def __get_page_name(name: str):
    """
    Resolve effective page name using argument and environment override.

    Args:
        name: Explicit page name from API call.

    Returns:
        Effective page name, preferring `FLET_WEB_APP_PATH` when `name` is empty.
    """

    env_page_name = os.getenv("FLET_WEB_APP_PATH")
    return env_page_name if not name and env_page_name else name


def __get_assets_dir_path(assets_dir: Optional[str], relative_to_cwd=False):
    """
    Resolve assets directory to an absolute path and apply env override.

    Args:
        assets_dir: Input assets directory path.
        relative_to_cwd: Resolve relative paths from current working directory
            instead of current script directory.

    Returns:
        Resolved assets directory path or `None`.
    """

    if assets_dir:
        if not Path(assets_dir).is_absolute():
            if "_MEI" in __file__:
                # support for "onefile" PyInstaller
                assets_dir = str(
                    Path(__file__).parent.parent.joinpath(assets_dir).resolve()
                )
            else:
                assets_dir = str(
                    Path(os.getcwd() if relative_to_cwd else get_current_script_dir())
                    .joinpath(assets_dir)
                    .resolve()
                )
        logger.info(f"Assets path configured: {assets_dir}")

    env_assets_dir = os.getenv("FLET_ASSETS_DIR")
    if env_assets_dir:
        assets_dir = env_assets_dir
    return assets_dir


def __get_upload_dir_path(upload_dir: Optional[str], relative_to_cwd=False):
    """
    Resolve upload directory to an absolute path.

    Args:
        upload_dir: Input upload directory path.
        relative_to_cwd: Resolve relative paths from current working directory
            instead of current script directory.

    Returns:
        Resolved upload directory path or `None`.
    """

    if upload_dir and not Path(upload_dir).is_absolute():
        upload_dir = str(
            Path(os.getcwd() if relative_to_cwd else get_current_script_dir())
            .joinpath(upload_dir)
            .resolve()
        )
    return upload_dir
