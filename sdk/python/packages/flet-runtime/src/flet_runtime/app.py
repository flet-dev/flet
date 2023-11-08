import asyncio
import logging
import os
import signal
import subprocess
import tarfile
import tempfile
import threading
import traceback
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional

import flet_runtime
from flet_core.event import Event
from flet_core.page import Page
from flet_core.types import (
    FLET_APP,
    FLET_APP_HIDDEN,
    FLET_APP_WEB,
    WEB_BROWSER,
    AppView,
    WebRenderer,
)
from flet_core.utils import is_coroutine, random_string
from flet_runtime.async_local_socket_connection import AsyncLocalSocketConnection
from flet_runtime.sync_local_socket_connection import SyncLocalSocketConnection
from flet_runtime.utils import (
    get_arch,
    get_current_script_dir,
    get_free_tcp_port,
    get_package_bin_dir,
    get_package_web_dir,
    get_platform,
    is_embedded,
    is_linux,
    is_linux_server,
    is_macos,
    is_windows,
    open_in_browser,
    safe_tar_extractall,
    which,
)

try:
    from flet.async_websocket_connection import AsyncWebSocketConnection
    from flet.sync_websocket_connection import SyncWebSocketConnection
except ImportError:
    from flet_core.connection import Connection

    class AsyncWebSocketConnection(Connection):
        pass

    class SyncWebSocketConnection(Connection):
        pass


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
    auth_token=None,
):
    if is_coroutine(target):
        asyncio.get_event_loop().run_until_complete(
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
                auth_token=auth_token,
            )
        )
    else:
        __app_sync(
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
            auth_token=auth_token,
        )


def __app_sync(
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
    auth_token=None,
):
    if isinstance(view, str):
        view = AppView(view)

    if isinstance(web_renderer, str):
        web_renderer = WebRenderer(web_renderer)

    force_web_view = os.environ.get("FLET_FORCE_WEB_VIEW")
    assets_dir = __get_assets_dir_path(assets_dir)

    conn = __connect_internal_sync(
        page_name=name,
        view=view if not force_web_view else AppView.WEB_BROWSER,
        host=host,
        port=port,
        auth_token=auth_token,
        session_handler=target,
        assets_dir=assets_dir,
        upload_dir=upload_dir,
        web_renderer=web_renderer,
        use_color_emoji=use_color_emoji,
        route_url_strategy=route_url_strategy,
    )

    url_prefix = os.getenv("FLET_DISPLAY_URL_PREFIX")
    if url_prefix is not None:
        print(url_prefix, conn.page_url)
    else:
        logger.info(f"App URL: {conn.page_url}")

    logger.info("Connected to Flet app and handling user sessions...")

    if (
        (
            view == AppView.FLET_APP
            or view == AppView.FLET_APP_HIDDEN
            or view == AppView.FLET_APP_WEB
        )
        and not is_linux_server()
        and not is_embedded()
        and url_prefix is None
    ):
        fvp, pid_file = open_flet_view(
            conn.page_url,
            assets_dir if view != AppView.FLET_APP_WEB else None,
            view == AppView.FLET_APP_HIDDEN,
        )
        try:
            fvp.wait()
        except:
            pass

        close_flet_view(pid_file)
        conn.close()

    elif not is_embedded():
        if view == AppView.WEB_BROWSER and url_prefix is None:
            open_in_browser(conn.page_url)

        terminate = threading.Event()

        def exit_gracefully(signum, frame):
            logger.debug("Gracefully terminating Flet app...")
            terminate.set()

        signal.signal(signal.SIGINT, exit_gracefully)
        signal.signal(signal.SIGTERM, exit_gracefully)

        try:
            while True:
                if terminate.wait(1):
                    break
        except KeyboardInterrupt:
            pass

        conn.close()


