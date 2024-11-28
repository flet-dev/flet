import asyncio
import concurrent.futures
import logging
import os
import signal
import traceback
from pathlib import Path
from typing import Optional

import flet.version
from flet.core.event import Event
from flet.core.page import Page
from flet.core.types import AppView, WebRenderer
from flet.utils import (
    get_bool_env_var,
    get_current_script_dir,
    get_free_tcp_port,
    is_embedded,
    is_linux_server,
    is_pyodide,
    open_in_browser,
)
from flet.utils.pip import (
    ensure_flet_desktop_package_installed,
    ensure_flet_web_package_installed,
)

import flet

logger = logging.getLogger(flet.__name__)


def app(
    target,
    name="",
    host=None,
    port=0,
    view: Optional[AppView] = AppView.FLET_APP,
    assets_dir="assets",
    upload_dir=None,
    web_renderer: WebRenderer = WebRenderer.CANVAS_KIT,
    use_color_emoji=False,
    route_url_strategy="path",
    export_asgi_app=False,
):
    if is_pyodide():
        __run_pyodide(target)
        return

    if export_asgi_app:
        ensure_flet_web_package_installed()
        from flet_web.fastapi.serve_fastapi_web_app import get_fastapi_web_app

        return get_fastapi_web_app(
            session_handler=target,
            page_name=__get_page_name(name),
            assets_dir=__get_assets_dir_path(assets_dir, relative_to_cwd=True),
            upload_dir=__get_upload_dir_path(upload_dir, relative_to_cwd=True),
            web_renderer=web_renderer,
            use_color_emoji=use_color_emoji,
            route_url_strategy=route_url_strategy,
        )

    return asyncio.run(
        app_async(
            target=target,
            name=name,
            host=host,
            port=port,
            view=view,
            assets_dir=assets_dir,
            upload_dir=upload_dir,
            web_renderer=web_renderer,
            use_color_emoji=use_color_emoji,
            route_url_strategy=route_url_strategy,
        )
    )


