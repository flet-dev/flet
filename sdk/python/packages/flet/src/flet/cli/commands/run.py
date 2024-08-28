import argparse
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Optional, Union
from urllib.parse import quote, urlparse, urlunparse
import yaml
import qrcode
from flet.cli.commands.base import BaseCommand
from flet_core.utils import random_string
from flet_runtime.app import close_flet_view, open_flet_view
from flet_runtime.utils import (
    get_free_tcp_port,
    get_local_ip,
    is_windows,
    open_in_browser,
)
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from rich.console import Console, Style
from flet_runtime.utils import (
    copy_tree,
    is_windows,
    get_bool_env_var,
)
from rich.table import Table, Column
from packaging import version
import flet.version
from flet.version import update_version

if is_windows():
    from ctypes import windll


error_style = Style(color="red1")
console = Console(log_path=False, style=Style(color="green", bold=True))


class ClientCompiler:
    MINIMAL_FLUTTER_VERSION = "3.19.0"
    DEFAULT_TEMPLATE = "gh:andersou/flet-run-bootstrap-template"

    def __init__(
        self,
        python_app_path=".",
        target_platform=platform.system(),
        webrenderer="canvaskit",
    ) -> None:
        self.python_app_path = python_app_path
        self.web_renderer = webrenderer
        self.template = self.DEFAULT_TEMPLATE
        self.template_ref = None
        self.emojis = {}
        self.dart_exe = None
        self.verbose = None
        self.flutter_dir = None
        self.flutter_exe = None
        self.target_platform = target_platform.lower()
        if self.target_platform == "darwin":
            self.target_platform = "macos"
        self.verbose = 0
        self.platforms = {
            "windows": {
                "build_command": "windows",
                "status_text": "Windows app",
                "outputs": ["build/windows/x64/runner/Release/*"],
                "dist": "windows",
                "can_be_run_on": ["Windows"],
            },
            "macos": {
                "build_command": "macos",
                "status_text": "macOS bundle",
                "outputs": ["build/macos/Build/Products/Release/Flet.app"],
                "dist": "macos",
                "can_be_run_on": ["Darwin"],
            },
            "linux": {
                "build_command": "linux",
                "status_text": "app for Linux",
                "outputs": ["build/linux/{arch}/release/bundle/*"],
                "dist": "linux",
                "can_be_run_on": ["Linux"],
            },
            "web": {
                "build_command": "web",
                "status_text": "web app",
                "outputs": ["build/web/*"],
                "dist": "web",
                "can_be_run_on": ["Darwin", "Windows", "Linux"],
            },
            "apk": {
                "build_command": "apk",
                "status_text": ".apk for Android",
                "outputs": ["build/app/outputs/flutter-apk/*"],
                "dist": "apk",
                "can_be_run_on": ["Darwin", "Windows", "Linux"],
            },
            "aab": {
                "build_command": "appbundle",
                "status_text": ".aab bundle for Android",
                "outputs": ["build/app/outputs/bundle/release/*"],
                "dist": "aab",
                "can_be_run_on": ["Darwin", "Windows", "Linux"],
            },
            "ipa": {
                "build_command": "ipa",
                "status_text": ".ipa bundle for iOS",
                "outputs": ["build/ios/archive/*", "build/ios/ipa/*"],
                "dist": "ipa",
                "can_be_run_on": ["Darwin"],
            },
        }

        # create and display build-platform-matrix table
        self.platform_matrix_table = Table(
            Column("Command", style="cyan", justify="left"),
            Column("Platform", style="magenta", justify="center"),
            title="Build Platform Matrix",
            header_style="bold",
            show_lines=True,
        )
        for p, info in self.platforms.items():
            self.platform_matrix_table.add_row(
                "flet build " + p,
                ", ".join(info["can_be_run_on"]).replace("Darwin", "macOS"),
                # style="bold red1" if p == target_platform else None,
            )

    def run(self, args, cwd, capture_output=True):
        if is_windows():
            # Source: https://stackoverflow.com/a/77374899/1435891
            # Save the current console output code page and switch to 65001 (UTF-8)
            previousCp = windll.kernel32.GetConsoleOutputCP()
            windll.kernel32.SetConsoleOutputCP(65001)

        if self.verbose > 0:
            console.log(f"Run subprocess: {args}")

        r = subprocess.run(
            args,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            encoding="utf8",
        )

        if is_windows():
            # Restore the previous output console code page.
            windll.kernel32.SetConsoleOutputCP(previousCp)

        return r

    def compile_client(self) -> None:
        self.flutter_dir = None
        no_rich_output = get_bool_env_var("FLET_CLI_NO_RICH_OUTPUT")
        self.emojis = {
            "checkmark": "[green]OK[/]" if no_rich_output else "✅",
            "loading": "" if no_rich_output else "⏳",
            "success": "" if no_rich_output else "🥳",
            "directory": "" if no_rich_output else "📁",
        }
        target_platform = self.target_platform
        # platform check
        current_platform = platform.system()
        if current_platform not in self.platforms[target_platform]["can_be_run_on"]:
            can_build_message = (
                "can't"
                if current_platform
                not in self.platforms[target_platform]["can_be_run_on"]
                else "can"
            )
            # replace "Darwin" with "macOS" for user-friendliness
            current_platform = (
                "macOS" if current_platform == "Darwin" else current_platform
            )
            # highlight the current platform in the build matrix table
            self.platform_matrix_table.rows[
                list(self.platforms.keys()).index(target_platform)
            ].style = "bold red1"
            console.log(self.platform_matrix_table)

            message = f"You {can_build_message} build [cyan]{target_platform}[/] on [magenta]{current_platform}[/]."
            self.cleanup(1, message)

        with console.status(
            f"[bold blue]Initializing {target_platform} build... ",
            spinner="bouncingBall",
        ) as self.status:
            from cookiecutter.main import cookiecutter

            # get `flutter` and `dart` executables from PATH
            self.flutter_exe = self.find_flutter_batch("flutter")
            self.dart_exe = self.find_flutter_batch("dart")

            if self.verbose > 1:
                console.log("Flutter executable:", self.flutter_exe)
                console.log("Dart executable:", self.dart_exe)

            python_app_path = Path(self.python_app_path).resolve()
            if not os.path.exists(python_app_path) or not os.path.isdir(
                python_app_path
            ):
                self.cleanup(
                    1,
                    f"Path to Flet app does not exist or is not a directory: {python_app_path}",
                )

            self.flutter_dir = Path(tempfile.gettempdir()).joinpath(
                f"flet_flutter_build_{random_string(10)}"
            )

            if self.verbose > 0:
                console.log("Flutter bootstrap directory:", self.flutter_dir)
            self.flutter_dir.mkdir(exist_ok=True)

            rel_out_dir = os.path.join(".flet", self.platforms[target_platform]["dist"])

            out_dir = python_app_path.joinpath(rel_out_dir)

            src_pubspec = None
            src_pubspec_path = python_app_path.joinpath("pubspec.yaml")
            if src_pubspec_path.exists():
                with open(src_pubspec_path, encoding="utf8") as f:
                    src_pubspec = pubspec = yaml.safe_load(f)

            flutter_dependencies = (
                src_pubspec["dependencies"]
                if src_pubspec and src_pubspec["dependencies"]
                else {}
            )

            # if options.flutter_packages:
            #     for package in options.flutter_packages:
            #         pspec = package.split(":")
            #         flutter_dependencies[pspec[0]] = (
            #             pspec[1] if len(pspec) > 1 else "any"
            #         )

            if self.verbose > 0:
                console.log(
                    f"Additional Flutter dependencies: {flutter_dependencies}"
                    if flutter_dependencies
                    else "No additional Flutter dependencies!"
                )

            template_data = {
                "out_dir": self.flutter_dir.name,
                "sep": os.sep,
                "web_renderer": self.web_renderer,
                "flutter": {"dependencies": list(flutter_dependencies.keys())},
            }
            # Remove None values from the dictionary
            template_data = {k: v for k, v in template_data.items() if v is not None}

            template_url = self.template
            template_ref = self.template_ref

            if not template_ref:
                template_ref = (
                    version.Version(flet.version.version).base_version
                    if flet.version.version
                    else update_version()
                )

            # create Flutter project from a template
            self.status.update(
                f"[bold blue]Creating Flutter bootstrap project from {template_url} with ref {template_ref} {self.emojis['loading']}... ",
            )
            try:
                cookiecutter(
                    template=template_url,
                    # directory=options.template_dir,
                    output_dir=str(self.flutter_dir.parent),
                    no_input=True,
                    overwrite_if_exists=True,
                    extra_context=template_data,
                )
            except Exception as e:
                console.log(e)
                self.cleanup(1, f"{e}")
            console.log(
                f"Created Flutter bootstrap project from {template_url} with ref {template_ref} {self.emojis['checkmark']}",
            )

            # load pubspec.yaml
            pubspec_path = str(self.flutter_dir.joinpath("pubspec.yaml"))
            with open(pubspec_path, encoding="utf8") as f:
                pubspec = yaml.safe_load(f)

            # merge dependencies to a dest pubspec.yaml
            for k, v in flutter_dependencies.items():
                pubspec["dependencies"][k] = v

            if src_pubspec and "dependency_overrides" in src_pubspec:
                pubspec["dependency_overrides"] = {}
                for k, v in src_pubspec["dependency_overrides"].items():
                    pubspec["dependency_overrides"][k] = v

            # # make sure project name is not named as any of dependencies
            # for dep in pubspec["dependencies"].keys():
            #     if dep == project_name:
            #         self.cleanup(
            #             1,
            #             f"Project name cannot have the same name as one of its dependencies: {dep}. "
            #             f"Use --project option to specify a different project name.",
            #         )

            # save pubspec.yaml
            with open(pubspec_path, "w", encoding="utf8") as f:
                yaml.dump(pubspec, f)

            # run `flutter build`
            self.status.update(
                f"[bold blue]Building [cyan]{self.platforms[target_platform]['status_text']}[/cyan] {self.emojis['loading']}... ",
            )
            build_args = [
                self.flutter_exe,
                "build",
                self.platforms[target_platform]["build_command"],
            ]

            if self.verbose > 1:
                build_args.append("--verbose")
            console.log(build_args)
            build_result = self.run(
                build_args, cwd=str(self.flutter_dir), capture_output=self.verbose < 1
            )

            if build_result.returncode != 0:
                if build_result.stdout:
                    console.log(build_result.stdout)
                if build_result.stderr:
                    console.log(build_result.stderr, style=error_style)
                self.cleanup(build_result.returncode, check_flutter_version=True)
            console.log(
                f"Built [cyan]{self.platforms[target_platform]['status_text']}[/cyan] {self.emojis['checkmark']}",
            )

            # copy build results to `out_dir`
            self.status.update(
                f"[bold blue]Copying build to [cyan]{rel_out_dir}[/cyan] directory {self.emojis['loading']}... ",
            )
            arch = platform.machine().lower()
            if arch == "x86_64" or arch == "amd64":
                arch = "x64"
            elif arch == "arm64" or arch == "aarch64":
                arch = "arm64"

            for build_output in self.platforms[target_platform]["outputs"]:
                build_output_dir = str(self.flutter_dir.joinpath(build_output))

                if self.verbose > 0:
                    console.log("Copying build output from: " + build_output_dir)

                build_output_glob = os.path.basename(build_output_dir)
                build_output_dir = os.path.dirname(build_output_dir)
                if not os.path.exists(build_output_dir):
                    continue

                if out_dir.exists():
                    shutil.rmtree(str(out_dir), ignore_errors=False, onerror=None)
                out_dir.mkdir(parents=True, exist_ok=True)

                def ignore_build_output(path, files):
                    if path == build_output_dir and build_output_glob != "*":
                        return [f for f in os.listdir(path) if f != build_output_glob]
                    return []

                copy_tree(build_output_dir, str(out_dir), ignore=ignore_build_output)

            assets_path = python_app_path.joinpath("assets")
            if target_platform == "web" and assets_path.exists():
                # copy `assets` directory contents to the output directory
                copy_tree(str(assets_path), str(out_dir))

            console.log(
                f"Copied build to [cyan]{rel_out_dir}[/cyan] directory {self.emojis['checkmark']}"
            )

            self.cleanup(
                0,
                message=f"Successfully built your [cyan]{self.platforms[target_platform]['status_text']}[/cyan]! {self.emojis['success']} "
                f"Find it in [cyan]{rel_out_dir}[/cyan] directory. {self.emojis['directory']}",
            )

    def find_flutter_batch(self, exe_filename: str):
        batch_path = shutil.which(exe_filename)
        if not batch_path:
            self.cleanup(
                1,
                f"`{exe_filename}` command is not available in PATH. Install Flutter SDK.",
            )
            return
        if is_windows() and batch_path.endswith(".file"):
            return batch_path.replace(".file", ".bat")
        return batch_path

    def cleanup(
        self, exit_code: int, message: Optional[str] = None, check_flutter_version=False
    ):
        if self.flutter_dir and os.path.exists(self.flutter_dir):
            if self.verbose > 0:
                console.log(f"Deleting Flutter bootstrap directory {self.flutter_dir}")
            shutil.rmtree(str(self.flutter_dir), ignore_errors=True, onerror=None)
        if exit_code == 0:
            msg = message or f"Success! {self.emojis['success']}"
            console.log(msg)
        else:
            msg = (
                message
                if message is not None
                else "Error building Flet app - see the log of failed command above."
            )
            console.log(msg, style=error_style)

            if check_flutter_version:
                version_results = self.run(
                    [self.flutter_exe, "--version"],
                    cwd=os.getcwd(),
                    capture_output=True,
                )
                if version_results.returncode == 0 and version_results.stdout:
                    match = re.search(
                        r"Flutter (\d+\.\d+\.\d+)", version_results.stdout
                    )
                    if match:
                        flutter_version = version.parse(match.group(1))
                        if flutter_version < version.parse(
                            self.MINIMAL_FLUTTER_VERSION
                        ):
                            flutter_msg = (
                                "Incorrect version of Flutter SDK installed. "
                                + f"Flet build requires Flutter {self.MINIMAL_FLUTTER_VERSION} or above. "
                                + f"You have {flutter_version}."
                            )
                            console.log(flutter_msg, style=error_style)
            # run flutter doctor
            self.run_flutter_doctor(style=error_style)

        raise Exception(f"Exit code: {exit_code}\n {message}")

    def run_flutter_doctor(self, style: Optional[Union[Style, str]] = None):
        self.status.update(
            f"[bold blue]Running Flutter doctor {self.emojis['loading']}... "
        )
        flutter_doctor = self.run(
            [self.flutter_exe, "doctor"],
            cwd=os.getcwd(),
            capture_output=True,
        )
        if flutter_doctor.returncode == 0 and flutter_doctor.stdout:
            console.log(flutter_doctor.stdout, style=style)


