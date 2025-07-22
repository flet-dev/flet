import asyncio
import os
import subprocess

import flet as ft

os.environ["FLET_PLATFORM"] = "macos"


class FlutterTest:
    def __init__(self, flutter_app_dir: str, tcp_port: int = 8550):
        self.flutter_app_dir = flutter_app_dir
        self.tcp_port = tcp_port
        self.flutter_process = None
        self.page = None

    async def start(self):
        """Start Flet app and Flutter test process."""

        page_ready = asyncio.Event()

        # start Flet app
        def main(page: ft.Page):
            page_ready.set()
            self.page = page

        asyncio.create_task(ft.run_async(main, port=self.tcp_port, view=None))
        print("Started Flet app")

        # start Flutter test
        env = os.environ.copy()
        env["FLET_TEST_APP_PORT"] = str(self.tcp_port)
        self.flutter_process = subprocess.Popen(
            ["flutter", "test", "integration_test", "-d", "macos"],
            cwd=self.flutter_app_dir,
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
        )
        print("Started Flutter test process.")
        print("Waiting for a Flet session...")
        await page_ready.wait()

    async def teardown(self):
        """Teardown Flutter process."""

        if self.flutter_process:
            print("Waiting for Flutter test process to exit...")
            self.flutter_process.terminate()
            try:
                self.flutter_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print("Flutter test process did not terminate in time, killing it...")
                self.flutter_process.kill()