async def app_async(
    target,
    name="",
    host=None,
    port=0,
    view: Optional[AppView] = AppView.FLET_APP,
    assets_dir=None,
    upload_dir=None,
    web_renderer: WebRenderer = WebRenderer.CANVAS_KIT,
    use_color_emoji=False,
    route_url_strategy="path",
    auth_token=None,
):
    if isinstance(view, str):
        view = AppView(view)

    if isinstance(web_renderer, str):
        web_renderer = WebRenderer(web_renderer)

    force_web_view = os.environ.get("FLET_FORCE_WEB_VIEW")
    assets_dir = __get_assets_dir_path(assets_dir)

    conn = await __connect_internal_async(
        page_name=name,
        view=view if not force_web_view else AppView.WEB_BROWSER,
        host=host,
        port=port,
        auth_token=auth_token,
        session_handler=target,
        assets_dir=assets_dir,
        upload_dir=upload_dir,
        web_renderer=web_renderer,
        use_color_emoji=use_color_emoji,
        route_url_strategy=route_url_strategy,
    )

    url_prefix = os.getenv("FLET_DISPLAY_URL_PREFIX")
    if url_prefix is not None:
        print(url_prefix, conn.page_url)
    else:
        logger.info(f"App URL: {conn.page_url}")

    terminate = asyncio.Event()

    def exit_gracefully(signum, frame):
        logger.debug("Gracefully terminating Flet app...")
        asyncio.get_running_loop().call_soon_threadsafe(terminate.set)

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    logger.info("Connected to Flet app and handling user sessions...")

    if (
        (
            view == AppView.FLET_APP
            or view == AppView.FLET_APP_HIDDEN
            or view == AppView.FLET_APP_WEB
        )
        and not is_linux_server()
        and not is_embedded()
        and url_prefix is None
    ):
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
        await conn.close()

    elif not is_embedded():
        if view == AppView.WEB_BROWSER and url_prefix is None:
            open_in_browser(conn.page_url)

        try:
            await terminate.wait()
        except KeyboardInterrupt:
            pass

        await conn.close()


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


def __connect_internal_sync(
    page_name,
    view: Optional[AppView] = None,
    host=None,
    port=0,
    server=None,
    auth_token=None,
    session_handler=None,
    assets_dir=None,
    upload_dir=None,
    web_renderer: Optional[WebRenderer] = None,
    use_color_emoji=False,
    route_url_strategy=None,
):
    env_port = os.getenv("FLET_SERVER_PORT")
    if env_port is not None and env_port:
        port = int(env_port)

    uds_path = os.getenv("FLET_SERVER_UDS_PATH")

    env_assets_dir = os.getenv("FLET_ASSETS_PATH")
    if env_assets_dir:
        assets_dir = env_assets_dir

    is_socket_server = server is None and (
        is_embedded() or view == AppView.FLET_APP or view == AppView.FLET_APP_HIDDEN
    )

    if not is_socket_server:
        server = __start_flet_server(
            host,
            port,
            upload_dir,
            web_renderer,
            use_color_emoji,
            route_url_strategy,
        )

    def on_event(conn, e):
        if e.sessionID in conn.sessions:
            conn.sessions[e.sessionID].on_event(
                Event(e.eventTarget, e.eventName, e.eventData)
            )
            if e.eventTarget == "page" and e.eventName == "close":
                logger.info(f"Session closed: {e.sessionID}")
                page = conn.sessions.pop(e.sessionID)
                page._close()
                del page

    def on_session_created(conn, session_data):
        page = Page(conn, session_data.sessionID)
        page.fetch_page_details()
        conn.sessions[session_data.sessionID] = page
        logger.info(f"Session started: {session_data.sessionID}")
        try:
            assert session_handler is not None
            session_handler(page)
        except Exception as e:
            print(
                f"Unhandled error processing page session {page.session_id}:",
                traceback.format_exc(),
            )
            page.error(f"There was an error while processing your request: {e}")

    env_page_name = os.getenv("FLET_PAGE_NAME")

    if is_socket_server:
        conn = SyncLocalSocketConnection(
            port,
            uds_path,
            on_event=on_event,
            on_session_created=on_session_created,
            blocking=is_embedded(),
        )
    else:
        assert server
        conn = SyncWebSocketConnection(
            server_address=server,
            page_name=env_page_name if not page_name and env_page_name else page_name,
            assets_dir=assets_dir,
            token=auth_token,
            on_event=on_event,
            on_session_created=on_session_created,
        )
    conn.connect()
    return conn


