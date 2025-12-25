import asyncio
import inspect
import logging
import os
import platform
import tempfile
from collections.abc import Iterable
from io import BytesIO
from pathlib import Path
from typing import Any, Optional
from enum import Enum

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

import flet as ft
from flet.controls.control import Control
from flet.testing.tester import Tester
from flet.utils.network import get_free_tcp_port
from flet.utils.platform_utils import get_bool_env_var

__all__ = ["FletTestApp"]


class DisposalMode(Enum):
    """
    Indicates the way in which a frame is treated after being displayed.
    """

    DEFAULT = 0
    """
    No disposal method specified
    """

    NONE = 1
    """
    Do not dispose
    """

    BACKGROUND = 2
    """
    Restore to background color.
    """

    PREVIOUS = 3
    """
    Restore to previous content.
    """


class FletTestApp:
    """
    Flet app test controller coordinates running a Python-based
    Flet app alongside a Flutter integration test.

    This class launches the Python Flet app, starts the Flutter test process,
    and facilitates programmatic interaction with the app's controls for
    automated UI testing.

    Args:
        flutter_app_dir:
            Path to the Flutter app directory containing integration tests.

        flet_app_main:
            A callable or coroutine function representing the main entry point
            of the Flet app under test. This will be invoked with a
            [`Page`][flet.] instance when the app starts.

        assets_dir:
            Path to the directory containing static assets for the Flet app.
            Defaults to `"assets"` if not provided.

        test_path:
            Path to the Python test file. Used to determine the location for
            golden screenshot comparisons.

        tcp_port:
            TCP port to run the Flet server on. If not specified, a free port
            is automatically selected.

        test_platform:
            Target platform for the Flutter integration test
            (e.g., `"windows"`, `"linux"`, `"macos"`, `"android"`, `"ios"`).
            Env override: `FLET_TEST_PLATFORM`.

        test_device:
            Target device ID or name for the Flutter integration test.
            Env override: `FLET_TEST_DEVICE`.

        capture_golden_screenshots:
            If `True`, screenshots taken during tests are stored as golden
            reference images. Env override: `FLET_TEST_GOLDEN=1`.

        screenshots_pixel_ratio:
            Device pixel ratio to use when capturing screenshots.
            Env override: `FLET_TEST_SCREENSHOTS_PIXEL_RATIO`.

        screenshots_similarity_threshold:
            Minimum percentage similarity required for screenshot comparisons
            to pass. Env override: `FLET_TEST_SCREENSHOTS_SIMILARITY_THRESHOLD`.

        use_http:
            If `True`, use HTTP transport instead of TCP for Flet client-server
            communication. Env override: `FLET_TEST_USE_HTTP=1`.

        disable_fvm:
            If `True`, do not invoke `fvm` when running the Flutter test
            process. Env override: `FLET_TEST_DISABLE_FVM=1`.

        skip_pump_and_settle:
            If `True`, the initial `pump_and_settle` after app start is skipped.

    Environment Variables:
        - `FLET_TEST_PLATFORM`: Overrides `test_platform`.
        - `FLET_TEST_DEVICE`: Overrides `test_device`.
        - `FLET_TEST_GOLDEN`: Enables golden screenshot capture when set to `1`.
        - `FLET_TEST_SCREENSHOTS_PIXEL_RATIO`: Overrides `screenshots_pixel_ratio`.
        - `FLET_TEST_SCREENSHOTS_SIMILARITY_THRESHOLD`:
            Overrides `screenshots_similarity_threshold`.
        - `FLET_TEST_USE_HTTP`: Enables HTTP transport when set to `1`.
        - `FLET_TEST_DISABLE_FVM`: Disables `fvm` usage when set to `1`.
    """

    def __init__(
        self,
        flutter_app_dir: os.PathLike,
        flet_app_main: Any = None,
        assets_dir: Optional[os.PathLike] = None,
        test_path: Optional[str] = None,
        tcp_port: Optional[int] = None,
        test_platform: Optional[str] = None,
        test_device: Optional[str] = None,
        capture_golden_screenshots: bool = False,
        screenshots_pixel_ratio: float = 2.0,
        screenshots_similarity_threshold: float = 99.0,
        use_http: bool = False,
        disable_fvm: bool = False,
        skip_pump_and_settle: bool = False,
    ):
        self.test_platform = os.getenv("FLET_TEST_PLATFORM", test_platform)
        self.test_device = os.getenv("FLET_TEST_DEVICE", test_device)
        self.__golden = (
            get_bool_env_var("FLET_TEST_GOLDEN") or capture_golden_screenshots
        )
        self.screenshots_pixel_ratio = float(
            os.getenv("FLET_TEST_SCREENSHOTS_PIXEL_RATIO", screenshots_pixel_ratio)
        )
        self.screenshots_similarity_threshold = float(
            os.getenv(
                "FLET_TEST_SCREENSHOTS_SIMILARITY_THRESHOLD",
                screenshots_similarity_threshold,
            )
        )
        self.__disable_fvm = get_bool_env_var("FLET_TEST_DISABLE_FVM") or disable_fvm
        self.__use_http = get_bool_env_var("FLET_TEST_USE_HTTP") or use_http
        self.__test_path = test_path
        self.__flet_app_main = flet_app_main
        self.__skip_pump_and_settle = skip_pump_and_settle
        self.__flutter_app_dir = flutter_app_dir
        self.__assets_dir = assets_dir or "assets"
        self.__tcp_port = tcp_port
        self.__flutter_process: Optional[asyncio.subprocess.Process] = None
        self.__page = None
        self.__tester: Tester | None = None

    @property
    def page(self) -> ft.Page:
        """
        Returns an instance of Flet's app [`Page`][flet.].
        """
        if self.__page is None:
            raise RuntimeError("page is not initialized")
        return self.__page

    @property
    def tester(self) -> Tester:
        """
        Returns an instance of [`Tester`][flet.testing.] class
        that programmatically interacts with page controls and the test environment.
        """
        if self.__tester is None:
            raise RuntimeError("tester is not initialized")
        return self.__tester

    async def start(self):
        """
        Starts Flet app and Flutter integration test process.
        """

        ready = asyncio.Event()

        async def main(page: ft.Page):
            self.__page = page
            self.__tester = Tester()
            page.theme_mode = ft.ThemeMode.LIGHT
            page.update()

            if inspect.iscoroutinefunction(self.__flet_app_main):
                await self.__flet_app_main(page)
            elif callable(self.__flet_app_main):
                self.__flet_app_main(page)
            if not self.__skip_pump_and_settle:
                await self.__tester.pump_and_settle()
            ready.set()

        if not self.__tcp_port:
            self.__tcp_port = get_free_tcp_port()

        if self.__use_http:
            os.environ["FLET_FORCE_WEB_SERVER"] = "true"

        asyncio.create_task(
            ft.run_async(
                main, port=self.__tcp_port, assets_dir=str(self.__assets_dir), view=None
            )
        )
        print("Started Flet app")

        stdout = asyncio.subprocess.DEVNULL
        stderr = asyncio.subprocess.DEVNULL
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            stdout = None
            stderr = None

        flutter_args = ["fvm", "flutter", "test", "integration_test"]

        if self.__disable_fvm:
            flutter_args.pop(0)

        if self.test_platform is None:
            self.test_platform = {
                "Windows": "windows",
                "Linux": "linux",
                "Darwin": "macos",
            }.get(platform.system(), "unknown")

        if not self.test_device:
            self.test_device = self.test_platform

        tcp_addr = "10.0.2.2" if self.test_platform == "android" else "127.0.0.1"
        protocol = "http" if self.__use_http else "tcp"

        if self.test_device:
            flutter_args += ["-d", self.test_device]

        app_url = f"{protocol}://{tcp_addr}:{self.__tcp_port}"
        flutter_args += [f"--dart-define=FLET_TEST_APP_URL={app_url}"]

        if not self.__use_http:
            temp_path = Path(tempfile.gettempdir()) / "flet_app_pid.txt"
            flutter_args += [f"--dart-define=FLET_TEST_PID_FILE_PATH={temp_path}"]
            if self.__assets_dir:
                flutter_args += [
                    f"--dart-define=FLET_TEST_ASSETS_DIR={self.__assets_dir}"
                ]

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
                    "Flutter process exited early with code "
                    f"{self.__flutter_process.returncode}"
                )

    async def teardown(self):
        """
        Teardown Flutter integration test process.
        """

        await self.tester.teardown()

        if self.__flutter_process:
            print("\nWaiting for Flutter test process to exit...")
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

    def resize_page(self, width: int, height: int):
        """
        Resizes the page window to the specified width and height.
        """
        if self.page.window.width is None or self.page.window.height is None:
            return

        chrome_width = self.page.window.width - self.page.width
        chrome_height = self.page.window.height - self.page.height
        self.page.window.width = width + chrome_width
        self.page.window.height = height + chrome_height

    async def wrap_page_controls_in_screenshot(
        self,
        margin=10,
        pump_times: int = 0,
        pump_duration: Optional[ft.DurationValue] = None,
    ) -> ft.Screenshot:
        """
        Wraps provided controls in a Screenshot control.
        """
        controls = list(self.page.controls)
        self.page.controls = [
            scr := ft.Screenshot(
                ft.Column(controls, margin=margin, intrinsic_width=True)
            )
        ]  # type: ignore
        self.page.update()
        await self.tester.pump_and_settle()
        for _ in range(0, pump_times):
            await self.tester.pump(duration=pump_duration)
        return scr

    async def take_page_controls_screenshot(
        self,
        pixel_ratio: Optional[float] = None,
        pump_times: int = 0,
        pump_duration: Optional[ft.DurationValue] = None,
    ) -> bytes:
        """
        Takes a screenshot of all controls on the current page.
        """
        scr = await self.wrap_page_controls_in_screenshot(
            pump_times=pump_times, pump_duration=pump_duration
        )
        return await scr.capture(
            pixel_ratio=pixel_ratio or self.screenshots_pixel_ratio
        )

    async def assert_control_screenshot(
        self,
        name: str,
        control: Control,
        pump_times: int = 0,
        pump_duration: Optional[ft.DurationValue] = None,
        expand_screenshot: bool = False,
        similarity_threshold: float = 0,
    ):
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
        await self.tester.pump_and_settle()

        # add control and take screenshot
        screenshot = ft.Screenshot(control, expand=expand_screenshot)
        self.page.add(screenshot)
        await self.tester.pump_and_settle()
        for _ in range(0, pump_times):
            await self.tester.pump(duration=pump_duration)
        self.assert_screenshot(
            name,
            await screenshot.capture(pixel_ratio=self.screenshots_pixel_ratio),
            similarity_threshold=similarity_threshold,
        )

    def assert_screenshot(
        self, name: str, screenshot: bytes, similarity_threshold: float = 0
    ):
        """
        Compares provided screenshot with a golden copy or takes golden screenshot
        if `FLET_TEST_GOLDEN=1` environment variable is set.

        Args:
            name: Screenshot name - will be used as a base for a screenshot filename.
            screenshot: Screenshot contents in PNG format.
        """
        if not self.test_platform:
            raise RuntimeError(
                "FLET_TEST_PLATFORM environment variable must be set "
                "to test with screenshots"
            )
        if not self.__test_path:
            raise RuntimeError("test_path must be set to test with screenshots")

        golden_image_path = (
            Path(self.__test_path).parent
            / "golden"
            / self.test_platform
            / Path(self.__test_path).stem.removeprefix("test_")
            / f"{name.removeprefix('test_')}.png"
        )

        if self.__golden:
            golden_image_path.parent.mkdir(parents=True, exist_ok=True)
            with open(golden_image_path, "bw") as f:
                f.write(screenshot)
        else:
            if not golden_image_path.exists():
                raise RuntimeError(
                    f"Golden image for {name} not found: {golden_image_path}"
                )
            golden_img = self._load_image_from_file(golden_image_path)
            img = self._load_image_from_bytes(screenshot)
            similarity = self._compare_images_rgb(golden_img, img)
            print(f"Similarity for {name}: {similarity}%")
            if similarity_threshold == 0:
                similarity_threshold = self.screenshots_similarity_threshold
            if similarity <= similarity_threshold:
                actual_image_path = (
                    golden_image_path.parent
                    / f"{golden_image_path.parent.stem}_{golden_image_path.stem}_actual.png"  # noqa: E501
                )
                with open(actual_image_path, "bw") as f:
                    f.write(screenshot)
            assert similarity > similarity_threshold, (
                f"{name} screenshots are not identical "
                f"(similarity: {similarity}% <= {similarity_threshold}%)"
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

    def create_gif(
        self,
        image_names: Iterable[str],
        output_name: str,
        *,
        duration: int = 1000,
        loop: int = 0,
        disposal: DisposalMode = DisposalMode.DEFAULT,
    ) -> Path:
        """Create an animated GIF from a sequence of image files.

        Args:
            image_names: Iterable of file name stems (without ``.png``) in the
                order they should appear in the animation.
            output_name: Base name for the resulting animation. The ``.gif``
                extension is added automatically and the file is stored in the
                same directory as the provided frames.
            duration: Frame duration in milliseconds. Defaults to ``300``.
            loop: Number of times the GIF should repeat (``0`` means infinite).

        Returns:
            Path to the generated GIF file.

        Raises:
            ValueError: If ``image_names`` is empty.
            FileNotFoundError: If any referenced image file does not exist.
        """

        if not self.__test_path:
            raise ValueError("test_path must be set to create GIF animations")
        if not self.test_platform:
            raise ValueError("test_platform must be set to create GIF animations")

        names = list(image_names)
        if not names:
            raise ValueError("image_names must contain at least one entry")

        stem = output_name
        golden_dir = (
            Path(self.__test_path).parent
            / "golden"
            / self.test_platform
            / Path(self.__test_path).stem.removeprefix("test_")
        )
        output = golden_dir / f"{stem}.gif"
        output.parent.mkdir(parents=True, exist_ok=True)

        frames: list[Image.Image] = []
        try:
            for name in names:
                path = golden_dir / f"{name}.png"
                if not path.exists():
                    raise FileNotFoundError(path)

                frames.append(
                    Image.open(path)
                    .convert("RGB")
                    .convert(
                        "P",
                        palette=Image.ADAPTIVE,
                        colors=256,
                    )
                )

            first, *rest = frames
            first.save(
                output,
                save_all=True,
                append_images=rest,
                duration=duration,
                loop=loop,
                optimize=True,
                disposal=disposal.value,
            )
        finally:
            for frame in frames:
                frame.close()

        return output
