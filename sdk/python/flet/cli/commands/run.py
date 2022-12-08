import argparse
import logging
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time
from flet.cli.commands.base import BaseCommand
from flet.flet import open_flet_view
from flet.utils import get_free_tcp_port, is_windows, open_in_browser
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Command(BaseCommand):
    """
    Run Flet app
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("script", type=str, help="path to a Python script")
        parser.add_argument(
            "-p",
            "--port",
            dest="port",
            type=int,
            default=None,
            help="custom TCP port to run Flet app on",
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

    def handle(self, options: argparse.Namespace) -> None:
        # print("RUN COMMAND", options)
        script_path = options.script
        if not os.path.isabs(options.script):
            script_path = str(Path(os.getcwd()).joinpath(options.script).resolve())

        if not Path(script_path).exists():
            print(f"File not found: {script_path}")
            exit(1)

        script_dir = os.path.dirname(script_path)

        port = options.port
        if options.port is None:
            port = get_free_tcp_port()

        my_event_handler = Handler(
            [sys.executable, "-u", script_path],
            None if options.directory or options.recursive else script_path,
            port,
            options.web,
            options.hidden,
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

        if my_event_handler.fvp is not None and not is_windows():
            try:
                logging.debug(f"Flet View process {my_event_handler.fvp.pid}")
                os.kill(my_event_handler.fvp.pid + 1, signal.SIGKILL)
            except:
                pass
        my_observer.stop()
        my_observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, args, script_path, port, web, hidden) -> None:
        super().__init__()
        self.args = args
        self.script_path = script_path
        self.port = port
        self.web = web
        self.hidden = hidden
        self.last_time = time.time()
        self.is_running = False
        self.fvp = None
        self.page_url_prefix = f"PAGE_URL_{time.time()}"
        self.page_url = None
        self.terminate = threading.Event()
        self.start_process()

    def start_process(self):
        p_env = {**os.environ}
        if self.port is not None:
            p_env["FLET_SERVER_PORT"] = str(self.port)
        p_env["FLET_DISPLAY_URL_PREFIX"] = self.page_url_prefix

        self.p = subprocess.Popen(self.args, env=p_env, stdout=subprocess.PIPE)
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
            line = line.decode("utf-8").rstrip("\r\n")
            if line.startswith(self.page_url_prefix):
                if not self.page_url:
                    self.page_url = line[len(self.page_url_prefix) + 1 :]
                    print(self.page_url)
                    if self.web:
                        open_in_browser(self.page_url)
                    else:
                        th = threading.Thread(
                            target=self.open_flet_view_and_wait, args=(), daemon=True
                        )
                        th.start()
            else:
                print(line)

    def open_flet_view_and_wait(self):
        self.fvp = open_flet_view(self.page_url, self.hidden)
        self.fvp.wait()
        self.p.kill()
        self.terminate.set()

    def restart_program(self):
        self.is_running = False
        self.p.kill()
        self.p.wait()
        time.sleep(0.5)
        self.start_process()
