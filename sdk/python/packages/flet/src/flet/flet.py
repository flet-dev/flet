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

from flet import version
from flet.async_local_socket_connection import AsyncLocalSocketConnection
from flet.async_websocket_connection import AsyncWebSocketConnection
from flet.sync_local_socket_connection import SyncLocalSocketConnection
from flet.sync_websocket_connection import SyncWebSocketConnection
from flet.utils import (
    get_arch,
    get_current_script_dir,
    get_free_tcp_port,
    get_package_bin_dir,
    get_package_web_dir,
    get_platform,
    is_linux,
    is_linux_server,
    is_macos,
    is_windows,
    open_in_browser,
    safe_tar_extractall,
    which,
)
from flet_core.event import Event
from flet_core.page import Page
from flet_core.utils import is_coroutine, random_string

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


WEB_BROWSER = "web_browser"
FLET_APP = "flet_app"
FLET_APP_HIDDEN = "flet_app_hidden"

AppViewer = Literal[None, "web_browser", "flet_app", "flet_app_hidden"]

WebRenderer = Literal[None, "auto", "html", "canvaskit"]


def app(
    target,
    name="",
    host=None,
    port=0,
    view: AppViewer = FLET_APP,
    assets_dir=None,
    upload_dir=None,
    web_renderer="canvaskit",
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
            route_url_strategy=route_url_strategy,
            auth_token=auth_token,
        )


def __app_sync(
    target,
    name="",
    host=None,
    port=0,
    view: AppViewer = FLET_APP,
    assets_dir=None,
    upload_dir=None,
    web_renderer="canvaskit",
    route_url_strategy="path",
    auth_token=None,
):
    force_web_view = os.environ.get("FLET_FORCE_WEB_VIEW")
    assets_dir = __get_assets_dir_path(assets_dir)

    conn = __connect_internal_sync(
        page_name=name,
        view=view if not force_web_view else WEB_BROWSER,
        host=host,
        port=port,
        auth_token=auth_token,
        session_handler=target,
        assets_dir=assets_dir,
        upload_dir=upload_dir,
        web_renderer=web_renderer,
        route_url_strategy=route_url_strategy,
    )

    url_prefix = os.getenv("FLET_DISPLAY_URL_PREFIX")
    if url_prefix is not None:
        print(url_prefix, conn.page_url)
    else:
        logging.info(f"App URL: {conn.page_url}")

    terminate = threading.Event()

    def exit_gracefully(signum, frame):
        logging.debug("Gracefully terminating Flet app...")
        terminate.set()

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    logging.info("Connected to Flet app and handling user sessions...")

    fvp = None
    pid_file = None

    if (
        (view == FLET_APP or view == FLET_APP_HIDDEN)
        and not is_linux_server()
        and url_prefix is None
    ):
        fvp, pid_file = open_flet_view(
            conn.page_url, assets_dir, view == FLET_APP_HIDDEN
        )
        try:
            fvp.wait()
        except (Exception) as e:
            pass
    else:
        if view == WEB_BROWSER and url_prefix is None:
            open_in_browser(conn.page_url)
        try:
            while True:
                if terminate.wait(1):
                    break
        except KeyboardInterrupt:
            pass

    conn.close()
    close_flet_view(pid_file)


async def app_async(
    target,
    name="",
    host=None,
    port=0,
    view: AppViewer = FLET_APP,
    assets_dir=None,
    upload_dir=None,
    web_renderer="canvaskit",
    route_url_strategy="path",
    auth_token=None,
):
    force_web_view = os.environ.get("FLET_FORCE_WEB_VIEW")
    assets_dir = __get_assets_dir_path(assets_dir)

    conn = await __connect_internal_async(
        page_name=name,
        view=view if not force_web_view else WEB_BROWSER,
        host=host,
        port=port,
        auth_token=auth_token,
        session_handler=target,
        assets_dir=assets_dir,
        upload_dir=upload_dir,
        web_renderer=web_renderer,
        route_url_strategy=route_url_strategy,
    )

    url_prefix = os.getenv("FLET_DISPLAY_URL_PREFIX")
    if url_prefix is not None:
        print(url_prefix, conn.page_url)
    else:
        logging.info(f"App URL: {conn.page_url}")

    terminate = asyncio.Event()

    def exit_gracefully(signum, frame):
        logging.debug("Gracefully terminating Flet app...")
        asyncio.get_running_loop().call_soon_threadsafe(terminate.set)

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    logging.info("Connected to Flet app and handling user sessions...")

    fvp = None
    pid_file = None

    if (
        (view == FLET_APP or view == FLET_APP_HIDDEN)
        and not is_linux_server()
        and url_prefix is None
    ):
        fvp, pid_file = await open_flet_view_async(
            conn.page_url, assets_dir, view == FLET_APP_HIDDEN
        )
        try:
            await fvp.wait()
        except (Exception) as e:
            pass
    else:
        if view == WEB_BROWSER and url_prefix is None:
            open_in_browser(conn.page_url)
        try:
            await terminate.wait()
        except KeyboardInterrupt:
            pass

    await conn.close()
    close_flet_view(pid_file)


