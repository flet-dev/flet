import json
import logging
import os
import signal
import subprocess
import sys
import tarfile
import tempfile
import threading
import traceback
import urllib.request
import zipfile
from pathlib import Path
from time import sleep

from flet import constants, version
from flet.connection import Connection
from flet.event import Event
from flet.page import Page
from flet.reconnecting_websocket import ReconnectingWebSocket
from flet.utils import (
    get_arch,
    get_current_script_dir,
    get_free_tcp_port,
    get_platform,
    is_linux,
    is_linux_server,
    is_macos,
    is_windows,
    open_in_browser,
    safe_tar_extractall,
    which,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


WEB_BROWSER = "web_browser"
FLET_APP = "flet_app"
FLET_APP_HIDDEN = "flet_app_hidden"

AppViewer = Literal[None, "web_browser", "flet_app", "flet_app_hidden"]

WebRenderer = Literal[None, "auto", "html", "canvaskit"]


def page(
    name="",
    host=None,
    port=0,
    permissions=None,
    view: AppViewer = WEB_BROWSER,
    assets_dir=None,
    upload_dir=None,
    web_renderer="canvaskit",
    route_url_strategy="hash",
):
    conn = _connect_internal(
        page_name=name,
        host=host,
        port=port,
        is_app=False,
        permissions=permissions,
        assets_dir=assets_dir,
        upload_dir=upload_dir,
        web_renderer=web_renderer,
        route_url_strategy=route_url_strategy,
    )
    url_prefix = os.getenv("FLET_DISPLAY_URL_PREFIX")
    if url_prefix is not None:
        print(url_prefix, conn.page_url)
    else:
        logging.info(f"Page URL: {conn.page_url}")

    page = Page(conn, constants.ZERO_SESSION)
    conn.sessions[constants.ZERO_SESSION] = page

    if view == WEB_BROWSER:
        open_in_browser(conn.page_url)

    return page


def app(
    name="",
    host=None,
    port=0,
    target=None,
    permissions=None,
    view: AppViewer = FLET_APP,
    assets_dir=None,
    upload_dir=None,
    web_renderer="canvaskit",
    route_url_strategy="hash",
):
    if target is None:
        raise Exception("target argument is not specified")

    conn = _connect_internal(
        page_name=name,
        host=host,
        port=port,
        is_app=True,
        permissions=permissions,
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

    if (
        (view == FLET_APP or view == FLET_APP_HIDDEN)
        and not is_linux_server()
        and url_prefix is None
    ):
        fvp = open_flet_view(conn.page_url, view == FLET_APP_HIDDEN)
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

    if fvp is not None and not is_windows():
        try:
            logging.debug(f"Flet View process {fvp.pid}")
            os.kill(fvp.pid + 1, signal.SIGKILL)
        except:
            pass


def _connect_internal(
    page_name=None,
    host=None,
    port=0,
    is_app=False,
    update=False,
    share=False,
    server=None,
    token=None,
    permissions=None,
    session_handler=None,
    assets_dir=None,
    upload_dir=None,
    web_renderer=None,
    route_url_strategy=None,
):
    if share and server is None:
        server = constants.HOSTED_SERVICE_URL
    elif server is None:
        # local mode
        env_port = os.getenv("FLET_SERVER_PORT")
        if env_port is not None and env_port:
            port = env_port

        # page with a custom port starts detached process
        attached = False if not is_app and port != 0 else True

        server_ip = host if host not in [None, "", "*"] else "127.0.0.1"
        port = _start_flet_server(
            host,
            port,
            attached,
            assets_dir,
            upload_dir,
            web_renderer,
            route_url_strategy,
        )
        server = f"http://{server_ip}:{port}"

    connected = threading.Event()

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

    ws_url = _get_ws_url(server)
    ws = ReconnectingWebSocket(ws_url)
    conn = Connection(ws)
    conn.on_event = on_event

    if session_handler is not None:
        conn.on_session_created = on_session_created

    def _on_ws_connect():
        if conn.page_name is None:
            conn.page_name = page_name
        assert conn.page_name is not None
        result = conn.register_host_client(
            conn.host_client_id, conn.page_name, is_app, update, token, permissions
        )
        conn.host_client_id = result.hostClientID
        conn.page_name = result.pageName
        conn.page_url = server.rstrip("/")
        if conn.page_name != constants.INDEX_PAGE:
            assert conn.page_url is not None
            conn.page_url += f"/{conn.page_name}"
        connected.set()

    def _on_ws_failed_connect():
        logging.info(f"Failed to connect: {ws_url}")
        # if is_localhost_url(ws_url):
        #     _start_flet_server()

    ws.on_connect = _on_ws_connect
    ws.on_failed_connect = _on_ws_failed_connect
    ws.connect()
    for n in range(0, constants.CONNECT_TIMEOUT_SECONDS):
        if not connected.is_set():
            sleep(1)
    if not connected.is_set():
        ws.close()
        raise Exception(
            f"Could not connected to Flet server in {constants.CONNECT_TIMEOUT_SECONDS} seconds."
        )

    return conn


def _start_flet_server(
    host, port, attached, assets_dir, upload_dir, web_renderer, route_url_strategy
):
    if port == 0:
        port = get_free_tcp_port()

    logging.info(f"Starting local Flet Server on port {port}...")
    logging.info(f"Attached process: {attached}")

    fletd_exe = "fletd.exe" if is_windows() else "fletd"

    # check if flet.exe exists in "bin" directory (user mode)
    p = Path(__file__).parent.joinpath("bin", fletd_exe)
    if p.exists():
        fletd_path = str(p)
        logging.info(f"Flet Server found in: {fletd_path}")
    else:
        # check if flet.exe is in PATH (flet developer mode)
        fletd_path = which(fletd_exe)
        if not fletd_path:
            # download flet from GitHub (python module developer mode)
            fletd_path = _download_fletd()
        else:
            logging.info(f"Flet Server found in PATH")

    fletd_env = {**os.environ}

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
        fletd_env["FLET_STATIC_ROOT_DIR"] = assets_dir

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

    args = [fletd_path, "--port", str(port)]

    creationflags = 0
    start_new_session = False

    if attached:
        args.append("--attached")
    else:
        if is_windows():
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            start_new_session = True

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

    return port


def open_flet_view(page_url, hidden):
    logging.info(f"Starting Flet View app...")

    args = []

    if is_windows():
        flet_exe = "flet.exe"
        temp_flet_dir = Path.home().joinpath(".flet", "bin", f"flet-{version.version}")

        # check if flet_view.exe exists in "bin" directory (user mode)
        p = Path(__file__).parent.joinpath("bin", "flet", flet_exe)
        if p.exists():
            flet_path = str(p)
            logging.info(f"Flet View found in: {flet_path}")
        else:
            # check if flet.exe is in PATH (flet developer mode)
            flet_path = which(flet_exe, sys.argv[0])
            if (
                flet_path
                and Path(flet_path).parent.joinpath("flutter_windows.dll").exists()
            ):
                logging.info(f"Flet View found in PATH: {flet_path}")
            else:
                if not temp_flet_dir.exists():
                    zip_file = _download_flet_client("flet-windows.zip")

                    logging.info(f"Extracting flet.exe from archive to {temp_flet_dir}")
                    temp_flet_dir.mkdir(parents=True, exist_ok=True)
                    with zipfile.ZipFile(zip_file, "r") as zip_arch:
                        zip_arch.extractall(str(temp_flet_dir))
                flet_path = str(temp_flet_dir.joinpath("flet", flet_exe))
        args = [flet_path, page_url]
    elif is_macos():
        # build version-specific path to Flet.app
        temp_flet_dir = Path.home().joinpath(".flet", "bin", f"flet-{version.version}")

        # check if flet_view.app exists in a temp directory
        if not temp_flet_dir.exists():
            # check if flet.tar.gz exists
            gz_filename = "flet-macos-amd64.tar.gz"
            tar_file = Path(__file__).parent.joinpath("bin", gz_filename)
            if not tar_file.exists():
                tar_file = _download_flet_client(gz_filename)

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
        args = ["open", str(app_path), "-n", "-W", "--args", page_url]
    elif is_linux():
        # build version-specific path to flet folder
        temp_flet_dir = Path.home().joinpath(".flet", "bin", f"flet-{version.version}")

        # check if flet_view.app exists in a temp directory
        if not temp_flet_dir.exists():
            # check if flet.tar.gz exists
            gz_filename = f"flet-linux-{get_arch()}.tar.gz"
            tar_file = Path(__file__).parent.joinpath("bin", gz_filename)
            if not tar_file.exists():
                tar_file = _download_flet_client(gz_filename)

            logging.info(f"Extracting Flet from archive to {temp_flet_dir}")
            temp_flet_dir.mkdir(parents=True, exist_ok=True)
            with tarfile.open(str(tar_file), "r:gz") as tar_arch:
                safe_tar_extractall(tar_arch, str(temp_flet_dir))
        else:
            logging.info(f"Flet View found in: {temp_flet_dir}")

        app_path = temp_flet_dir.joinpath("flet", "flet")
        args = [str(app_path), page_url]

    flet_env = {**os.environ}

    if hidden:
        flet_env["FLET_HIDE_WINDOW_ON_START"] = "true"

    # execute process
    return subprocess.Popen(args, env=flet_env)


def _get_ws_url(server: str):
    url = server.rstrip("/")
    if server.startswith("https://"):
        url = url.replace("https://", "wss://")
    elif server.startswith("http://"):
        url = url.replace("http://", "ws://")
    else:
        url = "ws://" + url
    return url + "/ws"


def _download_fletd():
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


def _download_flet_client(file_name):
    ver = version.version
    temp_arch = Path(tempfile.gettempdir()).joinpath(file_name)
    logging.info(f"Downloading Flet v{ver} to {temp_arch}")
    flet_url = f"https://github.com/flet-dev/flet/releases/download/v{ver}/{file_name}"
    urllib.request.urlretrieve(flet_url, temp_arch)
    return str(temp_arch)


# not currently used, but maybe useful in the future
def _get_latest_flet_release():
    releases = json.loads(
        urllib.request.urlopen(
            f"https://api.github.com/repos/flet-dev/flet/releases?per_page=5"
        )
        .read()
        .decode()
    )
    if len(releases) > 0:
        return releases[0]["tag_name"].lstrip("v")
    else:
        return None


# Fix: https://bugs.python.org/issue35935
# if _is_windows():
#    signal.signal(signal.SIGINT, signal.SIG_DFL)
