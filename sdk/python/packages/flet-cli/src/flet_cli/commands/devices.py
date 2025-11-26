import argparse
import os

from rich.console import Group
from rich.live import Live

from flet_cli.commands.build_base import BaseFlutterCommand, console, verbose2_style


class Command(BaseFlutterCommand):
    """
    List all connected devices.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)
        self.devices_platform = None

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "platform",
            type=str,
            nargs="?",
            choices=["ios", "android", "web"],
            help="The target platform to list devices for. "
            "If not specified, lists all platforms.",
        )
        # parser.add_argument(
        #     "--device-id",
        #     "-d",
        #     type=str,
        #     dest="device_id",
        #     help="Device ID to run the app on for iOS and Android builds.",
        # )
        # parser.add_argument(
        #     "--show-devices",
        #     dest="show_devices",
        #     action="store_true",
        #     default=False,
        #     help="Show connected devices for iOS and Android builds.",
        # )
        # parser.add_argument(
        #     "--release",
        #     dest="release",
        #     action="store_true",
        #     default=False,
        #     help="Build the app in release mode.",
        # )
        # parser.add_argument(
        #     "--route",
        #     type=str,
        #     dest="route",
        #     help="Route to open the app on for web, iOS and Android builds.",
        # )
        super().add_arguments(parser)

    def handle(self, options: argparse.Namespace) -> None:
        super().handle(options)
        if self.options and "platform" in self.options and self.options.platform:
            self.devices_platform = self.options.platform

        self.status = console.status(
            "[bold blue]Initializing environment...",
            spinner="bouncingBall",
        )
        with Live(Group(self.status, self.progress), console=console) as self.live:
            self.initialize_command()
            # if self.options.show_devices:
            #     self.run_flutter_devices()
            #     self.live.update("", refresh=True)
            #     return
            self.run_flutter_devices()
            self.cleanup(0, message=(""))

    def initialize_command(self):
        self.package_platform = ""
        self.config_platform = ""

        super().initialize_command()

    def run_flutter_devices(self):
        self.update_status("[bold blue]Checking connected devices...")
        flutter_devices = self.run(
            [self.flutter_exe, "devices", "--no-version-check", "--suppress-analytics"],
            cwd=os.getcwd(),
            capture_output=True,
        )
        if flutter_devices.returncode == 0 and flutter_devices.stdout:
            console.log(flutter_devices.stdout, style=verbose2_style)