def close_flet_view(pid_file):
    if pid_file is not None and os.path.exists(pid_file):
        try:
            with open(pid_file) as f:
                fvp_pid = int(f.read())
            logging.debug(f"Flet View process {fvp_pid}")
            os.kill(fvp_pid, signal.SIGKILL)
        except:
            pass
        finally:
            os.remove(pid_file)


def __connect_internal_sync(
    page_name,
    view: AppViewer = None,
    host=None,
    port=0,
    server=None,
    auth_token=None,
    session_handler=None,
    assets_dir=None,
    upload_dir=None,
    web_renderer=None,
    route_url_strategy=None,
):

    env_port = os.getenv("FLET_SERVER_PORT")
    if env_port is not None and env_port:
        port = int(env_port)

    uds_path = os.getenv("FLET_SERVER_UDS_PATH")

    is_desktop = view == FLET_APP or view == FLET_APP_HIDDEN
    if server is None and not is_desktop:
        server = __start_flet_server(
            host,
            port,
            assets_dir,
            upload_dir,
            web_renderer,
            route_url_strategy,
        )

    def on_event(conn, e):
        if e.sessionID in conn.sessions:
            conn.sessions[e.sessionID].on_event(
                Event(e.eventTarget, e.eventName, e.eventData)
            )
            if e.eventTarget == "page" and e.eventName == "close":
                logging.info(f"Session closed: {e.sessionID}")
                del conn.sessions[e.sessionID]

    def on_session_created(conn, session_data):
        page = Page(conn, session_data.sessionID)
        page.fetch_page_details()
        conn.sessions[session_data.sessionID] = page
        logging.info(f"Session started: {session_data.sessionID}")
        try:
            assert session_handler is not None
            session_handler(page)
        except Exception as e:
            print(
                f"Unhandled error processing page session {page.session_id}:",
                traceback.format_exc(),
            )
            page.error(f"There was an error while processing your request: {e}")

    if is_desktop:
        conn = SyncLocalSocketConnection(
            port,
            uds_path,
            on_event=on_event,
            on_session_created=on_session_created,
        )
    else:
        assert server
        conn = SyncWebSocketConnection(
            server_address=server,
            page_name=page_name,
            token=auth_token,
            on_event=on_event,
            on_session_created=on_session_created,
        )
    conn.connect()
    return conn


async def __connect_internal_async(
    page_name,
    view: AppViewer = None,
    host=None,
    port=0,
    server=None,
    auth_token=None,
    session_handler=None,
    assets_dir=None,
    upload_dir=None,
    web_renderer=None,
    route_url_strategy=None,
):

    env_port = os.getenv("FLET_SERVER_PORT")
    if env_port is not None and env_port:
        port = int(env_port)

    uds_path = os.getenv("FLET_SERVER_UDS_PATH")

    is_desktop = view == FLET_APP or view == FLET_APP_HIDDEN
    if server is None and not is_desktop:
        server = __start_flet_server(
            host,
            port,
            assets_dir,
            upload_dir,
            web_renderer,
            route_url_strategy,
        )

    async def on_event(e):
        if e.sessionID in conn.sessions:
            await conn.sessions[e.sessionID].on_event_async(
                Event(e.eventTarget, e.eventName, e.eventData)
            )
            if e.eventTarget == "page" and e.eventName == "close":
                logging.info(f"Session closed: {e.sessionID}")
                del conn.sessions[e.sessionID]

    async def on_session_created(session_data):
        page = Page(conn, session_data.sessionID)
        await page.fetch_page_details_async()
        conn.sessions[session_data.sessionID] = page
        logging.info(f"Session started: {session_data.sessionID}")
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

    if is_desktop:
        conn = AsyncLocalSocketConnection(
            port,
            uds_path,
            on_event=on_event,
            on_session_created=on_session_created,
        )
    else:
        assert server
        conn = AsyncWebSocketConnection(
            server_address=server,
            page_name=page_name,
            auth_token=auth_token,
            on_event=on_event,
            on_session_created=on_session_created,
        )
    await conn.connect()
    return conn


