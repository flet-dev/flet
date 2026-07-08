import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional

from rich.console import Group
from rich.live import Live

from flet_cli.commands.build_base import BaseBuildCommand, console

# Maps the user-facing test platform to the build target_platform used to
# provision the Flutter test host, plus the default device id for desktop.
TEST_PLATFORMS = {
    "windows": {"target_platform": "windows", "device_id": "windows"},
    "macos": {"target_platform": "macos", "device_id": "macos"},
    "linux": {"target_platform": "linux", "device_id": "linux"},
    "ios": {"target_platform": "ipa", "device_id": None},
    "android": {"target_platform": "apk", "device_id": None},
}


def _default_desktop_platform() -> str:
    name = platform.system().lower()
    return "macos" if name == "darwin" else name  # "windows" / "linux"


def _provision_steps(cmd: "BaseBuildCommand") -> Path:
    """
    Drive the shared `flet build` provisioning pipeline (in `test_mode`) to
    materialize a Flutter test host with the app's Python embedded as
    `app/app.zip` and the `integration_test/` driver. Release build, icons,
    splash and output-copy steps are intentionally skipped — `flutter test`
    compiles its own debug binary. Returns the provisioned Flutter project dir.
    """
    cmd.test_mode = True
    cmd.initialize_command()
    cmd.validate_target_platform()
    cmd.validate_entry_point()
    cmd.setup_template_data()
    cmd.create_flutter_project()
    cmd.package_python_app()
    cmd.register_flutter_extensions()
    if cmd.create_flutter_project(second_pass=True):
        cmd.update_flutter_dependencies()
    return cmd.flutter_dir


# Env vars set by `flet test` (and `provision_test_host`) for the pytest
# subprocess. `flutter test integration_test` (spawned by FletTestApp) runs the
# platform's native build, whose serious_python build phase bundles the staged
# app + site-packages — without these vars the embedded Python can't import its
# dependencies (e.g. ModuleNotFoundError: certifi) and, on Android, the
# `packageApp` Gradle task no-ops so a stale `app.zip` (old-Python `main.pyc`)
# survives in the APK (ImportError: bad magic number). `flet build`/`flet debug`
# set the SAME serious_python vars for their flutter build via
# `_serious_python_build_env` (build_base.py `_run_flutter_command`); we reuse it
# here so the two paths can't drift.
_TEST_ENV_KEYS = (
    "PATH",
    "FLET_TEST_DISABLE_FVM",
    "FLET_TEST_FLUTTER_EXE",
    "SERIOUS_PYTHON_VERSION",
    "SERIOUS_PYTHON_SITE_PACKAGES",
    "SERIOUS_PYTHON_APP",
    "SERIOUS_PYTHON_ANDROID_EXTRACT_PACKAGES",
    "SP_NATIVE_SET",
    "SERIOUS_PYTHON_FLUTTER_PACKAGES",
)


def _flutter_path_env(cmd: "BaseBuildCommand") -> dict:
    """
    Build an environment for the pytest subprocess so the on-device test run
    (`flutter test integration_test`, spawned by FletTestApp) finds the same
    Flutter SDK we provisioned with (without `fvm`) and so the native build
    bundles the app's site-packages.
    """
    env = {**os.environ, **cmd.env}
    if cmd.flutter_exe:
        flutter_bin = str(Path(cmd.flutter_exe).parent)
        env["PATH"] = os.pathsep.join([flutter_bin, env.get("PATH", "")])
        # Hand the resolved Flutter executable (e.g. `flutter.bat` on Windows) to
        # FletTestApp: it spawns `flutter test` with create_subprocess_exec, which
        # on Windows can't resolve a bare "flutter" (no PATHEXT lookup).
        env["FLET_TEST_FLUTTER_EXE"] = str(cmd.flutter_exe)
    env["FLET_TEST_DISABLE_FVM"] = "1"
    # Same serious_python env `flet build` hands its native build, so the app
    # `flutter test` builds is bundled identically (incl. SERIOUS_PYTHON_APP →
    # a fresh app.zip with a matching-Python main.pyc).
    env.update(cmd._serious_python_build_env())
    if getattr(cmd, "flutter_packages_temp_dir", None) is not None:
        env["SERIOUS_PYTHON_FLUTTER_PACKAGES"] = str(cmd.flutter_packages_temp_dir)
    return env


