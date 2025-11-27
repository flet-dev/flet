import argparse
import os

from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Column, Table

from flet_cli.commands.build_base import BaseFlutterCommand, console, verbose2_style


class Command(BaseFlutterCommand):
    """
    List, create, and launch available emulators.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)
        self.launch_target = None
        self.cold_boot = False
        self.create_emulator = False
        self.emulator_name = None

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--launch",
            dest="launch",
            type=str,
            help="Launch a specific emulator by ID or name.",
        )
        parser.add_argument(
            "--cold",
            dest="cold",
            action="store_true",
            default=False,
            help="Cold boot the emulator when launching.",
        )
        parser.add_argument(
            "--create",
            dest="create",
            action="store_true",
            default=False,
            help="Create a new emulator using Flutter defaults.",
        )
        parser.add_argument(
            "--name",
            dest="name",
            type=str,
            help="Name for the new emulator (used with --create).",
        )
        super().add_arguments(parser)

    def handle(self, options: argparse.Namespace) -> None:
        super().handle(options)
        if self.options:
            self.launch_target = self.options.launch
            self.cold_boot = bool(self.options.cold)
            self.create_emulator = bool(self.options.create)
            self.emulator_name = self.options.name

        if self.create_emulator and self.launch_target:
            console.log(
                "Please choose either --create or --launch, not both.",
                style=verbose2_style,
            )
            self.cleanup(
                1, Panel("Please choose either --create or --launch, not both.")
            )

        self.status = console.status(
            "[bold blue]Initializing environment...",
            spinner="bouncingBall",
        )
        with Live(Group(self.status, self.progress), console=console) as self.live:
            self.initialize_command()
            if self.create_emulator:
                self._create_emulator()
                return
            if self.launch_target:
                self._launch_emulator()
                return
            self._list_emulators()

    def initialize_command(self):
        self.require_android_sdk = True

        super().initialize_command()

    def _list_emulators(self):
        self.update_status("[bold blue]Listing available emulators...")
        emulators_process = self.run(
            [
                self.flutter_exe,
                "emulators",
                "--no-version-check",
                "--suppress-analytics",
            ],
            cwd=os.getcwd(),
            capture_output=True,
        )
        output = emulators_process.stdout or ""

        if emulators_process.returncode != 0:
            error_output = emulators_process.stderr or output
            self.cleanup(
                emulators_process.returncode,
                message=(
                    error_output
                    or "Failed to retrieve emulators via `flutter emulators`."
                ),
            )
            return

        if output and self.verbose >= 1:
            console.log(output, style=verbose2_style)

        emulators = self._parse_emulators_output(output)
        if not emulators:
            footer = (
                '\nRun [green]"flet emulators --create"[/green] '
                "to create a new emulator.\n"
            )
            self.cleanup(0, Group(Panel("No emulators found."), footer))

        table = Table(
            Column("Name", style="cyan", justify="left"),
            Column("ID", style="magenta", justify="left", no_wrap=True),
            Column("Platform", style="green", justify="center"),
            Column("Manufacturer", style="yellow", justify="left"),
            title="Available emulators",
            header_style="bold",
            show_lines=True,
        )

        for emulator in emulators:
            table.add_row(
                emulator["name"],
                emulator["id"],
                emulator["platform_label"],
                emulator["manufacturer"],
            )

        footer = (
            "\n"
            "Launch an emulator with "
            '[green]"flet emulators --launch <emulator-id>"[/green].\n'
            "Create a new emulator with "
            '[green]"flet emulators --create [--name <name>]"[/green].\n'
            "\n"
            "You can find more information on managing emulators at the links below:\n"
            "  https://developer.android.com/studio/run/managing-avds\n"
            "  https://developer.android.com/studio/command-line/avdmanager"
        )

        self.cleanup(0, message=Group(table, footer))

    def _launch_emulator(self):
        assert self.launch_target
        self.update_status(
            f"[bold blue]Launching emulator [cyan]{self.launch_target}[/cyan]..."
        )
        args = [
            self.flutter_exe,
            "emulators",
            "--launch",
            self.launch_target,
            "--no-version-check",
            "--suppress-analytics",
        ]
        if self.cold_boot:
            args.append("--cold")

        launch_result = self.run(
            args,
            cwd=os.getcwd(),
            capture_output=True,
        )

        output = launch_result.stdout or ""
        if launch_result.returncode != 0:
            error_output = launch_result.stderr or output
            self.cleanup(
                launch_result.returncode,
                Panel(
                    error_output or f"Failed to launch emulator '{self.launch_target}'."
                ),
            )
            return

        if output and self.verbose >= 1:
            console.log(output, style=verbose2_style)

        mode = " (cold boot)" if self.cold_boot else ""
        self.cleanup(
            0,
            Panel(
                f"Emulator [cyan]{self.launch_target}[/cyan] launched{mode}.",
            ),
        )

    def _create_emulator(self):
        self.update_status("[bold blue]Creating emulator...")
        args = [
            self.flutter_exe,
            "emulators",
            "--create",
            "--no-version-check",
            "--suppress-analytics",
        ]
        if self.emulator_name:
            args.extend(["--name", self.emulator_name])

        create_result = self.run(
            args,
            cwd=os.getcwd(),
            capture_output=True,
        )
        output = create_result.stdout or ""
        if create_result.returncode != 0:
            error_output = create_result.stderr or output
            self.cleanup(
                create_result.returncode,
                Panel(error_output or "Failed to create emulator."),
            )
            return

        if output and self.verbose >= 1:
            console.log(output, style=verbose2_style)

        created_name = self.emulator_name or "emulator"
        self.cleanup(
            0,
            Panel(
                f"Created emulator [cyan]{created_name}[/cyan]. "
                "Use `flet emulators` to list it or "
                f"`flet emulators --launch {created_name}` to start it.",
            ),
        )

    def _parse_emulators_output(self, output: str) -> list[dict]:
        emulators = []
        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line or "\u2022" not in line:
                continue
            parts = [p.strip() for p in line.split("\u2022") if p.strip()]
            if len(parts) < 2:
                continue

            name = parts[0]
            emulator_id = parts[1]
            # Skip header rows printed by `flutter emulators` (Id • Name • Platform ...)
            if name.lower() == "id" and emulator_id.lower() == "name":
                continue
            details_segments = parts[2:]
            platform_raw = details_segments[-1] if details_segments else ""
            platform = self._normalize_platform(platform_raw)
            manufacturer = (
                " • ".join(details_segments[:-1]) if len(details_segments) > 1 else ""
            )
            platform_label = platform_raw or platform or "Unknown"

            emulators.append(
                {
                    "name": name,
                    "id": emulator_id,
                    "platform": platform,
                    "platform_label": platform_label,
                    "manufacturer": manufacturer,
                }
            )

        return emulators

    def _normalize_platform(self, platform_raw: str) -> str | None:
        platform_lower = platform_raw.lower()
        if "android" in platform_lower:
            return "android"
        if "ios" in platform_lower:
            return "ios"
        return None
