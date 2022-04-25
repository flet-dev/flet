import json
import logging
import os
import signal
import socket
import sys
import tarfile
import tempfile
import threading
import traceback
import urllib.request
import zipfile
from ensurepip import version
from pathlib import Path
from time import sleep

from flet import constants, version
from flet.connection import Connection
from flet.event import Event
from flet.page import Page
from flet.reconnecting_websocket import ReconnectingWebSocket
from flet.utils import *

try:
    from typing import Literal
except:
    from typing_extensions import Literal


WEB_BROWSER = Literal[1]
FLET_APP = Literal[2]

AppViewer = Literal[
    None,
    WEB_BROWSER,
    FLET_APP,
]


def page(
    name="", port=0, permissions=None, view: AppViewer = WEB_BROWSER, assets_dir=None
):
    conn = _connect_internal(
        page_name=name,
        port=port,
        is_app=False,
        permissions=permissions,
        assets_dir=assets_dir,
    )
    print("Page URL:", conn.page_url)
    page = Page(conn, constants.ZERO_SESSION)
    conn.sessions[constants.ZERO_SESSION] = page

    if view == WEB_BROWSER:
        open_in_browser(conn.page_url)

    return page


def app(
    name="",
    port=0,
    target=None,
    permissions=None,
    view: AppViewer = FLET_APP,
    assets_dir=None,
):

    if target == None:
        raise Exception("target argument is not specified")

    conn = _connect_internal(
        page_name=name,
        port=port,
        is_app=True,
        permissions=permissions,
        session_handler=target,
        assets_dir=assets_dir,
    )
    print("App URL:", conn.page_url)

    terminate = threading.Event()

    def exit_gracefully(signum, frame):
        logging.debug("Gracefully terminating Flet app...")
        terminate.set()

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    print("Connected to Flet app and handling user sessions...")

    fvp = None

    if view == FLET_APP and not is_linux():
        fvp = _open_flet_view(conn.page_url)
        try:
            fvp.wait()
        except (Exception) as e:
            pass
    else:
        if view == WEB_BROWSER:
            open_in_browser(conn.page_url)
        try:
            if is_windows():
                input()
            else:
                terminate.wait()
        except (Exception) as e:
            pass

    conn.close()

    if fvp != None and not is_windows():
        try:
            logging.debug(f"Flet View process {fvp.pid}")
            os.kill(fvp.pid + 1, signal.SIGKILL)
        except:
            pass


def _connect_internal(
    page_name=None,
    port=0,
    is_app=False,
    update=False,
    share=False,
    server=None,
    token=None,
    permissions=None,
    session_handler=None,
    assets_dir=None,
):
    if share and server == None:
        server = constants.HOSTED_SERVICE_URL
    elif server == None:
        # local mode
        env_port = os.getenv("FLET_SERVER_PORT")
        if env_port != None and env_port != "":
            port = env_port

        # page with a custom port starts detached process
        attached = False if not is_app and port != 0 else True

        port = _start_flet_server(port, attached, assets_dir)
        server = f"http://localhost:{port}"

    connected = threading.Event()

    def on_event(conn, e):
        if e.sessionID in conn.sessions:
            conn.sessions[e.sessionID].on_event(
                Event(e.eventTarget, e.eventName, e.eventData)
            )
            if e.eventTarget == "page" and e.eventName == "close":
                print("Session closed:", e.sessionID)
                del conn.sessions[e.sessionID]

    def on_session_created(conn, session_data):
        page = Page(conn, session_data.sessionID)
        conn.sessions[session_data.sessionID] = page
        print("Session started:", session_data.sessionID)
        try:
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

    if session_handler != None:
        conn.on_session_created = on_session_created

    def _on_ws_connect():
        if conn.page_name == None:
            conn.page_name = page_name
        result = conn.register_host_client(
            conn.host_client_id, conn.page_name, is_app, update, token, permissions
        )
        conn.host_client_id = result.hostClientID
        conn.page_name = result.pageName
        conn.page_url = server.rstrip("/")
        if conn.page_name != constants.INDEX_PAGE:
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


