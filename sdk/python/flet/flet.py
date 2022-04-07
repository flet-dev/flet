import json
import logging
import os
import signal
import socket
import tarfile
import tempfile
import threading
import traceback
import urllib.request
import zipfile
from pathlib import Path
from time import sleep

from flet import constants
from flet.connection import Connection
from flet.event import Event
from flet.page import Page
from flet.reconnecting_websocket import ReconnectingWebSocket
from flet.utils import *


def page(
    name="",
    port=0,
    share=False,
    update=False,
    server=None,
    token=None,
    permissions=None,
    no_window=False,
):
    conn = _connect_internal(
        name, port, False, update, share, server, token, permissions, no_window
    )
    print("Page URL:", conn.page_url)
    page = Page(conn, constants.ZERO_SESSION)
    conn.sessions[constants.ZERO_SESSION] = page
    return page


def app(
    name="",
    port=0,
    share=False,
    server=None,
    token=None,
    target=None,
    permissions=None,
    no_window=False,
):

    if target == None:
        raise Exception("target argument is not specified")

    conn = _connect_internal(
        name, port, True, False, share, server, token, permissions, no_window, target
    )
    print("App URL:", conn.page_url)

    terminate = threading.Event()

    def exit_gracefully(signum, frame):
        logging.debug("Gracefully terminating Flet app...")
        terminate.set()

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    try:
        print("Connected to Flet app and handling user sessions...")

        if is_windows():
            input()
        else:
            terminate.wait()
    except (Exception) as e:
        pass

    conn.close()


def _connect_internal(
    page_name=None,
    port=0,
    is_app=False,
    update=False,
    share=False,
    server=None,
    token=None,
    permissions=None,
    no_window=False,
    session_handler=None,
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

        port = _start_flet_server(port, attached)
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

        if not no_window and not conn.browser_opened:
            open_in_browser(conn.page_url)
            conn.browser_opened = True
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


def _start_flet_server(port, attached):

    if port == 0:
        port = _get_free_tcp_port()

    logging.info(f"Starting local Flet Server on port {port}...")
    logging.info(f"Attached process: {attached}")

    flet_exe = "flet.exe" if is_windows() else "flet"

    # check if flet.exe exists in "bin" directory (user mode)
    p = Path(__file__).parent.joinpath("bin", flet_exe)
    if p.exists():
        flet_path = str(p)
        logging.info(f"Flet Server found in: {flet_path}")
    else:
        # check if flet.exe is in PATH (flet developer mode)
        flet_path = which(flet_exe)
        if not flet_path:
            # download flet from GitHub (python module developer mode)
            flet_path = _download_flet()
        else:
            logging.info(f"Flet Server found in PATH")

    flet_env = {**os.environ, "FLET_LOG_TO_FILE": "true"}

    args = [flet_path, "server", "--port", str(port)]

    if attached:
        args.append("--attached")

    log_level = logging.getLogger().getEffectiveLevel()
    if log_level == logging.CRITICAL:
        log_level = logging.FATAL

    if log_level != logging.NOTSET:
        log_level_name = logging.getLevelName(log_level).lower()
        args.extend(["--log-level", log_level_name])

    subprocess.Popen(
        args,
        env=flet_env,
        # creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return port


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
