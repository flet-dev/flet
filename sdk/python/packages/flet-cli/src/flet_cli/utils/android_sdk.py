import os
import platform
import tempfile
from pathlib import Path
from typing import Optional

from flet_cli.utils import processes
from flet_cli.utils.distros import download_with_progress, extract_with_progress
from rich.progress import Progress

ANDROID_CMDLINE_TOOLS_DOWNLOAD_VERSION = "11076708"
ANDROID_CMDLINE_TOOLS_VERSION = "12.0"

MINIMAL_PACKAGES = [
    "cmdline-tools;latest",
    "platform-tools",
    "platforms;android-35",
    "build-tools;34.0.0",
]


class AndroidSDK:
    def __init__(
        self, java_home: str, log, progress: Optional[Progress] = None
    ) -> None:
        self.java_home = java_home
        self.log = log
        self.progress = progress

    @staticmethod
    def studio_android_home_dir() -> Path:
        return (
            Path.home() / "AppData" / "Local" / "Android" / "Sdk"
            if platform.system() == "Windows"
            else (
                Path.home() / "Library" / "Android" / "sdk"
                if platform.system() == "Darwin"
                else Path.home() / "Android" / "Sdk"
            )
        )

    @staticmethod
    def default_android_home_dir() -> Path:
        return Path.home() / "Android" / "sdk"

    @staticmethod
    def android_home_dir() -> Optional[Path]:
        # check ANDROID_HOME environment variable
        home_dir = os.getenv("ANDROID_HOME")
        if home_dir and Path(home_dir).exists():
            return Path(home_dir)

        # check ANDROID_SDK_ROOT environment variable
        home_dir = os.getenv("ANDROID_SDK_ROOT")
        if home_dir and Path(home_dir).exists():
            return Path(home_dir)

        # check for Android SDKs installed with Android Studio
        for hd in [
            AndroidSDK.studio_android_home_dir(),
            AndroidSDK.default_android_home_dir(),
        ]:
            if hd.exists():
                return hd

        return None

    def cmdline_tools_bin(self, home_dir: Path) -> Optional[Path]:
        for d in [
            home_dir / "cmdline-tools" / "latest" / "bin",
            home_dir / "cmdline-tools" / ANDROID_CMDLINE_TOOLS_VERSION / "bin",
        ]:
            if d.exists():
                return d
        return None

    def tool_exe(self, name: str, windows_ext: str):
        ext = windows_ext if platform.system() == "Windows" else ""
        return f"{name}{ext}"

    def sdkmanager_exe(self, home_dir):
        bin = self.cmdline_tools_bin(home_dir)
        assert bin
        return bin / self.tool_exe("sdkmanager", ".bat")

    def cmdline_tools_url(self):
        try:
            url_platform = {
                "Darwin": {
                    "arm64": "mac",
                    "x86_64": "mac",
                },
                "Linux": {
                    "x86_64": "linux",
                },
                "Windows": {
                    "AMD64": "win",
                },
            }[platform.system()][platform.machine()]
        except KeyError as e:
            raise Exception(
                f"Unsupported platform: {platform.system()}-{platform.machine()}"
            )

        return (
            f"https://dl.google.com/android/repository/"
            f"commandlinetools-{url_platform}-{ANDROID_CMDLINE_TOOLS_DOWNLOAD_VERSION}_latest.zip"
        )

    def install(self):
        home_dir = AndroidSDK.android_home_dir()
        install = True
        if not home_dir:
            home_dir = AndroidSDK.default_android_home_dir()
            self.log(f"Android SDK not found. Will be installed into {home_dir}")
        else:
            if self.cmdline_tools_bin(home_dir):
                self.log(f"Android SDK installation found at {home_dir}")
                install = False
            else:
                self.log(
                    f"Android SDK installation at {home_dir} does not contain cmdline tools. "
                    + "Android SDK will be re-installed."
                )

        if install:
            self._install_cmdlinetools(home_dir)

        installed_packages = 0
        for package in MINIMAL_PACKAGES:
            installed_packages += self._install_package(home_dir, package)

        if installed_packages > 0:
            self._accept_licenses(home_dir)

        return str(home_dir)

    def _install_cmdlinetools(self, android_home: Path):
        archive_path = os.path.join(tempfile.gettempdir(), f"commandlinetools.zip")
        url = self.cmdline_tools_url()
        self.log(f"Downloading Android cmdline tools from {url}...")
        download_with_progress(url, archive_path, progress=self.progress)

        unpack_dir = android_home / "cmdline-tools"
        unpack_dir.mkdir(parents=True, exist_ok=True)

        self.log(f"Extracting Android cmdline tools to {unpack_dir}...")
        extract_with_progress(archive_path, str(unpack_dir), progress=self.progress)

        # rename "cmdline-tools/cmdline-tools" to "cmdline-tools/{version}"
        cmdlinetools_dir = unpack_dir / "cmdline-tools"
        cmdlinetools_dir.rename(unpack_dir / ANDROID_CMDLINE_TOOLS_VERSION)

        os.remove(archive_path)

    def _install_package(self, home_dir: Path, package_name: str) -> int:
        if home_dir.joinpath(*package_name.split(";")).exists():
            self.log(f'Android SDK package "{package_name}" is already installed')
            return 0

        self.log(f'Installing Android SDK package "{package_name}"')

        p = self.run(
            (
                [
                    "sh",
                    "-c",
                    f'yes | "{self.sdkmanager_exe(home_dir)}" "{package_name}"',
                ]
                if platform.system() != "Windows"
                else [
                    "cmd.exe",
                    "/C",
                    "echo",
                    "y",
                    "|",
                    self.sdkmanager_exe(home_dir),
                    package_name,
                ]
            ),
            env={"ANDROID_HOME": str(home_dir)},
            capture_output=False,
        )
        if p.returncode != 0:
            self.log(p.stderr)
            raise Exception("Error installing Android SDK tools")
        return 1

    def _accept_licenses(self, home_dir: Path):
        self.log("Accepting Android SDK licenses")

        p = self.run(
            (
                ["sh", "-c", f'yes | "{self.sdkmanager_exe(home_dir)}" --licenses']
                if platform.system() != "Windows"
                else [
                    "cmd.exe",
                    "/C",
                    "echo",
                    "y",
                    "|",
                    self.sdkmanager_exe(home_dir),
                    "--licenses",
                ]
            ),
            env={"ANDROID_HOME": str(home_dir)},
            capture_output=False,
        )
        if p.returncode != 0:
            self.log(p.stderr)
            raise Exception("Error accepting Android SDK licenses")

    def get_installed_packages(self, home_dir: Path):
        self.log("Checking installed Android APIs and build tools")
        p = self.run(
            [self.sdkmanager_exe(home_dir), "--list_installed"],
            env={"ANDROID_HOME": str(home_dir)},
            capture_output=False,
        )
        if p.returncode != 0:
            self.log(p.stderr)
            raise Exception(
                "Error retrieving the list of installed Android SDK packages"
            )
        return p.stdout

    def run(self, args, env=None, cwd=None, capture_output=True):

        self.log(f"Run subprocess: {args}")

        cmd_env = {"JAVA_HOME": self.java_home}

        if env:
            cmd_env = {**cmd_env, **env}

        self.log(f"Process environment: {cmd_env}")

        return processes.run(
            args,
            cwd if cwd else os.getcwd(),
            env=cmd_env,
            capture_output=capture_output,
            log=self.log,
        )
