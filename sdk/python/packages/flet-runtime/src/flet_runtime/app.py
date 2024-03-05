import asyncio
import concurrent.futures
import logging
import os
import signal
import subprocess
import tarfile
import tempfile
import traceback
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional

import flet_runtime
from flet_core.event import Event
from flet_core.page import Page
from flet_core.types import AppView, WebRenderer
from flet_core.utils import random_string
from flet_runtime.flet_socket_server import FletSocketServer
from flet_runtime.utils import (
    get_arch,
    get_bool_env_var,
    get_current_script_dir,
    get_free_tcp_port,
    get_package_bin_dir,
    is_embedded,
    is_linux,
    is_linux_server,
    is_macos,
    is_windows,
    open_in_browser,
    safe_tar_extractall,
)

try:
    from flet import version
except ImportError:
    from flet_runtime import version

logger = logging.getLogger(flet_runtime.__name__)


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
    if export_asgi_app:
        from flet.fastapi.serve_fastapi_web_app import get_fastapi_web_app

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
            blocking=(view == AppView.WEB_BROWSER or force_web_server),
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
    from flet.fastapi.serve_fastapi_web_app import serve_fastapi_web_app

    url_host = "127.0.0.1" if host in [None, "", "*"] else host

    if port == 0:
        port = get_free_tcp_port()

    logger.info(f"Starting Flet web server on port {port}...")

    log_level = logging.getLogger(flet_runtime.__name__).getEffectiveLevel()
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


def open_flet_view(page_url, assets_dir, hidden):
    args, flet_env, pid_file = __locate_and_unpack_flet_view(
        page_url, assets_dir, hidden
    )
    return subprocess.Popen(args, env=flet_env), pid_file


async def open_flet_view_async(page_url, assets_dir, hidden):
    args, flet_env, pid_file = __locate_and_unpack_flet_view(
        page_url, assets_dir, hidden
    )
    return (
        await asyncio.create_subprocess_exec(args[0], *args[1:], env=flet_env),
        pid_file,
    )


def close_flet_view(pid_file):
    if pid_file is not None and os.path.exists(pid_file):
        try:
            with open(pid_file) as f:
                fvp_pid = int(f.read())
            logger.debug(f"Flet View process {fvp_pid}")
            os.kill(fvp_pid, signal.SIGKILL)
        except Exception:
            pass
        finally:
            os.remove(pid_file)


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


def __locate_and_unpack_flet_view(page_url, assets_dir, hidden):
    logger.info("Starting Flet View app...")

    args = []

    # pid file - Flet client writes its process ID to this file
    pid_file = str(Path(tempfile.gettempdir()).joinpath(random_string(20)))

    if is_windows():
        flet_exe = "flet.exe"
        temp_flet_dir = Path.home().joinpath(".flet", "bin", f"flet-{version.version}")

        # check if flet_view.exe exists in "bin" directory (user mode)
        flet_path = os.path.join(get_package_bin_dir(), "flet", flet_exe)
        if os.path.exists(flet_path):
            logger.info(f"Flet View found in: {flet_path}")
        else:
            # check if flet.exe is in FLET_VIEW_PATH (flet developer mode)
            flet_path = os.environ.get("FLET_VIEW_PATH")
            if flet_path and os.path.exists(flet_path):
                logger.info(f"Flet View found in PATH: {flet_path}")
                flet_path = os.path.join(flet_path, flet_exe)
            else:
                if not temp_flet_dir.exists():
                    zip_file = __download_flet_client("flet-windows.zip")

                    logger.info(f"Extracting flet.exe from archive to {temp_flet_dir}")
                    temp_flet_dir.mkdir(parents=True, exist_ok=True)
                    with zipfile.ZipFile(zip_file, "r") as zip_arch:
                        zip_arch.extractall(str(temp_flet_dir))
                flet_path = str(temp_flet_dir.joinpath("flet", flet_exe))
        args = [flet_path, page_url, pid_file]
    elif is_macos():
        # build version-specific path to Flet.app
        temp_flet_dir = Path.home().joinpath(".flet", "bin", f"flet-{version.version}")

        # check if flet.exe is in FLET_VIEW_PATH (flet developer mode)
        flet_path = os.environ.get("FLET_VIEW_PATH")
        if flet_path:
            logger.info(f"Flet.app is set via FLET_VIEW_PATH: {flet_path}")
            temp_flet_dir = Path(flet_path)
        else:
            # check if flet_view.app exists in a temp directory
            if not temp_flet_dir.exists():
                # check if flet.tar.gz exists
                gz_filename = "flet-macos-amd64.tar.gz"
                tar_file = os.path.join(get_package_bin_dir(), gz_filename)
                if not os.path.exists(tar_file):
                    tar_file = __download_flet_client(gz_filename)

                logger.info(f"Extracting Flet.app from archive to {temp_flet_dir}")
                temp_flet_dir.mkdir(parents=True, exist_ok=True)
                with tarfile.open(str(tar_file), "r:gz") as tar_arch:
                    safe_tar_extractall(tar_arch, str(temp_flet_dir))
            else:
                logger.info(f"Flet View found in: {temp_flet_dir}")

        app_name = None
        for f in os.listdir(temp_flet_dir):
            if f.endswith(".app"):
                app_name = f
        assert app_name is not None, f"Application bundle not found in {temp_flet_dir}"
        app_path = temp_flet_dir.joinpath(app_name)
        args = ["open", str(app_path), "-n", "-W", "--args", page_url, pid_file]
    elif is_linux():
        # build version-specific path to flet folder
        temp_flet_dir = Path.home().joinpath(".flet", "bin", f"flet-{version.version}")

        app_path = None
        # check if flet.exe is in FLET_VIEW_PATH (flet developer mode)
        flet_path = os.environ.get("FLET_VIEW_PATH")
        if flet_path:
            logger.info(f"Flet View is set via FLET_VIEW_PATH: {flet_path}")
            temp_flet_dir = Path(flet_path)
            app_path = temp_flet_dir.joinpath("flet")
        else:
            # check if flet_view.app exists in a temp directory
            if not temp_flet_dir.exists():
                # check if flet.tar.gz exists
                gz_filename = f"flet-linux-{get_arch()}.tar.gz"
                tar_file = os.path.join(get_package_bin_dir(), gz_filename)
                if not os.path.exists(tar_file):
                    tar_file = __download_flet_client(gz_filename)

                logger.info(f"Extracting Flet from archive to {temp_flet_dir}")
                temp_flet_dir.mkdir(parents=True, exist_ok=True)
                with tarfile.open(str(tar_file), "r:gz") as tar_arch:
                    safe_tar_extractall(tar_arch, str(temp_flet_dir))
            else:
                logger.info(f"Flet View found in: {temp_flet_dir}")

            app_path = temp_flet_dir.joinpath("flet", "flet")
        args = [str(app_path), page_url, pid_file]

    flet_env = {**os.environ}

    if assets_dir:
        args.append(assets_dir)

    if hidden:
        flet_env["FLET_HIDE_WINDOW_ON_START"] = "true"

    return args, flet_env, pid_file


def __download_flet_client(file_name):
    ver = version.version
    temp_arch = Path(tempfile.gettempdir()).joinpath(file_name)
    logger.info(f"Downloading Flet v{ver} to {temp_arch}")
    flet_url = f"https://github.com/flet-dev/flet/releases/download/v{ver}/{file_name}"
    urllib.request.urlretrieve(flet_url, temp_arch)
    return str(temp_arch)