def __start_flet_server(
    host, port, assets_dir, upload_dir, web_renderer, route_url_strategy
):
    server_ip = host if host not in [None, "", "*"] else "127.0.0.1"

    if port == 0:
        port = get_free_tcp_port()

    logging.info(f"Starting local Flet Server on port {port}...")

    fletd_exe = "fletd.exe" if is_windows() else "fletd"

    # check if flet.exe exists in "bin" directory (user mode)
    fletd_path = os.path.join(get_package_bin_dir(), fletd_exe)
    if os.path.exists(fletd_path):
        logging.info(f"Flet Server found in: {fletd_path}")
    else:
        # check if flet.exe is in PATH (flet developer mode)
        fletd_path = which(fletd_exe)
        if not fletd_path:
            # download flet from GitHub (python module developer mode)
            fletd_path = __download_fletd()
        else:
            logging.info(f"Flet Server found in PATH")

    fletd_env = {**os.environ}

    if upload_dir:
        if not Path(upload_dir).is_absolute():
            upload_dir = str(
                Path(get_current_script_dir()).joinpath(upload_dir).resolve()
            )
        logging.info(f"Upload path configured: {upload_dir}")
        fletd_env["FLET_UPLOAD_ROOT_DIR"] = upload_dir

    if host not in [None, "", "*"]:
        logging.info(f"Host binding configured: {host}")
        fletd_env["FLET_SERVER_IP"] = host

        if host != "127.0.0.1":
            fletd_env["FLET_ALLOW_REMOTE_HOST_CLIENTS"] = "true"

    if web_renderer and web_renderer not in ["auto"]:
        logging.info(f"Web renderer configured: {web_renderer}")
        fletd_env["FLET_WEB_RENDERER"] = web_renderer

    if route_url_strategy is not None:
        logging.info(f"Route URL strategy configured: {route_url_strategy}")
        fletd_env["FLET_ROUTE_URL_STRATEGY"] = route_url_strategy

    web_root_dir = get_package_web_dir()

    if not os.path.exists(web_root_dir):
        raise Exception("Web root path not found: {}".format(web_root_dir))

    args = [fletd_path, "--content-dir", web_root_dir, "--port", str(port)]

    env_assets_dir = os.getenv("FLET_ASSETS_PATH")
    if env_assets_dir:
        assets_dir = env_assets_dir

    if assets_dir:
        args.extend(["--assets-dir", assets_dir])

    creationflags = 0
    start_new_session = False

    args.append("--attached")

    log_level = logging.getLogger().getEffectiveLevel()
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
        logging.info(f"Assets path configured: {assets_dir}")
    return assets_dir


def __locate_and_unpack_flet_view(page_url, assets_dir, hidden):
    logging.info(f"Starting Flet View app...")

    args = []

    # pid file - Flet client writes its process ID to this file
    pid_file = str(Path(tempfile.gettempdir()).joinpath(random_string(20)))

    if is_windows():
        flet_exe = "flet.exe"
        temp_flet_dir = Path.home().joinpath(".flet", "bin", f"flet-{version.version}")

        # check if flet_view.exe exists in "bin" directory (user mode)
        flet_path = os.path.join(get_package_bin_dir(), "flet", flet_exe)
        if os.path.exists(flet_path):
            logging.info(f"Flet View found in: {flet_path}")
        else:
            # check if flet.exe is in FLET_VIEW_PATH (flet developer mode)
            flet_path = os.environ.get("FLET_VIEW_PATH")
            if flet_path and os.path.exists(flet_path):
                logging.info(f"Flet View found in PATH: {flet_path}")
                flet_path = os.path.join(flet_path, flet_exe)
            else:
                if not temp_flet_dir.exists():
                    zip_file = __download_flet_client("flet-windows.zip")

                    logging.info(f"Extracting flet.exe from archive to {temp_flet_dir}")
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
            logging.info(f"Flet.app is set via FLET_VIEW_PATH: {flet_path}")
            temp_flet_dir = Path(flet_path)
        else:
            # check if flet_view.app exists in a temp directory
            if not temp_flet_dir.exists():
                # check if flet.tar.gz exists
                gz_filename = "flet-macos-amd64.tar.gz"
                tar_file = os.path.join(get_package_bin_dir(), gz_filename)
                if not os.path.exists(tar_file):
                    tar_file = __download_flet_client(gz_filename)

                logging.info(f"Extracting Flet.app from archive to {temp_flet_dir}")
                temp_flet_dir.mkdir(parents=True, exist_ok=True)
                with tarfile.open(str(tar_file), "r:gz") as tar_arch:
                    safe_tar_extractall(tar_arch, str(temp_flet_dir))
            else:
                logging.info(f"Flet View found in: {temp_flet_dir}")

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

            logging.info(f"Extracting Flet from archive to {temp_flet_dir}")
            temp_flet_dir.mkdir(parents=True, exist_ok=True)
            with tarfile.open(str(tar_file), "r:gz") as tar_arch:
                safe_tar_extractall(tar_arch, str(temp_flet_dir))
        else:
            logging.info(f"Flet View found in: {temp_flet_dir}")

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
        logging.info(f"Downloading Fletd v{ver} to {temp_fletd_dir}")
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
        logging.info(
            f"Fletd v{version.version} is already installed in {temp_fletd_dir}"
        )
    return str(temp_fletd_dir.joinpath(flet_exe))


def __download_flet_client(file_name):
    ver = version.version
    temp_arch = Path(tempfile.gettempdir()).joinpath(file_name)
    logging.info(f"Downloading Flet v{ver} to {temp_arch}")
    flet_url = f"https://github.com/flet-dev/flet/releases/download/v{ver}/{file_name}"
    urllib.request.urlretrieve(flet_url, temp_arch)
    return str(temp_arch)


# Fix: https://bugs.python.org/issue35935
# if _is_windows():
#    signal.signal(signal.SIGINT, signal.SIG_DFL)
