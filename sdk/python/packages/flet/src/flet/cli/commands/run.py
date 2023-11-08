import argparse
import os
import platform
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from urllib.parse import quote, urlparse, urlunparse

import qrcode
from flet.cli.commands.base import BaseCommand
from flet_core.utils import random_string
from flet_runtime.app import close_flet_view, open_flet_view
from flet_runtime.utils import (
    get_free_tcp_port,
    get_local_ip,
    is_windows,
    open_in_browser,
)
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Command(BaseCommand):
    """
    Run Flet app.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "script",
            type=str,
            nargs="?",
            default=".",
            help="path to a Python script",
        )
        parser.add_argument(
            "-p",
            "--port",
            dest="port",
            type=int,
            default=None,
            help="custom TCP port to run Flet app on",
        )
        parser.add_argument(
            "--host",
            dest="host",
            type=str,
            default=None,
            help='host to run Flet web app on. Use "*" to listen on all IPs.',
        )
        parser.add_argument(
            "--name",
            dest="app_name",
            type=str,
            default=None,
            help="app name to distinguish it from other on the same port",
        )
        parser.add_argument(
            "-m",
            "--module",
            dest="module",
            action="store_true",
            default=False,
            help="treat the script as a python module path as opposed to a file path",
        )
        parser.add_argument(
            "-d",
            "--directory",
            dest="directory",
            action="store_true",
            default=False,
            help="watch script directory",
        )
        parser.add_argument(
            "-r",
            "--recursive",
            dest="recursive",
            action="store_true",
            default=False,
            help="watch script directory and all sub-directories recursively",
        )
        parser.add_argument(
            "-n",
            "--hidden",
            dest="hidden",
            action="store_true",
            default=False,
            help="application window is hidden on startup",
        )
        parser.add_argument(
            "-w",
            "--web",
            dest="web",
            action="store_true",
            default=False,
            help="open app in a web browser",
        )
        parser.add_argument(
            "--ios",
            dest="ios",
            action="store_true",
            default=False,
            help="open app on iOS device",
        )
        parser.add_argument(
            "--android",
            dest="android",
            action="store_true",
            default=False,
            help="open app on Android device",
        )
        parser.add_argument(
            "-a",
            "--assets",
            dest="assets_dir",
            type=str,
            default="assets",
            help="path to assets directory",
        )

    def handle(self, options: argparse.Namespace) -> None:
        if options.module:
            script_path = str(options.script).replace(".", "/")
            if os.path.isdir(script_path):
                script_path += "/__main__.py"
            else:
                script_path += ".py"
        else:
            script_path = str(options.script)
            if not os.path.isabs(script_path):
                script_path = str(Path(os.getcwd()).joinpath(script_path).resolve())
            if os.path.isdir(script_path):
                script_path = os.path.join(script_path, "main.py")

        if not Path(script_path).exists():
            print(f"File or directory not found: {script_path}")
            sys.exit(1)

        script_dir = os.path.dirname(script_path)

        port = options.port
        if port is None and (options.ios or options.android):
            port = 8551
        elif port is None and (is_windows() or options.web):
            port = get_free_tcp_port()

        uds_path = None
        if port is None and not is_windows():
            uds_path = str(Path(tempfile.gettempdir()).joinpath(random_string(10)))

        assets_dir = options.assets_dir
        if assets_dir and not Path(assets_dir).is_absolute():
            assets_dir = str(
                Path(os.path.dirname(script_path)).joinpath(assets_dir).resolve()
            )

        my_event_handler = Handler(
            [sys.executable, "-u"]
            + ["-m"] * options.module
            + [options.script if options.module else script_path],
            None if options.directory or options.recursive else script_path,
            port,
            options.host,
            options.app_name,
            uds_path,
            options.web,
            options.ios,
            options.android,
            options.hidden,
            assets_dir,
        )

        my_observer = Observer()
        my_observer.schedule(my_event_handler, script_dir, recursive=options.recursive)
        my_observer.start()

        try:
            while True:
                if my_event_handler.terminate.wait(1):
                    break
        except KeyboardInterrupt:
            pass

        close_flet_view(my_event_handler.pid_file)
        my_observer.stop()
        my_observer.join()


class Handler(FileSystemEventHandler):
    def __init__(
        self,
        args,
        script_path,
        port,
        host,
        page_name,
        uds_path,
        web,
        ios,
        android,
        hidden,
        assets_dir,
    ) -> None:
        super().__init__()
        self.args = args
        self.script_path = script_path
        self.port = port
        self.host = host
        self.page_name = page_name
        self.uds_path = uds_path
        self.web = web
        self.ios = ios
        self.android = android
        self.hidden = hidden
        self.assets_dir = assets_dir
        self.last_time = time.time()
        self.is_running = False
        self.fvp = None
        self.pid_file = None
        self.page_url_prefix = f"PAGE_URL_{time.time()}"
        self.page_url = None
        self.terminate = threading.Event()
        self.start_process()

    def start_process(self):
        p_env = {**os.environ}
        if self.web or self.ios or self.android:
            p_env["FLET_FORCE_WEB_VIEW"] = "true"
            p_env["FLET_DETACH_FLETD"] = "true"

            # force page name for ios
            if self.ios or self.android:
                p_env["FLET_PAGE_NAME"] = "/".join(Path(self.script_path).parts[-2:])
        if self.port is not None:
            p_env["FLET_SERVER_PORT"] = str(self.port)
        if self.host is not None:
            p_env["FLET_SERVER_IP"] = str(self.host)
        if self.page_name:
            p_env["FLET_PAGE_NAME"] = self.page_name
        if self.uds_path is not None:
            p_env["FLET_SERVER_UDS_PATH"] = self.uds_path
        if self.assets_dir is not None:
            p_env["FLET_ASSETS_PATH"] = self.assets_dir
        p_env["FLET_DISPLAY_URL_PREFIX"] = self.page_url_prefix

        p_env["PYTHONIOENCODING"] = "utf-8"

        self.p = subprocess.Popen(
            self.args, env=p_env, stdout=subprocess.PIPE, encoding="utf-8"
        )
        self.is_running = True
        th = threading.Thread(target=self.print_output, args=[self.p], daemon=True)
        th.start()

    def on_any_event(self, event):
        if (
            self.script_path is None or event.src_path == self.script_path
        ) and not event.is_directory:
            current_time = time.time()
            if (current_time - self.last_time) > 0.5 and self.is_running:
                self.last_time = current_time
                th = threading.Thread(target=self.restart_program, args=(), daemon=True)
                th.start()

    def print_output(self, p):
        while True:
            line = p.stdout.readline()
            if not line:
                break
            line = line.rstrip("\r\n")
            if line.startswith(self.page_url_prefix):
                if not self.page_url:
                    self.page_url = line[len(self.page_url_prefix) + 1 :]
                    if (
                        self.page_url.startswith("http")
                        and not self.ios
                        and not self.android
                    ):
                        print(self.page_url)
                    if self.ios or self.android:
                        self.print_qr_code(self.page_url, self.android)
                    elif self.web:
                        open_in_browser(self.page_url)
                    else:
                        th = threading.Thread(
                            target=self.open_flet_view_and_wait, args=(), daemon=True
                        )
                        th.start()
            else:
                print(line)

    def open_flet_view_and_wait(self):
        self.fvp, self.pid_file = open_flet_view(
            self.page_url, self.assets_dir, self.hidden
        )
        self.fvp.wait()
        self.p.send_signal(signal.SIGTERM)
        self.terminate.set()

    def restart_program(self):
        self.is_running = False
        self.p.send_signal(signal.SIGTERM)
        self.p.wait()
        self.start_process()

    def print_qr_code(self, orig_url: str, android: bool):
        u = urlparse(orig_url)
        ip_addr = get_local_ip()
        lan_url = urlunparse(
            (u.scheme, f"{ip_addr}:{u.port}", u.path, None, None, None)
        )
        # self.clear_console()
        print("App is running on:", lan_url)
        print("")
        qr_url = (
            urlunparse(
                (
                    "https",
                    "android.flet.dev",
                    quote(f"{ip_addr}:{u.port}{u.path}", safe="/"),
                    None,
                    None,
                    None,
                )
            )
            if android
            else urlunparse(
                ("flet", "flet-host", quote(lan_url, safe=""), None, None, None)
            )
        )
        # print(qr_url)
        qr = qrcode.QRCode()
        qr.add_data(qr_url)
        qr.print_ascii(invert=True)
        # qr.print_tty()
        print("")
        print("Scan QR code above with Camera app.")

    def clear_console(self):
        if platform.system() == "Windows":
            if platform.release() in {"10", "11"}:
                subprocess.run(
                    "", shell=True
                )  # Needed to fix a bug regarding Windows 10; not sure about Windows 11
                print("\033c", end="")
            else:
                subprocess.run(["cls"])
        else:  # Linux and Mac
            print("\033c", end="")
