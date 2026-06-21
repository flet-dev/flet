import argparse
import os
import platform
import re
import shutil
import sys
from typing import Any, Optional

from packaging import version
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import Progress
from rich.prompt import Confirm
from rich.style import Style
from rich.theme import Theme

import flet.version
import flet_cli.utils.processes as processes
from flet.utils import cleanup_path, is_windows
from flet.utils.platform_utils import get_bool_env_var
from flet_cli.commands.base import BaseCommand
from flet_cli.utils.flutter import get_flutter_dir, install_flutter

no_rich_output = get_bool_env_var("FLET_CLI_NO_RICH_OUTPUT")

error_style = Style(color="red", bold=True)
warning_style = Style(color="yellow", bold=True)
console = Console(
    log_path=False,
    theme=Theme({"log.message": "green bold"}),
    force_terminal=not no_rich_output,
)
verbose1_style = Style(dim=True, bold=False)
verbose2_style = Style(color="bright_black", bold=False)


class BaseFlutterCommand(BaseCommand):
    """
    A base Flutter CLI command.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)

        self.env = {}
        self.options = None
        self.emojis = {}
        self.dart_exe = None
        self.flutter_exe = None
        self.required_flutter_version: Optional[version.Version] = None
        self.verbose = False
        self.require_android_sdk = False
        self.skip_flutter_doctor = get_bool_env_var("FLET_CLI_SKIP_FLUTTER_DOCTOR")
        self.no_rich_output = no_rich_output
        self.current_platform = platform.system()
        self.progress = Progress(transient=True)
        self.platform_labels = {
            "windows": "Windows",
            "macos": "macOS",
            "linux": "Linux",
            "web": "Web",
            "ios": "iOS",
            "android": "Android",
            None: "iOS/Android",
        }
        self.assume_yes = False
        self._android_install_confirmed = False

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Register shared CLI arguments for Flutter-based commands.

        Args:
            parser: Argument parser configured by the command runner.
        """

        parser.add_argument(
            "--no-rich-output",
            action="store_true",
            default=False,
            help="Disable rich output and prefer plain text. Useful on Windows builds "
            "[env: FLET_CLI_NO_RICH_OUTPUT=]",
        )
        parser.add_argument(
            "--yes",
            dest="assume_yes",
            action="store_true",
            default=False,
            help="Answer yes to all prompts (install dependencies "
            "without confirmation).",
        )
        parser.add_argument(
            "--skip-flutter-doctor",
            action="store_true",
            default=False,
            help="Skip running Flutter doctor upon failed builds "
            "[env: FLET_CLI_SKIP_FLUTTER_DOCTOR=]",
        )

    def handle(self, options: argparse.Namespace) -> None:
        """
        Store common option values used by derived commands.

        Args:
            options: Parsed command-line options.
        """

        self.options = options
        self.no_rich_output = self.no_rich_output or self.options.no_rich_output
        self.verbose = self.options.verbose
        self.assume_yes = getattr(self.options, "assume_yes", False)

    def initialize_command(self):
        """
        Validate prerequisites and prepare Flutter/Android toolchain.

        This method resolves required Flutter version, locates or installs SDK
        binaries, and optionally provisions JDK/Android SDK when the command
        requires mobile tooling.
        """

        assert self.options
        self.required_flutter_version = version.Version(flet.version.flutter_version)
        if self.required_flutter_version == version.Version("0"):
            self.cleanup(
                1,
                "Unable to determine the required Flutter SDK version. "
                "If in a source checkout, ensure a valid `.fvmrc` file exists.",
            )

        self.emojis = {
            "checkmark": "[green]OK[/]" if self.no_rich_output else "✅",
            "loading": "" if self.no_rich_output else "⏳",
            "success": "" if self.no_rich_output else "🥳",
            "directory": "" if self.no_rich_output else "📁",
        }

        self.skip_flutter_doctor = (
            self.skip_flutter_doctor or self.options.skip_flutter_doctor
        )

        # get `flutter` and `dart` executables from PATH
        self.flutter_exe = self.find_flutter_batch("flutter")
        self.dart_exe = self.find_flutter_batch("dart")

        if (
            not self.flutter_exe
            or not self.dart_exe
            or not self.flutter_version_valid()
        ):
            if not self.assume_yes:
                console.log(
                    "Flutter SDK not found or invalid version installed.",
                    style=warning_style,
                )
                prompt = (
                    f"Flutter SDK {self.required_flutter_version} is required. "
                    f"It will be installed now. Proceed? [y/n] "
                )

                if not self._prompt_input(prompt):
                    self.skip_flutter_doctor = True
                    self.cleanup(
                        1,
                        "Flutter SDK installation is required. "
                        "Re-run with --yes to install automatically.",
                    )
            self.install_flutter()

        if self.verbose > 0:
            console.log("Flutter executable:", self.flutter_exe, style=verbose2_style)
            console.log("Dart executable:", self.dart_exe, style=verbose2_style)

        if self.require_android_sdk:
            if not self._confirm_android_sdk_installation():
                self.skip_flutter_doctor = True
                self.cleanup(
                    1,
                    "Android SDK installation is required. "
                    "Re-run with --yes to install automatically.",
                )
            self.install_jdk()
            self.install_android_sdk()

    def flutter_version_valid(self):
        """
        Check whether the discovered Flutter SDK matches required major/minor version.

        Returns:
            `True` when installed Flutter version is compatible, otherwise `False`.
        """

        assert self.required_flutter_version
        version_results = self.run(
            [
                self.flutter_exe,
                "--version",
                "--no-version-check",
                "--suppress-analytics",
            ],
            cwd=os.getcwd(),
            capture_output=True,
        )
        if version_results.returncode == 0 and version_results.stdout:
            match = re.search(r"Flutter (\d+\.\d+\.\d+)", version_results.stdout)
            if match:
                flutter_version = version.parse(match.group(1))

                # validate installed Flutter version
                return (
                    flutter_version.major == self.required_flutter_version.major
                    and flutter_version.minor == self.required_flutter_version.minor
                )
        else:
            console.log(1, "Failed to validate Flutter version.")
        return False

    def install_flutter(self):
        """
        Install required Flutter SDK and update command environment.

        Also enables desktop support for the current desktop platform when
        applicable.
        """

        assert self.required_flutter_version
        self.update_status(
            f"[bold blue]Installing Flutter {self.required_flutter_version}..."
        )

        flutter_dir = install_flutter(
            str(self.required_flutter_version), self.log_stdout, progress=self.progress
        )
        ext = ".bat" if platform.system() == "Windows" else ""
        self.flutter_exe = os.path.join(flutter_dir, "bin", f"flutter{ext}")
        self.dart_exe = os.path.join(flutter_dir, "bin", f"dart{ext}")
        path_env = cleanup_path(
            cleanup_path(os.environ.get("PATH", ""), "flutter"), "dart"
        )
        self.env["PATH"] = os.pathsep.join([os.path.join(flutter_dir, "bin"), path_env])

        # desktop mode
        desktop_platform = platform.system().lower()
        if desktop_platform == "darwin":
            desktop_platform = "macos"
        if desktop_platform in ["macos", "windows", "linux"]:
            if self.verbose > 0:
                console.log(
                    "Ensure Flutter has desktop support enabled",
                    style=verbose1_style,
                )
            config_result = self.run(
                [
                    self.flutter_exe,
                    "config",
                    "--no-version-check",
                    "--suppress-analytics",
                    f"--enable-{desktop_platform}-desktop",
                ],
                cwd=os.getcwd(),
                capture_output=self.verbose < 1,
            )
            if config_result.returncode != 0:
                if isinstance(config_result.stdout, str):
                    console.log(config_result.stdout, style=verbose1_style)
                if isinstance(config_result.stderr, str):
                    console.log(config_result.stderr, style=error_style)
                self.cleanup(config_result.returncode)

        if self.verbose > 0:
            console.log(
                f"Flutter {self.required_flutter_version} "
                f"installed {self.emojis['checkmark']}"
            )

    def install_jdk(self):
        """
        Install or resolve JDK and configure Flutter to use it.
        """

        from flet_cli.utils.jdk import install_jdk

        self.update_status("[bold blue]Installing JDK...")
        jdk_dir = install_jdk(self.log_stdout, progress=self.progress)
        self.env["JAVA_HOME"] = jdk_dir

        # config flutter's JDK dir
        if self.verbose > 0:
            console.log(
                "Configuring Flutter's path to JDK",
                style=verbose1_style,
            )
        config_result = self.run(
            [
                self.flutter_exe,
                "config",
                "--no-version-check",
                "--suppress-analytics",
                f"--jdk-dir={jdk_dir}",
            ],
            cwd=os.getcwd(),
            capture_output=self.verbose < 1,
        )
        if config_result.returncode != 0:
            if isinstance(config_result.stdout, str):
                console.log(config_result.stdout, style=verbose1_style)
            if isinstance(config_result.stderr, str):
                console.log(config_result.stderr, style=error_style)
            self.cleanup(config_result.returncode)

        if self.verbose > 0:
            console.log(f"JDK installed {self.emojis['checkmark']}")

    def install_android_sdk(self):
        """
        Install Android SDK command-line tools and required baseline packages.
        """

        from flet_cli.utils.android_sdk import AndroidSDK

        self.update_status("[bold blue]Installing Android SDK...")
        self.env["ANDROID_HOME"] = AndroidSDK(
            self.env["JAVA_HOME"], self.log_stdout, progress=self.progress
        ).install()

        if self.verbose > 0:
            console.log(f"Android SDK installed {self.emojis['checkmark']}")

    def _confirm_android_sdk_installation(self) -> bool:
        """
        Confirm Android SDK installation when it is missing or incomplete.

        Returns:
            `True` when installation is confirmed or not needed, otherwise `False`.
        """

        from flet_cli.utils.android_sdk import AndroidSDK

        if AndroidSDK.has_minimal_packages_installed():
            self._android_install_confirmed = True
            return True
        if self._android_install_confirmed:
            return True
        if self.assume_yes:
            self._android_install_confirmed = True
            return True

        prompt = (
            "\nAndroid SDK is required. If it's missing or incomplete, "
            "it will be installed now. Proceed? [y/n] "
        )

        if self._prompt_input(prompt):
            self._android_install_confirmed = True
            return True
        return False

    def _prompt_input(self, prompt: str) -> bool:
        """
        Ask an interactive yes/no prompt while temporarily pausing live rendering.

        Args:
            prompt: Prompt text shown to the user.

        Returns:
            `True` when user confirms, otherwise `False`.
        """

        self.live.stop()
        try:
            return Confirm.ask(prompt, default=True)
        finally:
            self.live.start()

    def find_flutter_batch(self, exe_filename: str):
        """Locate the Flutter/Dart executable, preferring the managed SDK install."""
        assert self.required_flutter_version

        install_dir = get_flutter_dir(str(self.required_flutter_version))
        ext = ".bat" if is_windows() else ""
        batch_path = os.path.join(install_dir, "bin", f"{exe_filename}{ext}")

        if os.path.exists(batch_path):
            return batch_path

        # Fall back to system-installed executable
        batch_path = shutil.which(exe_filename)
        if not batch_path:
            return None

        if is_windows():
            # convert shim paths
            if batch_path.endswith(".file"):
                return batch_path.replace(".file", ".bat")

            # normalize .exe casing
            root, ext = os.path.splitext(batch_path)
            if ext.lower() == ".exe":
                return f"{root}.exe"

        return batch_path

    def run(self, args, cwd, env: Optional[dict] = None, capture_output=True):
        """
        Run a subprocess using merged command environment.

        Args:
            args: Command and arguments to execute.
            cwd: Working directory for the process.
            env: Additional environment variables merged on top of `self.env`.
            capture_output: Whether to capture output instead of streaming.

        Returns:
            Process result object returned by `flet_cli.utils.processes.run`.
        """

        if self.verbose > 0:
            console.log(f"Run subprocess: {args}", style=verbose1_style)

        return processes.run(
            args,
            cwd,
            env={**self.env, **env} if env else self.env,
            capture_output=capture_output,
            log=self.log_stdout,
        )

    def cleanup(self, exit_code: int, message: Any = None, no_border: bool = False):
        """
        Finalize command output, optionally run Flutter doctor, and exit process.

        Args:
            exit_code: Exit status code.
            message: Optional success/error message content.
            no_border: Whether to render success message without a panel border.
        """

        if exit_code == 0:
            self.live.update(
                (message if no_border else Panel(message)) if message else "",
                refresh=True,
            )
        else:
            msg = (
                message
                if message is not None
                else "Error building Flet app - see the log of failed command above."
            )

            # windows has been reported to raise encoding errors
            # when running `flutter doctor`
            # so skip running `flutter doctor` if no_rich_output is True
            # and platform is Windows
            if not (
                (self.no_rich_output and self.current_platform == "Windows")
                or self.skip_flutter_doctor
            ):
                status = console.status(
                    "[bold blue]Running Flutter doctor...",
                    spinner="bouncingBall",
                )
                self.live.update(
                    Group(Panel(msg, style=error_style), status), refresh=True
                )
                self.run_flutter_doctor()
            self.live.update(Panel(msg, style=error_style), refresh=True)

        sys.exit(exit_code)

    def run_flutter_doctor(self):
        """
        Execute `flutter doctor` and print diagnostic output.
        """

        flutter_doctor = self.run(
            [self.flutter_exe, "doctor", "--no-version-check", "--suppress-analytics"],
            cwd=os.getcwd(),
            capture_output=True,
        )
        if flutter_doctor.stdout:
            console.log(flutter_doctor.stdout, style=verbose1_style)
        if flutter_doctor.stderr:
            console.log(flutter_doctor.stderr, style=error_style)

    def update_status(self, status):
        """
        Update current live status message or log it in plain-output mode.

        Args:
            status: Status text to display.
        """

        if self.no_rich_output:
            console.log(status)
        else:
            self.status.update(status)

    def log_stdout(self, message):
        """
        Log subprocess output lines when verbose mode is enabled.

        Args:
            message: Output text chunk.
        """

        if self.verbose > 0:
            console.log(
                message,
                end="",
                style=verbose2_style,
                markup=False,
            )