async def __connect_internal_async(
    page_name,
    view: Optional[AppView] = None,
    host=None,
    port=0,
    server=None,
    auth_token=None,
    session_handler=None,
    assets_dir=None,
    upload_dir=None,
    web_renderer: Optional[WebRenderer] = None,
    use_color_emoji=False,
    route_url_strategy=None,
):
    env_port = os.getenv("FLET_SERVER_PORT")
    if env_port is not None and env_port:
        port = int(env_port)

    uds_path = os.getenv("FLET_SERVER_UDS_PATH")

    env_assets_dir = os.getenv("FLET_ASSETS_PATH")
    if env_assets_dir:
        assets_dir = env_assets_dir

    is_socket_server = server is None and (
        is_embedded() or view == AppView.FLET_APP or view == AppView.FLET_APP_HIDDEN
    )
    if not is_socket_server:
        server = __start_flet_server(
            host,
            port,
            upload_dir,
            web_renderer,
            use_color_emoji,
            route_url_strategy,
        )

    async def on_event(e):
        if e.sessionID in conn.sessions:
            await conn.sessions[e.sessionID].on_event_async(
                Event(e.eventTarget, e.eventName, e.eventData)
            )
            if e.eventTarget == "page" and e.eventName == "close":
                logger.info(f"Session closed: {e.sessionID}")
                page = conn.sessions.pop(e.sessionID)
                await page._close_async()
                del page

    async def on_session_created(session_data):
        page = Page(conn, session_data.sessionID)
        await page.fetch_page_details_async()
        conn.sessions[session_data.sessionID] = page
        logger.info(f"Session started: {session_data.sessionID}")
        try:
            assert session_handler is not None
            await session_handler(page)
        except Exception as e:
            print(
                f"Unhandled error processing page session {page.session_id}:",
                traceback.format_exc(),
            )
            await page.error_async(
                f"There was an error while processing your request: {e}"
            )

    env_page_name = os.getenv("FLET_PAGE_NAME")

    if is_socket_server:
        conn = AsyncLocalSocketConnection(
            port,
            uds_path,
            on_event=on_event,
            on_session_created=on_session_created,
            blocking=is_embedded(),
        )
    else:
        assert server
        conn = AsyncWebSocketConnection(
            server_address=server,
            page_name=env_page_name if not page_name and env_page_name else page_name,
            assets_dir=assets_dir,
            auth_token=auth_token,
            on_event=on_event,
            on_session_created=on_session_created,
        )
    await conn.connect()
    return conn


def __start_flet_server(
    host,
    port,
    upload_dir,
    web_renderer: Optional[WebRenderer],
    use_color_emoji,
    route_url_strategy,
):
    server_ip = host if host not in [None, "", "*"] else "127.0.0.1"

    if port == 0:
        port = get_free_tcp_port()

    logger.info(f"Starting local Flet Server on port {port}...")

    fletd_exe = "fletd.exe" if is_windows() else "fletd"

    # check if flet.exe exists in "bin" directory (user mode)
    fletd_path = os.path.join(get_package_bin_dir(), fletd_exe)
    if os.path.exists(fletd_path):
        logger.info(f"Flet Server found in: {fletd_path}")
    else:
        # check if flet.exe is in PATH (flet developer mode)
        fletd_path = which(fletd_exe)
        if not fletd_path:
            # download flet from GitHub (python module developer mode)
            fletd_path = __download_fletd()
        else:
            logger.info("Flet Server found in PATH")

    fletd_env = {**os.environ}

    if upload_dir:
        if not Path(upload_dir).is_absolute():
            upload_dir = str(
                Path(get_current_script_dir()).joinpath(upload_dir).resolve()
            )
        logger.info(f"Upload path configured: {upload_dir}")
        fletd_env["FLET_UPLOAD_ROOT_DIR"] = upload_dir

    if host not in [None, "", "*"]:
        logger.info(f"Host binding configured: {host}")
        fletd_env["FLET_SERVER_IP"] = host

        if host != "127.0.0.1":
            fletd_env["FLET_ALLOW_REMOTE_HOST_CLIENTS"] = "true"

    if web_renderer and web_renderer not in [WebRenderer.AUTO]:
        logger.info(f"Web renderer configured: {web_renderer.value}")
        fletd_env["FLET_WEB_RENDERER"] = web_renderer.value

    logger.info(f"Use color emoji: {use_color_emoji}")
    fletd_env["FLET_USE_COLOR_EMOJI"] = str(use_color_emoji).lower()

    if route_url_strategy is not None:
        logger.info(f"Route URL strategy configured: {route_url_strategy}")
        fletd_env["FLET_ROUTE_URL_STRATEGY"] = route_url_strategy

    web_root_dir = get_package_web_dir()

    if not os.path.exists(web_root_dir):
        raise Exception(f"Web root path not found: {web_root_dir}")

    args = [fletd_path, "--content-dir", web_root_dir, "--port", str(port)]

    creationflags = 0
    start_new_session = False

    if os.getenv("FLET_DETACH_FLETD") is None:
        args.append("--attached")
    else:
        if is_windows():
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            start_new_session = True

    log_level = logging.getLogger(flet_runtime.__name__).getEffectiveLevel()
    if log_level == logging.CRITICAL:
        log_level = logging.FATAL

    if log_level != logging.NOTSET:
        log_level_name = logging.getLevelName(log_level).lower()
        args.extend(["--log-level", log_level_name])

    startupinfo = None
    if is_windows():
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen(
        args,
        env=fletd_env,
        creationflags=creationflags,
        start_new_session=start_new_session,
        stdout=subprocess.DEVNULL if log_level >= logging.WARNING else None,
        stderr=subprocess.DEVNULL if log_level >= logging.WARNING else None,
        startupinfo=startupinfo,
    )

    return f"http://{server_ip}:{port}"


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


