import argparse
import os
import platform

from rich.console import Group
from rich.live import Live
from rich.progress import Progress

from flet_cli.commands.flutter_base import BaseFlutterCommand, console, verbose2_style


class Command(BaseFlutterCommand):
    """
    Run a Flet Python app in debug mode on a specified platform (desktop, web, mobile).
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)

        self.debug_platforms = {
            "windows": {"target_platform": "windows", "device_id": "windows"},
            "macos": {"target_platform": "macos", "device_id": "macos"},
            "linux": {"target_platform": "linux", "device_id": "linux"},
            "web": {"target_platform": "web", "device_id": "chrome"},
            "ios": {"target_platform": "ipa", "device_id": None},
            "android": {"target_platform": "apk", "device_id": None},
        }
        self.device_id = None

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "platform",
            type=str,
            nargs="?",
            choices=["macos", "linux", "windows", "web", "ios", "android"],
            help="The target platform to run the app on",
        )
        parser.add_argument(
            "--device-id",
            "-d",
            type=str,
            dest="device_id",
            help="Device ID to run the app on for iOS and Android builds.",
        )
        parser.add_argument(
            "--show-devices",
            dest="show_devices",
            action="store_true",
            default=False,
            help="Show connected devices for iOS and Android builds.",
        )
        parser.add_argument(
            "--route",
            type=str,
            dest="route",
            help="Route to open the app on for web, iOS and Android builds.",
        )
        super().add_arguments(parser)

    def handle(self, options: argparse.Namespace) -> None:
        super().handle(options)
        self.options.output_dir = None  # disable output dir for debug builds
        if self.options:
            if "platform" in self.options and self.options.platform:
                self.debug_platform = self.options.platform
            else:
                self.debug_platform = platform.system().lower()
                if self.debug_platform == "darwin":
                    self.debug_platform = "macos"
            self.target_platform = self.debug_platforms[self.debug_platform][
                "target_platform"
            ]
            self.device_id = self.debug_platforms[self.debug_platform]["device_id"]
            if self.options.device_id:
                self.device_id = self.options.device_id

        self.status = console.status(
            f"[bold blue]Initializing {self.target_platform} debug session...",
            spinner="bouncingBall",
        )
        self.progress = Progress(transient=True)
        self.no_rich_output = self.no_rich_output or self.options.no_rich_output
        self.verbose = self.options.verbose
        with Live(Group(self.status, self.progress), console=console) as self.live:
            self.check_device_id()
            self.initialize_build()
            if self.options.show_devices:
                self.run_flutter_devices()
                self.live.update("", refresh=True)
                return
            self.validate_target_platform()
            self.validate_entry_point()
            self.setup_template_data()
            self.create_flutter_project()
            self.package_python_app()
            self.register_flutter_extensions()
            if self.create_flutter_project(second_pass=True):
                self.update_flutter_dependencies()
            self.customize_icons()
            self.customize_splash_images()
            self.flutter_build()

            self.cleanup(
                0,
                message=(
                    f"Successfully built your [cyan]"
                    f"{self.platforms[self.target_platform]['status_text']}"
                    f"[/cyan]! {self.emojis['success']} "
                    f"Find it in [cyan]{self.rel_out_dir}[/cyan] directory. "
                    f"{self.emojis['directory']}"
                    + (
                        "\nRun [cyan]flet serve[/cyan] command to start a web server "
                        "with your app. "
                        if self.target_platform == "web"
                        else ""
                    )
                ),
            )

    def check_device_id(self):
        if self.device_id is None and self.debug_platform in [
            "ios",
            "android",
        ]:
            self.skip_flutter_doctor = True
            self.cleanup(
                1,
                "Device ID must be specified for iOS and Android debug builds.\n"
                "Use --device-id option to specify it.\n"
                "Use --show-devices option to list connected devices.",
            )

    def add_flutter_build_args(self, args: list[str]):
        assert self.device_id
        args.extend(["run", "-d", self.device_id])

    def run_flutter_devices(self):
        self.update_status("[bold blue]Checking connected devices...")
        flutter_devices = self.run(
            [self.flutter_exe, "devices", "--no-version-check", "--suppress-analytics"],
            cwd=os.getcwd(),
            capture_output=True,
        )
        if flutter_devices.returncode == 0 and flutter_devices.stdout:
            console.log(flutter_devices.stdout, style=verbose2_style)
