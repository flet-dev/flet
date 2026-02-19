import os
import platform
import tempfile
from pathlib import Path
from typing import Optional

from rich.progress import Progress

from flet_cli.utils import processes
from flet_cli.utils.distros import download_with_progress, extract_with_progress

ANDROID_CMDLINE_TOOLS_DOWNLOAD_VERSION = "11076708"
ANDROID_CMDLINE_TOOLS_VERSION = "12.0"

MINIMAL_PACKAGES = [
    "cmdline-tools;latest",
    "platform-tools",
    "platforms;android-35",
    "build-tools;34.0.0",
]


class AndroidSDK:
    """
    Helper for discovering, installing, and invoking Android SDK tooling.

    The class manages command-line tools installation, required package setup,
    license acceptance, and subprocess execution with the required environment.
    """

    def __init__(
        self, java_home: str, log, progress: Optional[Progress] = None
    ) -> None:
        self.java_home = java_home
        self.log = log
        self.progress = progress

    @staticmethod
    def studio_android_home_dir() -> Path:
        """
        Return the default Android Studio SDK directory for the current platform.

        Returns:
            Platform-specific SDK path typically used by Android Studio.
        """

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
        """
        Return the fallback SDK installation directory used by this CLI.

        Returns:
            Default SDK path under the user's home directory.
        """

        return Path.home() / "Android" / "sdk"

    @staticmethod
    def android_home_dir() -> Optional[Path]:
        """
        Locate an existing Android SDK home directory.

        Detection order:
        - `ANDROID_HOME` when it exists;
        - `ANDROID_SDK_ROOT` when it exists;
        - common SDK directories used by Android Studio and the CLI.

        Returns:
            Existing SDK directory path, or `None` if no installation is found.
        """

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
        """
        Return the `cmdline-tools` binary directory in an SDK installation.

        Args:
            home_dir: Android SDK home directory.

        Returns:
            Path to the tools `bin` directory, or `None` if not found.
        """

        for d in [
            home_dir / "cmdline-tools" / "latest" / "bin",
            home_dir / "cmdline-tools" / ANDROID_CMDLINE_TOOLS_VERSION / "bin",
        ]:
            if d.exists():
                return d
        return None

    def tool_exe(self, name: str, windows_ext: str):
        """
        Build a platform-specific executable name.

        Args:
            name: Base executable name.
            windows_ext: Extension to append on Windows (for example `.bat`).

        Returns:
            Executable name for the current platform.
        """

        ext = windows_ext if platform.system() == "Windows" else ""
        return f"{name}{ext}"

    def sdkmanager_exe(self, home_dir):
        """
        Return the absolute path to `sdkmanager`.

        Args:
            home_dir: Android SDK home directory.

        Returns:
            Path to the `sdkmanager` executable.
        """

        bin = self.cmdline_tools_bin(home_dir)
        assert bin
        return bin / self.tool_exe("sdkmanager", ".bat")

    def avdmanager_exe(self, home_dir):
        """
        Return the absolute path to `avdmanager`.

        Args:
            home_dir: Android SDK home directory.

        Returns:
            Path to the `avdmanager` executable.
        """

        bin = self.cmdline_tools_bin(home_dir)
        assert bin
        return bin / self.tool_exe("avdmanager", ".bat")

    @staticmethod
    def has_minimal_packages_installed() -> bool:
        """
        Check whether a usable SDK and required baseline packages are present.

        Returns:
            `True` when SDK command-line tools and all packages in
                `MINIMAL_PACKAGES` are installed; otherwise `False`.
        """

        home_dir = AndroidSDK.android_home_dir()
        if not home_dir:
            return False

        sdk = AndroidSDK("", lambda *_: None)
        if not sdk.cmdline_tools_bin(home_dir):
            return False

        for package in MINIMAL_PACKAGES:
            if not home_dir.joinpath(*package.split(";")).exists():
                return False

        return True

    def delete_avd(self, home_dir: Path, avd_name: str) -> None:
        """
        Deletes an Android Virtual Device using avdmanager.
        """
        self.log(f'Deleting Android emulator "{avd_name}"')
        result = self.run(
            [
                self.avdmanager_exe(home_dir),
                "delete",
                "avd",
                "-n",
                avd_name,
            ],
            env={"ANDROID_HOME": str(home_dir)},
            capture_output=True,
        )
        if result.returncode != 0:
            self.log(result.stderr or result.stdout)
            raise RuntimeError(f'Failed to delete Android emulator "{avd_name}"')

    def cmdline_tools_url(self):
        """
        Build the command-line tools archive URL for the current platform.

        Returns:
            Download URL for Android command-line tools.

        Raises:
            RuntimeError: If the current platform or architecture is unsupported.
        """

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
        except KeyError:
            raise RuntimeError(
                f"Unsupported platform: {platform.system()}-{platform.machine()}"
            ) from None

        return (
            f"https://dl.google.com/android/repository/"
            f"commandlinetools-{url_platform}-{ANDROID_CMDLINE_TOOLS_DOWNLOAD_VERSION}_latest.zip"
        )

    def install(self):
        """
        Ensure Android command-line tools and required SDK packages are installed.

        The method locates an SDK home (or chooses a default path), installs
        command-line tools if needed, installs all entries in `MINIMAL_PACKAGES`,
        and accepts licenses when new packages are installed.

        Returns:
            Android SDK home directory as a string.
        """

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
                    f"Android SDK installation at {home_dir} does not contain "
                    + "cmdline tools. Android SDK will be re-installed."
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
        """
        Download and extract Android command-line tools into `android_home`.

        Args:
            android_home: SDK home directory where `cmdline-tools` is created.
        """

        archive_path = os.path.join(tempfile.gettempdir(), "commandlinetools.zip")
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
        """
        Install a single SDK package when it is not already present.

        Args:
            home_dir: Android SDK home directory.
            package_name: SDK package identifier accepted by `sdkmanager`.

        Returns:
            `1` when installation was performed, `0` when already installed.

        Raises:
            RuntimeError: If package installation fails.
        """

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
            raise RuntimeError("Error installing Android SDK tools")
        return 1

    def _accept_licenses(self, home_dir: Path):
        """
        Accept Android SDK licenses non-interactively.

        Args:
            home_dir: Android SDK home directory.

        Raises:
            RuntimeError: If license acceptance fails.
        """

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
            raise RuntimeError("Error accepting Android SDK licenses")

    def get_installed_packages(self, home_dir: Path):
        """
        Query installed SDK packages using `sdkmanager`.

        Args:
            home_dir: Android SDK home directory.

        Returns:
            Command output listing installed packages.

        Raises:
            RuntimeError: If querying installed packages fails.
        """

        self.log("Checking installed Android APIs and build tools")
        p = self.run(
            [self.sdkmanager_exe(home_dir), "--list_installed"],
            env={"ANDROID_HOME": str(home_dir)},
            capture_output=False,
        )
        if p.returncode != 0:
            self.log(p.stderr)
            raise RuntimeError(
                "Error retrieving the list of installed Android SDK packages"
            )
        return p.stdout

    def run(self, args, env=None, cwd=None, capture_output=True):
        """
        Run a subprocess configured for Android SDK tooling.

        `JAVA_HOME` is always injected from this instance, then merged with
        any additional environment entries.

        Args:
            args: Command arguments passed to the subprocess helper.
            env: Optional additional environment variables.
            cwd: Optional working directory. Defaults to current directory.
            capture_output: Forwarded to subprocess helper.

        Returns:
            Subprocess result object returned by `flet_cli.utils.processes.run`.
        """

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