def __get_assets_dir_path(assets_dir: Optional[str]):
    if assets_dir:
        if not Path(assets_dir).is_absolute():
            if "_MEI" in __file__:
                # support for "onefile" PyInstaller
                assets_dir = str(
                    Path(__file__).parent.parent.joinpath(assets_dir).resolve()
                )
            else:
                assets_dir = str(
                    Path(get_current_script_dir()).joinpath(assets_dir).resolve()
                )
        logger.info(f"Assets path configured: {assets_dir}")
    return assets_dir


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


def __download_fletd():
    ver = version.version
    flet_exe = "fletd.exe" if is_windows() else "fletd"

    # build version-specific path to Fletd
    temp_fletd_dir = Path.home().joinpath(".flet", "bin", f"fletd-{ver}")

    if not temp_fletd_dir.exists():
        logger.info(f"Downloading Fletd v{ver} to {temp_fletd_dir}")
        temp_fletd_dir.mkdir(parents=True, exist_ok=True)
        ext = "zip" if is_windows() else "tar.gz"
        file_name = f"fletd-{ver}-{get_platform()}-{get_arch()}.{ext}"
        flet_url = (
            f"https://github.com/flet-dev/flet/releases/download/v{ver}/{file_name}"
        )

        temp_arch = Path(tempfile.gettempdir()).joinpath(file_name)
        try:
            urllib.request.urlretrieve(flet_url, temp_arch)
            if is_windows():
                with zipfile.ZipFile(temp_arch, "r") as zip_arch:
                    zip_arch.extractall(str(temp_fletd_dir))
            else:
                with tarfile.open(temp_arch, "r:gz") as tar_arch:
                    safe_tar_extractall(tar_arch, str(temp_fletd_dir))
        finally:
            os.remove(temp_arch)
    else:
        logger.info(
            f"Fletd v{version.version} is already installed in {temp_fletd_dir}"
        )
    return str(temp_fletd_dir.joinpath(flet_exe))


def __download_flet_client(file_name):
    ver = version.version
    temp_arch = Path(tempfile.gettempdir()).joinpath(file_name)
    logger.info(f"Downloading Flet v{ver} to {temp_arch}")
    flet_url = f"https://github.com/flet-dev/flet/releases/download/v{ver}/{file_name}"
    urllib.request.urlretrieve(flet_url, temp_arch)
    return str(temp_arch)


# Fix: https://bugs.python.org/issue35935
# if _is_windows():
#    signal.signal(signal.SIGINT, signal.SIG_DFL)