def _start_flet_server(port, attached, assets_dir):

    if port == 0:
        port = _get_free_tcp_port()

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
            fletd_path = _download_flet()
        else:
            logging.info(f"Flet Server found in PATH")

    fletd_env = {**os.environ}

    if assets_dir:
        if not Path(assets_dir).is_absolute():
            assets_dir = str(
                Path(get_current_script_dir()).joinpath(assets_dir).resolve()
            )
        logging.info(f"Assets path configured: {assets_dir}")
        fletd_env["FLET_STATIC_ROOT_DIR"] = assets_dir

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

    subprocess.Popen(
        args,
        env=fletd_env,
        creationflags=creationflags,
        start_new_session=start_new_session,
        stdout=subprocess.DEVNULL if log_level >= logging.WARNING else None,
        stderr=subprocess.DEVNULL if log_level >= logging.WARNING else None,
    )

    return port


def _open_flet_view(page_url):

    logging.info(f"Starting Flet View app...")

    args = []

    if is_windows():
        flet_exe = "flet.exe"

        # check if flet_view.exe exists in "bin" directory (user mode)
        p = Path(__file__).parent.joinpath("bin", "flet", flet_exe)
        if p.exists():
            flet_path = str(p)
            logging.info(f"Flet View found in: {flet_path}")
        else:
            # check if flet.exe is in PATH (flet developer mode)
            flet_path = which(flet_exe)
            if flet_path:
                logging.info(f"Flet View found in PATH: {flet_path}")
            else:
                logging.info(f"No Flet View found in PATH or 'bin' directory.")
                return
        args = [flet_path, page_url]
    elif is_macos():
        # check if flet.tar.gz exists
        tar_file = Path(__file__).parent.joinpath("bin", "flet.tar.gz")
        if not tar_file.exists():
            logging.info(f"Flet.app archive does not exist: {tar_file}")
            return

        # build version-specific path to Flet.app
        temp_flet_dir = Path(tempfile.gettempdir()).joinpath(f"flet-{version.version}")

        # check if flet_view.app exists in "bin" directory
        if not temp_flet_dir.exists():
            logging.info(f"Extracting Flet.app from archive to {temp_flet_dir}")
            temp_flet_dir.mkdir(parents=True, exist_ok=True)
            with tarfile.open(str(tar_file), "r:gz") as tar_arch:
                tar_arch.extractall(str(temp_flet_dir))

        app_path = temp_flet_dir.joinpath("Flet.app")
        args = ["open", str(app_path), "-W", "--args", page_url]

    # execute process
    return subprocess.Popen(args)


def _get_ws_url(server: str):
    url = server.rstrip("/")
    if server.startswith("https://"):
        url = url.replace("https://", "wss://")
    elif server.startswith("http://"):
        url = url.replace("http://", "ws://")
    else:
        url = "ws://" + url
    return url + "/ws"


def _download_flet():
    flet_exe = "flet.exe" if is_windows() else "flet"
    flet_bin = Path.home().joinpath(".flet", "bin")
    flet_bin.mkdir(parents=True, exist_ok=True)

    flet_version = _get_latest_flet_release()

    if flet_version == None:
        raise Exception("There are no Flet releases yet.")

    installed_ver = None
    flet_path = flet_bin.joinpath(flet_exe)
    if flet_path.exists():
        # check installed version
        installed_ver = subprocess.check_output([str(flet_path), "--version"]).decode(
            "utf-8"
        )
        logging.info(f"Flet v{flet_version} is already installed in {flet_path}")

    if not installed_ver or installed_ver != flet_version:
        print(f"Downloading Flet v{flet_version} to {flet_path}")

        ext = "zip" if is_windows() else "tar.gz"
        file_name = f"flet-{flet_version}-{get_platform()}-{get_arch()}.{ext}"
        flet_url = f"https://github.com/flet/flet/releases/download/v{flet_version}/{file_name}"

        temp_arch = Path(tempfile.gettempdir()).joinpath(file_name)
        try:
            urllib.request.urlretrieve(flet_url, temp_arch)
            if is_windows():
                with zipfile.ZipFile(temp_arch, "r") as zip_arch:
                    zip_arch.extractall(flet_bin)
            else:
                with tarfile.open(temp_arch, "r:gz") as tar_arch:
                    tar_arch.extractall(flet_bin)
        finally:
            os.remove(temp_arch)
    return str(flet_path)


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


def _get_free_tcp_port():
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]


# Fix: https://bugs.python.org/issue35935
# if _is_windows():
#    signal.signal(signal.SIGINT, signal.SIG_DFL)
