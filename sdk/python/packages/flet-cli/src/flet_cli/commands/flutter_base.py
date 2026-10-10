import argparse
import contextlib
import os
import platform
import re
import shutil
import sys
from collections.abc import Generator
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
from flet.utils import is_windows
from flet.utils.platform_utils import get_bool_env_var
from flet_cli.commands.base import BaseCommand
from flet_cli.utils.flutter import get_flutter_dir, install_flutter
from flet_cli.utils.log_format import (
    LOG_FORMATS,
    CliOutput,
    PlainLogConsole,
    detect_log_format,
    resolve_log_format,
    step_title,
)

# Detect the plain-output request BEFORE building the shared console: the
# `--log-format`/`--no-rich-output` argparse options are parsed per-command,
# too late to affect this module-level console, so check sys.argv for them
# here too (alongside the env vars). Without this, the flag only suppressed
# emojis while the color + Live spinner kept going.
log_format = detect_log_format(sys.argv, os.environ)
no_rich_output = log_format != "rich"

error_style = Style(color="red", bold=True)
warning_style = Style(color="yellow", bold=True)
# `plain`/`github` log plain lines: no time column, no wrapping.
console = (PlainLogConsole if no_rich_output else Console)(
    log_path=False,
    theme=Theme({"log.message": "green bold"}),
    # no_rich_output forces fully plain output (no color, no animation).
    # Otherwise auto-detect the terminal (force_terminal=None): a real TTY
    # gets the animated Live spinner, but piped output (CI, cloud build)
    # must NOT be fed one line per animation frame — forcing the terminal
    # on there floods non-TTY logs with thousands of spinner redraws.
    force_terminal=False if no_rich_output else None,
)
verbose1_style = Style(dim=True, bold=False)
verbose2_style = Style(color="bright_black", bold=False)

