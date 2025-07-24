import asyncio
import logging
import os
import platform
import subprocess
from io import BytesIO
from pathlib import Path
from typing import Any, Optional

import flet as ft
import numpy as np
from flet.utils.platform_utils import get_bool_env_var
from PIL import Image
from skimage.metrics import structural_similarity as ssim


class FletTestApp:
    def __init__(
        self,
        flutter_app_dir: os.PathLike,
        flet_app_main: Any = None,
        test_path: Optional[str] = None,
        tcp_port: int = 8550,
    ):
        self.test_path = test_path
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

        tcp_addr = "127.0.0.1"

        flet_test_platform = os.getenv("FLET_TEST_PLATFORM")
        if flet_test_platform == "android":
            tcp_addr = "10.0.2.2"

        if flet_test_device is not None:
            flutter_args.extend(["-d", flet_test_device])

        app_url = f"tcp://{tcp_addr}:{self.tcp_port}"
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

    def assert_screenshot(self, name: str, screenshot: bytes):
        assert self.test_path, "test_path must be set to work with screenshots"
        # if this is set then screenshot is saved as a golden image
        # without doing comparison
        golden_mode = get_bool_env_var("FLET_TEST_GOLDEN")
        golden_image_path = Path(self.test_path).parent.joinpath(
            "golden",
            Path(self.test_path).stem.removeprefix("test_"),
            f"{name.removeprefix('test_')}.png",
        )

        if golden_mode:
            # save image
            golden_image_path.parent.mkdir(parents=True, exist_ok=True)
            with open(golden_image_path, "bw") as f:
                f.write(screenshot)
        else:
            # load image and compare with provided screenshot
            if not golden_image_path.exists():
                raise Exception(f"Golden image not found: {golden_image_path}")
            golden_img = self.load_image_from_file(golden_image_path)
            img = self.load_image_from_bytes(screenshot)
            assert self.compare_images_rgb(golden_img, img) > 99.0, (
                "Screenshots are not identical"
            )

    def load_image_from_file(self, file_name):
        return Image.open(file_name).convert("RGB")

    def load_image_from_bytes(self, data: bytes) -> Image.Image:
        return Image.open(BytesIO(data)).convert("RGB")

    def compare_images_rgb(self, img1, img2) -> float:
        """Returns similarity as a percentage using color-aware SSIM."""
        # Resize if needed
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)

        arr1 = np.array(img1)
        arr2 = np.array(img2)

        # Use SSIM in RGB mode (3-channel)
        similarity, _ = ssim(arr1, arr2, channel_axis=-1, full=True)
        return similarity * 100
