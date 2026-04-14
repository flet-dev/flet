import asyncio
import inspect
import logging
import os
import platform
import tempfile
from collections.abc import Iterable, Sequence
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

import flet as ft
from flet.controls.control import Control
from flet.testing.tester import Tester
from flet.utils.network import get_free_tcp_port
from flet.utils.platform_utils import get_bool_env_var

if TYPE_CHECKING:
    from flet.app import AppCallable

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
    Flet app test controller coordinates running a Python-based Flet app alongside \
    a Flutter integration test.

    This class launches the Python Flet app, starts the Flutter test process,
    and facilitates programmatic interaction with the app's controls for
    automated UI testing.

    Args:
        flutter_app_dir:
            Path to the Flutter app directory containing integration tests.

        flet_app_main:
            A callable or coroutine function representing the main entry point
            of the Flet app under test. This will be invoked with a
            :class:`~flet.Page` instance when the app starts.

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
        flet_app_main: Optional["AppCallable"] = None,
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
        Returns an instance of Flet's app :class:`~flet.Page`.
        """
        if self.__page is None:
            raise RuntimeError("page is not initialized")
        return self.__page

    @property
    def tester(self) -> Tester:
        """
        Returns an instance of `Tester` class that programmatically \
        interacts with page controls and the test environment.
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
            """
            Initializes the test page and runs the user-provided Flet app entry point.

            Args:
                page: Connected app :class:`~flet.Page` instance.
            """
            self.__page = page
            self.__tester = Tester()
            page.theme_mode = ft.ThemeMode.LIGHT
            page.update()

            if inspect.iscoroutinefunction(self.__flet_app_main):
                await self.__flet_app_main(page)
            elif callable(self.__flet_app_main):
                self.__flet_app_main(page)
            if not self.__skip_pump_and_settle:
                await self.__pump_and_settle_with_timeout("start")
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
        try:
            await self.tester.teardown(timeout=10)
        except (RuntimeError, TimeoutError) as e:
            print(f"Tester teardown failed: {e}")

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
        await self.__pump_and_settle_with_timeout("wrap_page_controls_in_screenshot")
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
        Adds control to a clean page, takes a screenshot and compares it with a golden \
        copy or takes golden screenshot if `FLET_TEST_GOLDEN=1` environment variable \
        is set.

        Args:
            name: Screenshot name - will be used as a base for a screenshot filename.
            control: Control to take a screenshot of.
        """
        # clean page
        self.page.clean()
        await self.__pump_and_settle_with_timeout("assert_control_screenshot-clean")

        # add control and take screenshot
        screenshot = ft.Screenshot(control, expand=expand_screenshot)
        self.page.add(screenshot)
        await self.__pump_and_settle_with_timeout("assert_control_screenshot-add")
        for _ in range(0, pump_times):
            await self.tester.pump(duration=pump_duration)
        self.assert_screenshot(
            name,
            await screenshot.capture(pixel_ratio=self.screenshots_pixel_ratio),
            similarity_threshold=similarity_threshold,
        )

    async def __pump_and_settle_with_timeout(self, stage: str):
        try:
            await self.tester.pump_and_settle(timeout=self.__pump_and_settle_timeout)
        except TimeoutError as e:
            raise TimeoutError(
                f"Timed out during {stage}: "
                f"tester.pump_and_settle() did not complete in "
                f"{self.__pump_and_settle_timeout} seconds"
            ) from e

    def assert_screenshot(
        self, name: str, screenshot: bytes, similarity_threshold: float = 0
    ):
        """
        Compares provided screenshot with a golden copy or takes golden screenshot if \
        `FLET_TEST_GOLDEN=1` environment variable is set.

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

    def _load_image_from_file(self, file_name: Union[str, Path]) -> Image.Image:
        """
        Loads an image from disk.

        Args:
            file_name: Path to an image file.

        Returns:
            Loaded Pillow image object.
        """
        return Image.open(file_name)

    def _load_image_from_bytes(self, data: bytes) -> Image.Image:
        """
        Loads an image from PNG bytes.

        Args:
            data: Image data bytes.

        Returns:
            Loaded Pillow image object.
        """
        return Image.open(BytesIO(data))

    def _compare_images_rgb(self, img1: Image.Image, img2: Image.Image) -> float:
        """
        Calculates structural similarity between two RGB images.

        If image sizes differ, the second image is resized to match the first image
        before comparison.

        Args:
            img1: Reference image.
            img2: Image to compare.

        Returns:
            Similarity percentage in the `0..100` range.
        """
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)
        arr1 = np.array(img1)
        arr2 = np.array(img2)
        similarity, _ = ssim(arr1, arr2, channel_axis=-1, full=True)
        return similarity * 100

    def create_gif(
        self,
        image_names: Optional[Iterable[str]] = None,
        output_name: str = "",
        *,
        frames: Optional[Iterable[bytes]] = None,
        duration: Union[int, Sequence[int]] = 1000,
        loop: int = 0,
        disposal: DisposalMode = DisposalMode.DEFAULT,
    ) -> Path:
        """Create an animated GIF from a sequence of PNG frames.

        Exactly one of ``image_names`` or ``frames`` must be provided.

        Args:
            image_names: Iterable of file name stems (without ``.png``) in the
                order they should appear in the animation. Frames are read from
                disk under the test's golden directory.
            output_name: Base name for the resulting animation. The ``.gif``
                extension is added automatically and the file is stored in the
                same directory as the source frames.
            frames: Iterable of PNG-encoded frame bytes to use directly, in the
                order they should appear in the animation. Typically paired
                with :meth:`Page.take_animation`.
            duration: Frame duration in milliseconds. Either a single ``int``
                applied to every frame, or a sequence of ``int`` with one
                entry per frame. Pass the same list used for
                ``take_animation(frame_delays_ms=...)`` to have the GIF play
                at the same pace it was captured.
            loop: Number of times the GIF should repeat (``0`` means infinite).
            disposal: Frame disposal mode.

        Returns:
            Path to the generated GIF file.

        Raises:
            ValueError: If neither or both of ``image_names`` / ``frames`` are
                given, the input is empty, or a ``duration`` sequence has a
                different length than the frame count.
            FileNotFoundError: If any referenced image file does not exist.
        """

        if not self.__test_path:
            raise ValueError("test_path must be set to create GIF animations")
        if not self.test_platform:
            raise ValueError("test_platform must be set to create GIF animations")
        if (image_names is None) == (frames is None):
            raise ValueError("Exactly one of image_names or frames must be provided")

        golden_dir = self._golden_dir()
        output = golden_dir / f"{output_name}.gif"
        output.parent.mkdir(parents=True, exist_ok=True)

        if image_names is not None:
            names = list(image_names)
            if not names:
                raise ValueError("image_names must contain at least one entry")
            frame_bytes_list: list[bytes] = []
            for name in names:
                path = golden_dir / f"{name}.png"
                if not path.exists():
                    raise FileNotFoundError(path)
                frame_bytes_list.append(path.read_bytes())
        else:
            frame_bytes_list = list(frames or ())

        gif_bytes = self._frames_to_gif_bytes(
            frame_bytes_list, duration, loop, disposal
        )
        output.write_bytes(gif_bytes)
        return output

    def _golden_dir(self) -> Path:
        return (
            Path(self.__test_path).parent
            / "golden"
            / self.test_platform
            / Path(self.__test_path).stem.removeprefix("test_")
        )

    def _frames_to_gif_bytes(
        self,
        frames: list[bytes],
        duration: Union[int, Sequence[int]],
        loop: int,
        disposal: DisposalMode,
    ) -> bytes:
        if not frames:
            raise ValueError("frames must contain at least one entry")
        gif_frames: list[Image.Image] = []
        try:
            for frame_bytes in frames:
                with Image.open(BytesIO(frame_bytes)) as img:
                    gif_frames.append(
                        img.convert("RGB").convert(
                            "P", palette=Image.ADAPTIVE, colors=256
                        )
                    )

            if isinstance(duration, int):
                save_duration: Union[int, list[int]] = duration
            else:
                save_duration = list(duration)
                if len(save_duration) != len(gif_frames):
                    raise ValueError(
                        f"duration sequence length ({len(save_duration)}) must "
                        f"match frame count ({len(gif_frames)})"
                    )

            first, *rest = gif_frames
            out = BytesIO()
            first.save(
                out,
                format="GIF",
                save_all=True,
                append_images=rest,
                duration=save_duration,
                loop=loop,
                optimize=True,
                disposal=disposal.value,
            )
            return out.getvalue()
        finally:
            for frame in gif_frames:
                frame.close()

    def assert_gif(
        self,
        name: str,
        frames: Iterable[bytes],
        *,
        duration: Union[int, Sequence[int]] = 1000,
        loop: int = 0,
        disposal: DisposalMode = DisposalMode.DEFAULT,
        similarity_threshold: float = 0,
    ):
        """Compare an animated GIF built from `frames` against a golden GIF.

        Builds the GIF in memory from the provided frames. If the
        `FLET_TEST_GOLDEN=1` environment variable is set, writes the GIF as
        the golden reference. Otherwise loads the existing golden GIF from
        disk and compares frame-by-frame via structural similarity, saving
        an `<name>_actual.gif` next to the golden on mismatch.

        Args:
            name: GIF name - will be used as a base for the GIF file name.
            frames: Iterable of PNG-encoded frame bytes. Typically the result
                of `Page.take_animation(...)`.
            duration: Frame duration in milliseconds. Either a single `int`
                or a per-frame sequence matching the number of frames.
            loop: Number of times the GIF should repeat (`0` means infinite).
            disposal: Frame disposal mode.
            similarity_threshold: Minimum acceptable per-frame SSIM (%). Uses
                `screenshots_similarity_threshold` when `0`.
        """
        if not self.test_platform:
            raise RuntimeError(
                "FLET_TEST_PLATFORM environment variable must be set to test with GIFs"
            )
        if not self.__test_path:
            raise RuntimeError("test_path must be set to test with GIFs")

        gif_bytes = self._frames_to_gif_bytes(list(frames), duration, loop, disposal)

        golden_gif_path = self._golden_dir() / f"{name.removeprefix('test_')}.gif"

        if self.__golden:
            golden_gif_path.parent.mkdir(parents=True, exist_ok=True)
            golden_gif_path.write_bytes(gif_bytes)
            return

        if not golden_gif_path.exists():
            raise RuntimeError(f"Golden GIF for {name} not found: {golden_gif_path}")

        similarity, frame_count_mismatch = self._compare_gifs(
            golden_gif_path, gif_bytes
        )
        print(f"Similarity for {name}: {similarity}%")
        if similarity_threshold == 0:
            similarity_threshold = self.screenshots_similarity_threshold

        if frame_count_mismatch or similarity <= similarity_threshold:
            actual_gif_path = (
                golden_gif_path.parent
                / f"{golden_gif_path.parent.stem}_{golden_gif_path.stem}_actual.gif"  # noqa: E501
            )
            actual_gif_path.write_bytes(gif_bytes)

        if frame_count_mismatch:
            raise AssertionError(frame_count_mismatch)
        assert similarity > similarity_threshold, (
            f"{name} GIFs are not identical "
            f"(similarity: {similarity}% <= {similarity_threshold}%)"
        )

    def _compare_gifs(
        self, golden_path: Path, current_bytes: bytes
    ) -> tuple[float, Optional[str]]:
        """Returns (min-per-frame similarity, frame-count-mismatch message)."""
        with (
            Image.open(golden_path) as golden,
            Image.open(BytesIO(current_bytes)) as current,
        ):
            if golden.n_frames != current.n_frames:
                return (
                    0.0,
                    f"GIF frame count mismatch: "
                    f"golden={golden.n_frames}, current={current.n_frames}",
                )
            similarities: list[float] = []
            for i in range(golden.n_frames):
                golden.seek(i)
                current.seek(i)
                similarities.append(
                    self._compare_images_rgb(
                        golden.convert("RGB"), current.convert("RGB")
                    )
                )
            return min(similarities), None

    __pump_and_settle_timeout = 10.0
