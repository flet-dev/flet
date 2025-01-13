import os
import platform
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from flet_cli.utils.distros import download_with_progress, extract_with_progress
from rich.console import Console
from rich.progress import Progress

ANDROID_CMDLINE_TOOLS_VERSION = "11076708"
ANDROID_API_VERSION = "35"
BUILD_TOOLS_VERSION = "33.0.1"


class AndroidSDK:
    def __init__(
        self, java_home: str, log, progress: Optional[Progress] = None
    ) -> None:
        self.java_home = java_home
        self.log = log
        self.progress = progress

    def default_android_home_dir(self):
        return (
            Path.home() / "AppData" / "Local" / "Android" / "Sdk"
            if platform.system() == "Windows"
            else (
                Path.home() / "Library" / "Android" / "sdk"
                if platform.system() == "Darwin"
                else Path.home() / "Android" / "sdk"
            )
        )

    def android_home_dir(self) -> Path | None:
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
            Path.home() / "Android" / "Sdk",
            self.default_android_home_dir(),
        ]:
            if hd.exists():
                return hd

        return None

    def sdkmanager_dir(self, home_dir: Path) -> Path | None:
        for d in [
            home_dir / "tools" / "bin",
            home_dir / "cmdline-tools" / "latest" / "bin",
            home_dir / "cmdline-tools" / "bin",
        ]:
            if d.exists():
                return d
        return None

    def tool_exe(self, name: str, windows_ext: str):
        ext = windows_ext if platform.system() == "Windows" else ""
        return f"{name}{ext}"

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
            f"commandlinetools-{url_platform}-{ANDROID_CMDLINE_TOOLS_VERSION}_latest.zip"
        )

    def install(self):
        self.log("Checking for existing Android SDK installation")
        home_dir = self.android_home_dir()
        install = True
        if not home_dir:
            home_dir = self.default_android_home_dir()
            self.log(f"Android SDK not found. Will be installed into {home_dir}")
        else:
            if self.sdkmanager_dir(home_dir):
                self.log(f"Android SDK installation found at {home_dir}")
                install = False
            else:
                self.log(
                    f"Android SDK installation at {home_dir} does not contain sdkmanager executable. "
                    + "Android SDK will be re-installed."
                )

        if install:
            self._install_cmdlinetools(home_dir)

        return home_dir

    def _install_cmdlinetools(self, android_home: Path):
        archive_path = os.path.join(tempfile.gettempdir(), f"commandlinetools.zip")
        url = self.cmdline_tools_url()
        self.log(f"Downloading Android cmdline tools from {url}...")
        download_with_progress(url, archive_path, progress=self.progress)

        unpack_dir = android_home / "cmdline-tools"
        unpack_dir.mkdir(parents=True, exist_ok=True)

        self.log(f"Extracting Android cmdline tools to {unpack_dir}...")
        extract_with_progress(archive_path, str(unpack_dir), progress=self.progress)

        # rename "cmdline-tools/cmdline-tools" to "cmdline-tools/latest"
        cmdlinetools_dir = unpack_dir / "cmdline-tools"
        cmdlinetools_dir.rename(unpack_dir / "latest")

        os.remove(archive_path)

    def accept_sdkmanager_licenses(self):
        """
        Automatically accept all licenses for the Android SDK Manager.
        """
        try:
            # Define the command for sdkmanager --licenses
            command = [
                "C:\\Android\\sdk\\cmdline-tools\\latest\\bin\\sdkmanager.bat",
                "--licenses",
            ]

            # Run the command, sending 'y' (yes) to approve all licenses
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                # stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env={"JAVA_HOME": "C:\\Users\\feodo\\java\\17.0.13+11"},
            )
            # Simulate accepting licenses by sending 'y' repeatedly
            stdout, stderr = process.communicate(input="y\n" * 100)

            # Check the process return code
            if process.returncode == 0:
                print("All licenses accepted successfully.")
            else:
                print(f"Failed to accept licenses. Error: {stderr}")
        except FileNotFoundError:
            print(
                "sdkmanager not found. Ensure the Android SDK is installed and in your PATH."
            )
        except Exception as e:
            print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    console = Console()
    jdk_path = AndroidSDK(
        os.environ["JAVA_HOME"], lambda m: console.log(m)
    ).accept_sdkmanager_licenses()
