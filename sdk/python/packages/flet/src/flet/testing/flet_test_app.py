import asyncio
import logging
import os
import platform
import subprocess

import flet as ft


class FletTestApp:
    def __init__(
        self, flutter_app_dir: os.PathLike, flet_app_main=None, tcp_port: int = 8550
    ):
        self.flet_app_main = flet_app_main
        self.flutter_app_dir = flutter_app_dir
        self.tcp_port = tcp_port
        self.flutter_process = None
        self.__page = None
        self.__tester = None

    @property
    def page(self) -> ft.Page:
        assert self.__page
        return self.__page

    @property
    def tester(self) -> ft.Tester:
        assert self.__tester
        return self.__tester

    async def start(self):
        """Start Flet app and Flutter test process."""

        ready = asyncio.Event()

        # start Flet app
        async def main(page: ft.Page):
            self.__page = page
            self.__tester = ft.Tester()
            page.services.append(self.__tester)
            page.update()

            if asyncio.iscoroutinefunction(self.flet_app_main):
                await self.flet_app_main(page)
            elif callable(self.flet_app_main):
                self.flet_app_main(page)
            ready.set()

        asyncio.create_task(ft.run_async(main, port=self.tcp_port, view=None))
        print("Started Flet app")

        pipe = subprocess.DEVNULL
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            pipe = None

        flutter_args = ["flutter", "test", "integration_test"]

        flet_test_device = os.getenv("FLET_TEST_DEVICE")
        if flet_test_device is None:
            if platform.system() == "Windows":
                flet_test_device = "windows"
            elif platform.system() == "Linux":
                flet_test_device = "linux"
            elif platform.system() == "Darwin":
                flet_test_device = "macos"

        if flet_test_device is not None:
            flutter_args.extend(["-d", flet_test_device])

        app_url = f"tcp://127.0.0.1:{self.tcp_port}"
        flutter_args.append(f"--dart-define=FLET_TEST_APP_URL={app_url}")

        # start Flutter test
        self.flutter_process = subprocess.Popen(
            flutter_args, cwd=str(self.flutter_app_dir), stdout=pipe, stderr=pipe
        )
        print("Started Flutter test process.")
        print("Waiting for a Flet session...")
        while not ready.is_set():
            await asyncio.sleep(0.2)
            if self.flutter_process.poll() is not None:
                raise RuntimeError(
                    f"Flutter process exited early with code {self.flutter_process.returncode}"
                )

    async def teardown(self):
        """Teardown Flutter process."""

        await self.tester.teardown()

        if self.flutter_process:
            print("Waiting for Flutter test process to exit...")
            try:
                self.flutter_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print("Flutter test process did exit in time, terminating it...")
                self.flutter_process.terminate()  # or .kill() ?
