import argparse
import os

from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Column, Table

from flet_cli.commands.flutter_base import BaseFlutterCommand, console, verbose2_style


class Command(BaseFlutterCommand):
    """
    List all connected iOS and Android devices.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)
        self.devices_platform = None
        self.device_timeout = 10
        self.device_connection = "default"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "platform",
            type=str.lower,
            nargs="?",
            choices=["ios", "android"],
            help="The target platform to list devices for. "
            "If not specified, lists all platforms.",
        )
        parser.add_argument(
            "--device-timeout",
            type=int,
            default=10,
            dest="device_timeout",
            help="Time (in seconds) to wait for devices to attach",
        )
        parser.add_argument(
            "--device-connection",
            type=str.lower,
            choices=["both", "attached", "wireless"],
            default="both",
            dest="device_connection",
            help="Filter devices by connection type: attached (USB) or wireless",
        )
        super().add_arguments(parser)

    def handle(self, options: argparse.Namespace) -> None:
        super().handle(options)
        if self.options and "platform" in self.options and self.options.platform:
            self.devices_platform = self.options.platform
        if self.options and "device_timeout" in self.options:
            self.device_timeout = self.options.device_timeout or 10
        if self.options and "device_connection" in self.options:
            self.device_connection = self.options.device_connection
        self.platform_label = self.platform_labels[self.devices_platform]

        self.status = console.status(
            "[bold blue]Initializing environment...",
            spinner="bouncingBall",
        )
        with Live(Group(self.status, self.progress), console=console) as self.live:
            self.initialize_command()
            self.run_flutter_devices()
            self.cleanup(0)

    def initialize_command(self):
        self.require_android_sdk = True

        super().initialize_command()

    def run_flutter_devices(self):
        self.update_status(
            f"[bold blue]Checking connected {self.platform_label} devices..."
        )
        flutter_devices = self.run(
            [
                self.flutter_exe,
                "devices",
                "--no-version-check",
                "--suppress-analytics",
                "--device-timeout",
                str(self.device_timeout),
            ],
            cwd=os.getcwd(),
            capture_output=True,
        )
        output = flutter_devices.stdout or ""

        if flutter_devices.returncode != 0:
            error_output = flutter_devices.stderr or output
            self.cleanup(
                flutter_devices.returncode,
                message=(
                    error_output or "Failed to retrieve devices via `flutter devices`."
                ),
            )
            return None

        if output and self.verbose >= 1:
            console.log(output, style=verbose2_style)

        footer = (
            '\nRun [green]"flet emulators"[/green] to list '
            "and start any available device emulators.\n"
        )

        devices = [
            device
            for device in self._parse_devices_output(output)
            if device["platform"] in ("ios", "android")
        ]
        if self.device_connection != "both":
            devices = [d for d in devices if d["connection"] == self.device_connection]
        if self.devices_platform:
            devices = [d for d in devices if d["platform"] == self.devices_platform]

        if not devices:
            self.cleanup(
                0,
                Group(Panel(f"No {self.platform_label} devices found."), footer),
                no_border=True,
            )

        devices_table = Table(
            Column("ID", style="magenta", justify="left", no_wrap=True),
            Column("Name", style="cyan", justify="left"),
            Column("Platform", style="green", justify="center"),
            Column("Details", style="yellow", justify="left"),
            title=f"Connected {self.platform_label} devices",
            header_style="bold",
            show_lines=True,
        )

        for device in devices:
            devices_table.add_row(
                device["id"],
                device["name"],
                device["platform_label"],
                device["details"],
            )

        self.cleanup(0, message=Group(devices_table, footer), no_border=True)

    def _parse_devices_output(self, output: str) -> list[dict]:
        devices = []
        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line or "\u2022" not in line:
                continue
            parts = [p.strip() for p in line.split("\u2022")]
            if len(parts) < 3:
                continue

            name = parts[0]
            device_id = parts[1]
            platform_raw = parts[2]
            details = parts[3] if len(parts) > 3 else ""
            platform = self._normalize_platform(platform_raw)
            connection = self._detect_connection_type(parts)

            devices.append(
                {
                    "name": name,
                    "id": device_id,
                    "platform": platform,
                    "platform_label": platform_raw,
                    "connection": connection,
                    "details": details,
                }
            )

        return devices

    def _normalize_platform(self, platform_raw: str) -> str | None:
        platform_lower = platform_raw.lower()
        if "android" in platform_lower:
            return "android"
        if "ios" in platform_lower:
            return "ios"
        return None

    def _detect_connection_type(self, parts: list[str]) -> str:
        # Heuristic: Flutter prints "wireless" or "wifi" in one of the bullet segments
        # for wireless devices. Default to "attached" otherwise.
        parts_lower = " ".join(parts).lower()
        if "wireless" in parts_lower or "wi-fi" in parts_lower or "wifi" in parts_lower:
            return "wireless"
        return "attached"