# Renders steps, warnings and errors in the selected log format.
output = CliOutput(
    console, log_format, warning_style=warning_style, error_style=error_style
)


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
        self._flutter_arch: Optional[tuple[str, Optional[str]]] = None
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

    @property
    def log_format(self) -> str:
        """
        The output format, one of `rich`, `plain` or `github`.

        Stored on the process-wide `output`, which also renders module-level
        warnings, so the format is the same everywhere.
        """

        return output.format

    @log_format.setter
    def log_format(self, value: str) -> None:
        output.format = value

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Register shared CLI arguments for Flutter-based commands.

        Args:
            parser: Argument parser configured by the command runner.
        """

        parser.add_argument(
            "--log-format",
            type=str.lower,
            choices=LOG_FORMATS,
            default=None,
            help="Output format: `rich` (default) shows a live spinner, `plain` "
            "prints plain text lines, `github` prints plain text plus GitHub "
            "Actions workflow commands - a collapsible group per build step and "
            "annotations for warnings and errors [env: FLET_CLI_LOG_FORMAT=]",
        )
        parser.add_argument(
            "--no-rich-output",
            action="store_true",
            default=False,
            help="Disable rich output and prefer plain text, same as "
            "`--log-format plain`. Useful on Windows builds "
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
        try:
            self.log_format = resolve_log_format(
                getattr(options, "log_format", None),
                getattr(options, "no_rich_output", False),
                os.environ,
            )
        except ValueError as e:
            console.print(str(e), style=error_style, markup=False)
            sys.exit(1)
        self.no_rich_output = self.log_format != "rich"
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

        sdk_found = bool(
            self.flutter_exe and self.dart_exe and self.flutter_version_valid()
        )
        if not sdk_found or not self.flutter_sdk_supported():
            if not self.assume_yes:
                if not sdk_found:
                    self.warn(
                        "Flutter SDK not found or invalid version installed.",
                        title="Flutter SDK",
                        prefix="",
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

    def flutter_sdk_supported(self) -> bool:
        """
        Check whether the Flutter SDK found can build for this command's target.

        Returns:
            `True` when the SDK can be used, otherwise `False`, in which case the
                required Flutter SDK is installed and used instead.
        """

        return True

    def flutter_arch(self) -> Optional[str]:
        """
        Return the CPU architecture of the Flutter SDK's Dart, such as `x64` or
        `arm64`. On Windows, Flutter builds desktop apps for this architecture.

        Returns:
            The architecture reported by `dart --version`, or `None` when it can't
                be determined.
        """

        if not self.dart_exe:
            return None
        if self._flutter_arch and self._flutter_arch[0] == self.dart_exe:
            return self._flutter_arch[1]

        arch = None
        result = self.run(
            [self.dart_exe, "--version"], cwd=os.getcwd(), capture_output=True
        )
        output = f"{result.stdout or ''}{result.stderr or ''}"
        # e.g. `Dart SDK version: 3.12.2 (stable) (...) on "windows_arm64"`
        match = re.search(r'on "[a-z]+_([a-z0-9]+)"', output)
        if match:
            arch = match.group(1)
        self._flutter_arch = (self.dart_exe, arch)
        return arch

    def install_flutter(self):
        """
        Install required Flutter SDK and update command environment.

        Also enables desktop support for the current desktop platform when
        applicable.
        """

        assert self.required_flutter_version
        with self.step(
            f"[bold blue]Installing Flutter {self.required_flutter_version}..."
        ):
            flutter_dir = install_flutter(
                str(self.required_flutter_version),
                self.log_stdout,
                progress=self.progress,
            )
            ext = ".bat" if platform.system() == "Windows" else ""
            self.flutter_exe = os.path.join(flutter_dir, "bin", f"flutter{ext}")
            self.dart_exe = os.path.join(flutter_dir, "bin", f"dart{ext}")
            path_env = os.environ.get("PATH", "")
            flutter_bin = os.path.join(flutter_dir, "bin")
            self.env["PATH"] = (
                os.pathsep.join([flutter_bin, path_env]) if path_env else flutter_bin
            )

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

        with self.step("[bold blue]Installing JDK..."):
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

        with self.step("[bold blue]Installing Android SDK..."):
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
            if self.no_rich_output:
                # Non-interactive (plain/github): the exit code and the last
                # step say it; a success banner is only noise in CI and
                # hosted-build logs.
                self.live.update("", refresh=True)
            else:
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
            if output.github:
                # Annotate the failure, titled after the step it happened in.
                output.error(msg, title=output.error_title)

            # windows has been reported to raise encoding errors
            # when running `flutter doctor`
            # so skip running `flutter doctor` if no_rich_output is True
            # and platform is Windows
            if not (
                (self.no_rich_output and self.current_platform == "Windows")
                or self.skip_flutter_doctor
            ):
                if output.github:
                    with output.group("Running Flutter doctor"):
                        self.run_flutter_doctor()
                else:
                    status = console.status(
                        "[bold blue]Running Flutter doctor...",
                        spinner="bouncingBall",
                    )
                    self.live.update(
                        Group(Panel(msg, style=error_style), status), refresh=True
                    )
                    self.run_flutter_doctor()
            if output.github:
                # The `::error::` line above already shows in the log (and
                # as an annotation); a box-drawn panel would only repeat it.
                self.live.update("", refresh=True)
            elif self.no_rich_output:
                # One plain line, not a box: some failures (bad arguments,
                # a missing app) have no other output explaining them.
                self.live.update("", refresh=True)
                output.console.print(msg, style=error_style, soft_wrap=True)
            else:
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

    @contextlib.contextmanager
    def step(self, status: str) -> Generator[None, None, None]:
        """
        Run a block as a named build step.

        `rich`: shows `status` on the live spinner. `plain`: logs `status`.
        `github`: wraps the block in `::group::<title>` ... `::endgroup::`,
        the title being `status` without markup and trailing ellipsis; the
        group is closed even when the block raises or exits via `cleanup()`.
        The block logs its own completion message, if any.

        Args:
            status: Status text, such as `[bold blue]Generating app icons...`.
        """

        if not output.github:
            self.update_status(status)
            yield
            return

        with output.group(step_title(status)):
            yield

    def warn(
        self,
        message: Any,
        title: Optional[str] = None,
        file: Optional[str] = None,
        line: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Report a warning: a `Warning: <message>` log line, or a `::warning::`
        annotation in the `github` log format.

        Args:
            message: The warning text.
            title: Annotation title (`github` only).
            file: File the annotation points to (`github` only).
            line: Line in `file` (`github` only).
            **kwargs: Passed to `CliOutput.warn()`.
        """

        output.warn(message, title=title, file=file, line=line, **kwargs)

    def error(
        self,
        message: Any,
        title: Optional[str] = None,
        file: Optional[str] = None,
        line: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Report an error: a log line in the error style, or an `::error::`
        annotation in the `github` log format.

        Args:
            message: The error text.
            title: Annotation title (`github` only).
            file: File the annotation points to (`github` only).
            line: Line in `file` (`github` only).
            **kwargs: Passed to `CliOutput.error()`.
        """

        output.error(message, title=title, file=file, line=line, **kwargs)

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