async def app_async(
    target,
    name="",
    host=None,
    port=0,
    view: Optional[AppView] = AppView.FLET_APP,
    assets_dir="assets",
    upload_dir=None,
    web_renderer: WebRenderer = WebRenderer.CANVAS_KIT,
    use_color_emoji=False,
    route_url_strategy="path",
):
    if is_pyodide():
        __run_pyodide(target)
        return

    if isinstance(view, str):
        view = AppView(view)

    if isinstance(web_renderer, str):
        web_renderer = WebRenderer(web_renderer)

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
        is_embedded() or view == AppView.FLET_APP or view == AppView.FLET_APP_HIDDEN
    ) and not force_web_server

    url_prefix = os.getenv("FLET_DISPLAY_URL_PREFIX")

    def on_app_startup(page_url):
        if url_prefix is not None:
            print(url_prefix, page_url)
        else:
            logger.info(f"App URL: {page_url}")

        if view == AppView.WEB_BROWSER and url_prefix is None and not force_web_server:
            open_in_browser(page_url)

    loop = asyncio.get_running_loop()

    terminate = asyncio.Event()

    def exit_gracefully(signum, frame):
        logger.debug("Gracefully terminating Flet app...")
        loop.call_soon_threadsafe(terminate.set)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    conn = (
        await __run_socket_server(
            port=port,
            session_handler=target,
            blocking=is_embedded(),
        )
        if is_socket_server
        else await __run_web_server(
            session_handler=target,
            host=host,
            port=port,
            page_name=page_name,
            assets_dir=assets_dir,
            upload_dir=upload_dir,
            web_renderer=web_renderer,
            use_color_emoji=use_color_emoji,
            route_url_strategy=route_url_strategy,
            blocking=(view == AppView.WEB_BROWSER or view is None or force_web_server),
            on_startup=on_app_startup,
        )
    )

    logger.info("Flet app has started...")

    try:
        if (
            (
                view == AppView.FLET_APP
                or view == AppView.FLET_APP_HIDDEN
                or view == AppView.FLET_APP_WEB
            )
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
            try:
                await fvp.wait()
            except:
                pass

            close_flet_view(pid_file)

        elif url_prefix and is_socket_server:
            on_app_startup(conn.page_url)

            try:
                await terminate.wait()
            except KeyboardInterrupt:
                pass

    finally:
        await conn.close()


async def __run_socket_server(port=0, session_handler=None, blocking=False):
    from flet.flet_socket_server import FletSocketServer

    uds_path = os.getenv("FLET_SERVER_UDS_PATH")

    executor = concurrent.futures.ThreadPoolExecutor()

    async def on_event(e):
        if e.sessionID in conn.sessions:
            await conn.sessions[e.sessionID].on_event_async(
                Event(e.eventTarget, e.eventName, e.eventData)
            )
            if e.eventTarget == "page" and e.eventName == "close":
                logger.info(f"Session closed: {e.sessionID}")
                page = conn.sessions.pop(e.sessionID)
                page._close()
                del page

    async def on_session_created(session_data):
        page = Page(
            conn,
            session_data.sessionID,
            executor=executor,
            loop=asyncio.get_running_loop(),
        )
        await page.fetch_page_details_async()
        conn.sessions[session_data.sessionID] = page
        logger.info("App session started")
        try:
            assert session_handler is not None
            if asyncio.iscoroutinefunction(session_handler):
                await session_handler(page)
            else:
                # run in thread pool
                await asyncio.get_running_loop().run_in_executor(
                    executor, session_handler, page
                )

        except Exception as e:
            print(
                f"Unhandled error processing page session {page.session_id}:",
                traceback.format_exc(),
            )
            page.error(f"There was an error while processing your request: {e}")

    conn = FletSocketServer(
        loop=asyncio.get_running_loop(),
        port=port,
        uds_path=uds_path,
        on_event=on_event,
        on_session_created=on_session_created,
        blocking=blocking,
        executor=executor,
    )
    await conn.start()
    return conn


async def __run_web_server(
    session_handler,
    host,
    port,
    page_name,
    assets_dir,
    upload_dir,
    web_renderer: Optional[WebRenderer],
    use_color_emoji,
    route_url_strategy,
    blocking,
    on_startup,
):
    ensure_flet_web_package_installed()
    from flet_web.fastapi.serve_fastapi_web_app import serve_fastapi_web_app

    url_host = "127.0.0.1" if host in [None, "", "*"] else host

    if port == 0:
        port = get_free_tcp_port()

    logger.info(f"Starting Flet web server on port {port}...")

    log_level = logging.getLogger(flet.__name__).getEffectiveLevel()
    if log_level == logging.CRITICAL or log_level == logging.NOTSET:
        log_level = logging.FATAL

    return await serve_fastapi_web_app(
        session_handler,
        host=host,
        url_host=url_host,
        port=port,
        page_name=page_name,
        assets_dir=assets_dir,
        upload_dir=upload_dir,
        web_renderer=web_renderer,
        use_color_emoji=use_color_emoji,
        route_url_strategy=route_url_strategy,
        blocking=blocking,
        on_startup=on_startup,
        log_level=logging.getLevelName(log_level).lower(),
    )


def __run_pyodide(target):
    import flet_js
    from flet.pyodide_connection import PyodideConnection

    async def on_event(e):
        if e.sessionID in conn.sessions:
            await conn.sessions[e.sessionID].on_event_async(
                Event(e.eventTarget, e.eventName, e.eventData)
            )
            if e.eventTarget == "page" and e.eventName == "close":
                logger.info(f"Session closed: {e.sessionID}")
                del conn.sessions[e.sessionID]

    async def on_session_created(session_data):
        page = Page(conn, session_data.sessionID, loop=asyncio.get_running_loop())
        await page.fetch_page_details_async()
        conn.sessions[session_data.sessionID] = page
        logger.info("App session started")
        try:
            assert target is not None
            if asyncio.iscoroutinefunction(target):
                await target(page)
            else:
                target(page)
        except Exception as e:
            print(
                f"Unhandled error processing page session {page.session_id}:",
                traceback.format_exc(),
            )
            page.error(f"There was an error while processing your request: {e}")

    conn = PyodideConnection(
        on_event=on_event,
        on_session_created=on_session_created,
    )


def __get_page_name(name: str):
    env_page_name = os.getenv("FLET_WEB_APP_PATH")
    return env_page_name if not name and env_page_name else name


def __get_assets_dir_path(assets_dir: Optional[str], relative_to_cwd=False):
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
    if upload_dir:
        if not Path(upload_dir).is_absolute():
            upload_dir = str(
                Path(os.getcwd() if relative_to_cwd else get_current_script_dir())
                .joinpath(upload_dir)
                .resolve()
            )
    return upload_dir
