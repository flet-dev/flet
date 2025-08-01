import asyncio
import logging
import os
import platform
from io import BytesIO
from pathlib import Path
from typing import Any, Optional

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

import flet as ft
from flet.controls.control import Control
from flet.testing.tester import Tester
from flet.utils.network import get_free_tcp_port
from flet.utils.platform_utils import get_bool_env_var

pixel_ratio = float(os.getenv("FLET_TEST_SCREENSHOTS_PIXEL_RATIO", "2.0"))
similarity_threshold = float(os.getenv("FLET_TEST_SIMILARITY_THRESHOLD", "99.0"))


class FletTestApp:
    def __init__(
        self,
        flutter_app_dir: os.PathLike,
        flet_app_main: Any = None,
        test_path: Optional[str] = None,
        tcp_port: Optional[int] = None,
    ):
        """
        Flet app test controller is a bridge that connects together
        a Flet app in Python and a running integration test in Flutter.
        """
        self.__test_path = test_path
        self.__flet_app_main = flet_app_main
        self.__flutter_app_dir = flutter_app_dir
        self.__tcp_port = tcp_port
        self.__flutter_process: Optional[asyncio.subprocess.Process] = None
        self.__page = None
        self.__tester = None

    @property
    def page(self) -> ft.Page:
        """
        Returns an instance of Flet's app [`Page`][flet.Page].
        """
        assert self.__page
        return self.__page

    @property
    def tester(self) -> Tester:
        """
        Returns an instance of [`Tester`][flet.testing.Tester] class
        that programmatically interacts with page controls and the test environment.
        """
        assert self.__tester
        return self.__tester

    async def start(self):
        """
        Starts Flet app and Flutter integration test process.
        """

        ready = asyncio.Event()

        async def main(page: ft.Page):
            self.__page = page
            self.__tester = Tester()
            page.services.append(self.__tester)
            page.update()

            if asyncio.iscoroutinefunction(self.__flet_app_main):
                await self.__flet_app_main(page)
            elif callable(self.__flet_app_main):
                self.__flet_app_main(page)
            ready.set()

        if not self.__tcp_port:
            self.__tcp_port = get_free_tcp_port()

        asyncio.create_task(ft.run_async(main, port=self.__tcp_port, view=None))
        print("Started Flet app")

        stdout = asyncio.subprocess.DEVNULL
        stderr = asyncio.subprocess.DEVNULL
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            stdout = None
            stderr = None

        flutter_args = ["flutter", "test", "integration_test"]

        self.test_platform = os.getenv("FLET_TEST_PLATFORM")
        if self.test_platform is None:
            self.test_platform = {
                "Windows": "windows",
                "Linux": "linux",
                "Darwin": "macos",
            }.get(platform.system(), "unknown")

        self.test_device = os.getenv("FLET_TEST_DEVICE", self.test_platform)

        tcp_addr = "10.0.2.2" if self.test_platform == "android" else "127.0.0.1"

        if self.test_device:
            flutter_args += ["-d", self.test_device]

        app_url = f"tcp://{tcp_addr}:{self.__tcp_port}"
        flutter_args += [f"--dart-define=FLET_TEST_APP_URL={app_url}"]

        self.__flutter_process = await asyncio.create_subprocess_exec(
            *flutter_args,
            cwd=str(self.__flutter_app_dir),
            stdout=stdout,
            stderr=stderr,
        )

        print("Started Flutter test process.")
        print("Waiting for a Flet client to connect...")

        while not ready.is_set():
            await asyncio.sleep(0.2)
            if self.__flutter_process.returncode is not None:
                raise RuntimeError(
                    f"Flutter process exited early with code {self.__flutter_process.returncode}"
                )

    async def teardown(self):
        """
        Teardown Flutter integration test process.
        """

        await self.tester.teardown()

        if self.__flutter_process:
            print("Waiting for Flutter test process to exit...")
            try:
                await asyncio.wait_for(self.__flutter_process.wait(), timeout=10)
                print("Flutter test process has exited.")
            except asyncio.TimeoutError:
                print("Flutter test process did not exit in time, terminating it...")
                self.__flutter_process.terminate()
                # Optionally ensure it terminates
                try:
                    await asyncio.wait_for(self.__flutter_process.wait(), timeout=5)
                except asyncio.TimeoutError:
                    print("Force killing Flutter test process...")
                    self.__flutter_process.kill()

    async def assert_control_screenshot(self, name: str, control: Control):
        """
        Adds control to a clean page, takes a screenshot and compares it with
        a golden copy or takes golden screenshot if `FLET_TEST_GOLDEN=1`
        environment variable is set.

        Args:
            name: Screenshot name - will be used as a base for a screenshot filename.
            control: Control to take a screenshot of.
        """
        # clean page
        self.page.clean()

        # add control and take screenshot
        screenshot = ft.Screenshot(control)
        self.page.add(screenshot)
        await self.tester.pump_and_settle()
        self.assert_screenshot(
            name,
            await screenshot.capture_async(pixel_ratio=pixel_ratio),
        )

    def assert_screenshot(self, name: str, screenshot: bytes):
        """
        Compares provided screenshot with a golden copy or takes golden screenshot
        if `FLET_TEST_GOLDEN=1` environment variable is set.

        Args:
            name: Screenshot name - will be used as a base for a screenshot filename.
            screenshot: Screenshot contents in PNG format.
        """
        assert self.test_platform, (
            "FLET_TEST_PLATFORM must be set to test with screenshots"
        )
        assert self.__test_path, "test_path must be set to test with screenshots"

        golden_mode = get_bool_env_var("FLET_TEST_GOLDEN")
        golden_image_path = (
            Path(self.__test_path).parent
            / "golden"
            / self.test_platform
            / Path(self.__test_path).stem.removeprefix("test_")
            / f"{name.removeprefix('test_')}.png"
        )

        if golden_mode:
            golden_image_path.parent.mkdir(parents=True, exist_ok=True)
            with open(golden_image_path, "bw") as f:
                f.write(screenshot)
        else:
            if not golden_image_path.exists():
                raise Exception(
                    f"Golden image for {name} not found: {golden_image_path}"
                )
            golden_img = self._load_image_from_file(golden_image_path)
            img = self._load_image_from_bytes(screenshot)
            similarity = self._compare_images_rgb(golden_img, img)
            print(f"Similarity for {name}: {similarity}%")
            if similarity <= similarity_threshold:
                actual_image_path = (
                    golden_image_path.parent
                    / f"{golden_image_path.parent.stem}_{golden_image_path.stem}_actual.png"
                )
                with open(actual_image_path, "bw") as f:
                    f.write(screenshot)
            assert similarity > similarity_threshold, (
                f"{name} screenshots are not identical"
            )

    def _load_image_from_file(self, file_name):
        return Image.open(file_name)

    def _load_image_from_bytes(self, data: bytes) -> Image.Image:
        return Image.open(BytesIO(data))

    def _compare_images_rgb(self, img1, img2) -> float:
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)
        arr1 = np.array(img1)
        arr2 = np.array(img2)
        similarity, _ = ssim(arr1, arr2, channel_axis=-1, full=True)
        return similarity * 100