class Command(BaseBuildCommand):
    """
    Run Flet integration tests for an app.

    Provisions a Flutter test host from the app (the same pipeline as
    `flet build`, in test mode) so the app runs on-device with embedded Python,
    then runs pytest. Tests in the `tests/` directory drive the app through the
    `flet_app` fixture (find controls by key, tap, take/assert screenshots).

    Detailed usage guide: https://flet.dev/docs/getting-started/integration-testing
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)
        self.test_platform_name: Optional[str] = None
        self.device_id: Optional[str] = None
        self.tests_dir = "tests"
        self.update_goldens = False
        self.pytest_args: list[str] = []
        self.flutter_test_host: Optional[str] = None

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        # `platform` is a positional, like `flet debug`. Register it first, then
        # the inherited build args (which add the `python_app_path` positional),
        # then our trailing `pytest_args` REMAINDER positional.
        parser.add_argument(
            "platform",
            type=str.lower,
            nargs="?",
            choices=["macos", "linux", "windows", "ios", "android"],
            help="The target platform to run the tests on "
            "(defaults to the current desktop platform).",
        )
        super().add_arguments(parser)
        parser.add_argument(
            "--device-id",
            "-d",
            dest="device_id",
            help="Device ID to run the tests on (for iOS and Android).",
        )
        parser.add_argument(
            "--tests-dir",
            dest="tests_dir",
            default="tests",
            help="Directory with the integration tests, relative to the app "
            "directory (default: tests).",
        )
        parser.add_argument(
            "--update-goldens",
            "-u",
            dest="update_goldens",
            action="store_true",
            default=False,
            help="Capture/update golden screenshots instead of comparing.",
        )
        parser.add_argument(
            "--flutter-test-host",
            dest="flutter_test_host",
            default=None,
            help="Use an already-provisioned Flutter test host directory "
            "instead of building one (e.g. a CI-cached host).",
        )
        parser.add_argument(
            "-k",
            dest="pytest_keyword",
            default=None,
            help="Only run tests matching the given pytest keyword expression "
            "(passed through to pytest -k).",
        )

    def handle(self, options: argparse.Namespace) -> None:
        super().handle(options)
        # `flet test` never produces a packaged artifact; build output dir is
        # irrelevant (mirrors `flet debug`).
        self.options.output_dir = None

        self.test_platform_name = options.platform or _default_desktop_platform()
        self.target_platform = TEST_PLATFORMS[self.test_platform_name][
            "target_platform"
        ]
        self.device_id = (
            options.device_id or TEST_PLATFORMS[self.test_platform_name]["device_id"]
        )
        self.tests_dir = options.tests_dir
        self.update_goldens = options.update_goldens
        self.flutter_test_host = options.flutter_test_host

        self.pytest_args = []
        if options.pytest_keyword:
            self.pytest_args += ["-k", options.pytest_keyword]

        if self.test_platform_name in ("android", "ios") and not self.device_id:
            console.print(
                f"[red]A device id is required for {self.test_platform_name}. "
                "Pass it with --device-id (use `flet devices` to list "
                "connected devices).[/red]"
            )
            sys.exit(1)

        if self.flutter_test_host:
            flutter_dir = Path(self.flutter_test_host).resolve()
            # Still need python_app_path/env for pytest; run a light init.
            self.test_mode = True
            self.status = console.status(
                "[bold blue]Preparing tests...", spinner="bouncingBall"
            )
            with Live(Group(self.status, self.progress), console=console) as self.live:
                self.initialize_command()
                self.validate_entry_point()
        else:
            self.status = console.status(
                f"[bold blue]Provisioning {self.target_platform} test host...",
                spinner="bouncingBall",
            )
            with Live(Group(self.status, self.progress), console=console) as self.live:
                flutter_dir = _provision_steps(self)
                self.update_status("[bold blue]Test host ready. Starting tests...")

        exit_code = self._run_pytest(flutter_dir)
        sys.exit(exit_code)

    def _run_pytest(self, flutter_dir: Path) -> int:
        assert self.python_app_path
        env = _flutter_path_env(self)
        env["FLET_TEST_DEVICE_MODE"] = "1"
        env["FLET_TEST_FLUTTER_APP_DIR"] = str(flutter_dir)
        env["FLET_TEST_PLATFORM"] = self.test_platform_name or ""
        if self.device_id:
            env["FLET_TEST_DEVICE"] = self.device_id
        if self.update_goldens:
            env["FLET_TEST_GOLDEN"] = "1"

        pytest_args = list(self.pytest_args)
        if self.verbose > 0:
            # Stream the Flutter test process output (compilation/launch
            # progress) and don't let pytest capture it.
            env["FLET_TEST_VERBOSE"] = "1"
            pytest_args += ["-s"]

        tests_path = Path(self.python_app_path) / self.tests_dir
        args = [sys.executable, "-m", "pytest", str(tests_path), *pytest_args]
        console.log(f"Running tests: {' '.join(args)}")
        return subprocess.run(args, cwd=str(self.python_app_path), env=env).returncode


def provision_test_host(
    project_dir: str,
    platform_name: Optional[str] = None,
    device_id: Optional[str] = None,
    verbose: int = 0,
) -> Path:
    """
    Provision (or reuse the cached) Flutter test host for the app at
    `project_dir` and return its directory. Also wires up the current process
    environment (PATH to the resolved Flutter SDK, FLET_TEST_DISABLE_FVM) so a
    subsequent `flutter test` launched by FletTestApp works.

    Called by the pytest plugin so that `uv run pytest` works without first
    running `flet test`. Cached by the build pipeline's input hash, so warm
    runs are fast.
    """
    parser = argparse.ArgumentParser()
    cmd = Command(parser)
    plat = platform_name or _default_desktop_platform()

    argv = [plat]
    if device_id:
        argv += ["-d", device_id]
    options = parser.parse_args(argv)
    options.python_app_path = str(Path(project_dir).resolve())
    options.output_dir = None
    options.verbose = verbose
    options.assume_yes = True

    cmd.options = options
    cmd.no_rich_output = cmd.no_rich_output or options.no_rich_output
    cmd.verbose = verbose
    cmd.assume_yes = True
    cmd.test_platform_name = plat
    cmd.target_platform = TEST_PLATFORMS[plat]["target_platform"]

    cmd.status = console.status(
        f"[bold blue]Provisioning {cmd.target_platform} test host...",
        spinner="bouncingBall",
    )
    with Live(Group(cmd.status, cmd.progress), console=console) as cmd.live:
        flutter_dir = _provision_steps(cmd)

    # Make the SDK discoverable for the FletTestApp-spawned `flutter test` and
    # propagate the SERIOUS_PYTHON_* vars so the native build bundles
    # site-packages into the app.
    env = _flutter_path_env(cmd)
    for key in _TEST_ENV_KEYS:
        if key in env:
            os.environ[key] = env[key]
    return flutter_dir
