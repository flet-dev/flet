import argparse
import contextlib
import os
import platform

from rich.console import Group
from rich.live import Live

from flet_cli.commands.build_base import BaseBuildCommand, console, verbose2_style


class Command(BaseBuildCommand):
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
        self.debug_platform = None
        self.device_id = None

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "platform",
            type=str.lower,
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
            "--release",
            dest="release",
            action="store_true",
            default=False,
            help="Build the app in release mode.",
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
            self.platform_label = self.platform_labels[self.debug_platform]
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
        with Live(Group(self.status, self.progress), console=console) as self.live:
            self.check_device_id()
            self.initialize_command()
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
            self.run_flutter()
            self.cleanup(0, message="Debug session ended.")

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

    def add_flutter_command_args(self, args: list[str]):
        assert self.device_id
        args.extend(["run", "-d", self.device_id])

        if self.options:
            if self.options.release:
                args.append("--release")
            if self.options.route and self.debug_platform in [
                "web",
                "ios",
                "android",
            ]:
                args.extend(["--route", self.options.route])

    def run_flutter(self):
        assert self.platforms
        assert self.target_platform
        mode = "release" if self.options.release else "debug"
        self.update_status(
            f"[bold blue]Running {mode} version of the app on "
            f"[cyan]{self.platform_label}[/cyan] device..."
        )

        with contextlib.suppress(KeyboardInterrupt):
            self._run_flutter_command()

    def run_flutter_devices(self):
        self.update_status("[bold blue]Checking connected devices...")
        flutter_devices = self.run(
            [self.flutter_exe, "devices", "--no-version-check", "--suppress-analytics"],
            cwd=os.getcwd(),
            capture_output=True,
        )
        if flutter_devices.returncode == 0 and flutter_devices.stdout:
            console.log(flutter_devices.stdout, style=verbose2_style)