class Command(BaseCommand):
    """
    Run Flet app.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "script",
            type=str,
            nargs="?",
            default=".",
            help="path to a Python script",
        )
        parser.add_argument(
            "-p",
            "--port",
            dest="port",
            type=int,
            default=None,
            help="custom TCP port to run Flet app on",
        )
        parser.add_argument(
            "--host",
            dest="host",
            type=str,
            default=None,
            help='host to run Flet web app on. Use "*" to listen on all IPs.',
        )
        parser.add_argument(
            "--name",
            dest="app_name",
            type=str,
            default=None,
            help="app name to distinguish it from other on the same port",
        )
        parser.add_argument(
            "-m",
            "--module",
            dest="module",
            action="store_true",
            default=False,
            help="treat the script as a python module path as opposed to a file path",
        )
        parser.add_argument(
            "-d",
            "--directory",
            dest="directory",
            action="store_true",
            default=False,
            help="watch script directory",
        )
        parser.add_argument(
            "-r",
            "--recursive",
            dest="recursive",
            action="store_true",
            default=False,
            help="watch script directory and all sub-directories recursively",
        )
        parser.add_argument(
            "-n",
            "--hidden",
            dest="hidden",
            action="store_true",
            default=False,
            help="application window is hidden on startup",
        )
        parser.add_argument(
            "-w",
            "--web",
            dest="web",
            action="store_true",
            default=False,
            help="open app in a web browser",
        )
        parser.add_argument(
            "--ios",
            dest="ios",
            action="store_true",
            default=False,
            help="open app on iOS device",
        )
        parser.add_argument(
            "--android",
            dest="android",
            action="store_true",
            default=False,
            help="open app on Android device",
        )
        parser.add_argument(
            "-a",
            "--assets",
            dest="assets_dir",
            type=str,
            default="assets",
            help="path to assets directory",
        )
        parser.add_argument(
            "--ignore-dirs",
            dest="ignore_dirs",
            type=str,
            default=None,
            help="directories to ignore during watch. If more than one, separate with a comma.",
        )

    def needs_recompile_client(self, script) -> bool:
        python_app_path = Path(script).resolve()
        src_pubspec_path = python_app_path.joinpath("pubspec.yaml")
        if src_pubspec_path.exists():
            return True
        return False

    def compile_client(self, options: argparse.Namespace) -> bool:
        target_platform = platform.system().lower()
        if options.web:
            target_platform = "web"
        elif options.ios:
            target_platform = "ipa"
        elif options.android:
            target_platform = "apk"
        compiler = ClientCompiler(
            python_app_path=options.script, target_platform=target_platform
        )
        try:
            # compiler.compile_client()
            os.environ["FLET_WEB_PATH"] = str(
                (Path(options.script).joinpath(".flet").joinpath("web").resolve())
            )
            os.environ["FLET_VIEW_PATH"] = str(
                (
                    Path(options.script)
                    .joinpath(".flet")
                    .joinpath(compiler.target_platform)
                    .resolve()
                )
            )
            print("FLET_WEB_PATH", os.environ["FLET_WEB_PATH"])
            print("FLET_VIEW_PATH", os.environ["FLET_VIEW_PATH"])
            return True
        except Exception as e:
            console.log(e, style=error_style)
            print(e)
            return False

    def handle(self, options: argparse.Namespace) -> None:
        if self.needs_recompile_client(options.script):
            print("Recompiling client...")
            if self.compile_client(options):
                print("Client recompiled successfully.")
            else:
                print("Client recompilation failed.")
                print("Using default client")
        if options.module:
            script_path = str(options.script).replace(".", "/")
            if os.path.isdir(script_path):
                script_path += "/__main__.py"
            else:
                script_path += ".py"
        else:
            script_path = str(options.script)
            if not os.path.isabs(script_path):
                script_path = str(Path(os.getcwd()).joinpath(script_path).resolve())
            if os.path.isdir(script_path):
                script_path = os.path.join(script_path, "main.py")

        if not Path(script_path).exists():
            print(f"File or directory not found: {script_path}")
            sys.exit(1)

        script_dir = os.path.dirname(script_path)

        port = options.port
        if port is None and (options.ios or options.android):
            port = 8551
        elif port is None and (is_windows() or options.web):
            port = get_free_tcp_port()

        uds_path = None
        if port is None and not is_windows():
            uds_path = str(Path(tempfile.gettempdir()).joinpath(random_string(10)))

        assets_dir = options.assets_dir
        if assets_dir and not Path(assets_dir).is_absolute():
            assets_dir = str(
                Path(os.path.dirname(script_path)).joinpath(assets_dir).resolve()
            )

        ignore_dirs = (
            [
                str(Path(os.path.dirname(script_path)).joinpath(directory).resolve())
                for directory in options.ignore_dirs.split(",")
            ]
            if options.ignore_dirs
            else []
        )

        my_event_handler = Handler(
            args=[sys.executable, "-u"]
            + ["-m"] * options.module
            + [options.script if options.module else script_path],
            watch_directory=options.directory or options.recursive,
            script_path=script_path,
            port=port,
            host=options.host,
            page_name=options.app_name,
            uds_path=uds_path,
            web=options.web,
            ios=options.ios,
            android=options.android,
            hidden=options.hidden,
            assets_dir=assets_dir,
            ignore_dirs=ignore_dirs,
        )

        my_observer = Observer()
        my_observer.schedule(my_event_handler, script_dir, recursive=options.recursive)
        my_observer.start()

        try:
            while True:
                if my_event_handler.terminate.wait(1):
                    break
        except KeyboardInterrupt:
            pass

        close_flet_view(my_event_handler.pid_file)
        my_observer.stop()
        my_observer.join()


class Handler(FileSystemEventHandler):
    def __init__(
        self,
        args,
        watch_directory,
        script_path,
        port,
        host,
        page_name,
        uds_path,
        web,
        ios,
        android,
        hidden,
        assets_dir,
        ignore_dirs,
    ) -> None:
        super().__init__()
        self.args = args
        self.watch_directory = watch_directory
        self.script_path = script_path
        self.port = port
        self.host = host
        self.page_name = page_name
        self.uds_path = uds_path
        self.web = web
        self.ios = ios
        self.android = android
        self.hidden = hidden
        self.assets_dir = assets_dir
        self.ignore_dirs = ignore_dirs
        self.last_time = time.time()
        self.is_running = False
        self.fvp = None
        self.pid_file = None
        self.page_url_prefix = f"PAGE_URL_{time.time()}"
        self.page_url = None
        self.terminate = threading.Event()
        self.start_process()

    def start_process(self):
        p_env = {**os.environ}
        if self.web or self.ios or self.android:
            p_env["FLET_FORCE_WEB_SERVER"] = "true"

            # force page name for ios
            if self.ios or self.android:
                p_env["FLET_WEB_APP_PATH"] = "/".join(Path(self.script_path).parts[-2:])
        if self.port is not None:
            p_env["FLET_SERVER_PORT"] = str(self.port)
        if self.host is not None:
            p_env["FLET_SERVER_IP"] = str(self.host)
        if self.page_name:
            p_env["FLET_WEB_APP_PATH"] = self.page_name
        if self.uds_path is not None:
            p_env["FLET_SERVER_UDS_PATH"] = self.uds_path
        if self.assets_dir is not None:
            p_env["FLET_ASSETS_DIR"] = self.assets_dir
        p_env["FLET_DISPLAY_URL_PREFIX"] = self.page_url_prefix

        p_env["PYTHONIOENCODING"] = "utf-8"
        p_env["PYTHONWARNINGS"] = "default::DeprecationWarning"

        self.p = subprocess.Popen(
            self.args, env=p_env, stdout=subprocess.PIPE, encoding="utf-8"
        )

        self.is_running = True
        th = threading.Thread(target=self.print_output, args=[self.p], daemon=True)
        th.start()

    def on_any_event(self, event):
        for directory in self.ignore_dirs:
            child = os.path.abspath(event.src_path)
            # check if the file which triggered the reload is in the (ignored) directory
            if os.path.commonpath([directory]) == os.path.commonpath(
                [directory, child]
            ):
                return

        if (
            self.watch_directory or event.src_path == self.script_path
        ) and event.event_type in ["modified", "deleted", "created", "moved"]:

            current_time = time.time()
            if (current_time - self.last_time) > 0.5 and self.is_running:
                self.last_time = current_time
                th = threading.Thread(target=self.restart_program, args=(), daemon=True)
                th.start()

    def print_output(self, p):
        while True:
            line = p.stdout.readline()
            if not line:
                break
            line = line.rstrip("\r\n")
            if line.startswith(self.page_url_prefix):
                if not self.page_url:
                    self.page_url = line[len(self.page_url_prefix) + 1 :]
                    if (
                        self.page_url.startswith("http")
                        and not self.ios
                        and not self.android
                    ):
                        print(self.page_url)
                    if self.ios or self.android:
                        self.print_qr_code(self.page_url, self.android)
                    elif self.web:
                        open_in_browser(self.page_url)
                    else:
                        th = threading.Thread(
                            target=self.open_flet_view_and_wait, args=(), daemon=True
                        )
                        th.start()
            else:
                print(line)

    def open_flet_view_and_wait(self):
        self.fvp, self.pid_file = open_flet_view(
            self.page_url, self.assets_dir, self.hidden
        )
        self.fvp.wait()
        self.p.send_signal(signal.SIGTERM)
        try:
            self.p.wait(2)
        except subprocess.TimeoutExpired:
            self.p.kill()
        self.terminate.set()

    def restart_program(self):
        self.is_running = False
        self.p.send_signal(signal.SIGTERM)
        self.p.wait()
        self.start_process()

    def print_qr_code(self, orig_url: str, android: bool):
        u = urlparse(orig_url)
        ip_addr = get_local_ip()
        lan_url = urlunparse(
            (u.scheme, f"{ip_addr}:{u.port}", u.path, None, None, None)
        )
        # self.clear_console()
        print("App is running on:", lan_url)
        print("")
        qr_url = (
            urlunparse(
                (
                    "https",
                    "android.flet.dev",
                    quote(f"{ip_addr}:{u.port}{u.path}", safe="/"),
                    None,
                    None,
                    None,
                )
            )
            if android
            else urlunparse(
                ("flet", "flet-host", quote(lan_url, safe=""), None, None, None)
            )
        )
        # print(qr_url)
        qr = qrcode.QRCode()
        qr.add_data(qr_url)
        qr.print_ascii(invert=True)
        # qr.print_tty()
        print("")
        print("Scan QR code above with Camera app.")

    def clear_console(self):
        if platform.system() == "Windows":
            if platform.release() in {"10", "11"}:
                subprocess.run(
                    "", shell=True
                )  # Needed to fix a bug regarding Windows 10; not sure about Windows 11
                print("\033c", end="")
            else:
                subprocess.run(["cls"])
        else:  # Linux and Mac
            print("\033c", end="")
