import argparse
import os
import re
from pathlib import Path

from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Column, Table

from flet_cli.commands.flutter_base import BaseFlutterCommand, console, verbose2_style
from flet_cli.utils.android_sdk import AndroidSDK


class Command(BaseFlutterCommand):
    """
    List, create, and launch available emulators.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)
        self.action = None
        self.emulator_target = None
        self.cold_boot = False
        self.emulator_name = None

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "action",
            type=str.lower,
            nargs="?",
            choices=["start", "create", "delete"],
            help="Action to perform: start an emulator, create a new one, "
            "or delete it.",
        )
        parser.add_argument(
            "emulator",
            type=str,
            nargs="?",
            help="Emulator ID or name (required for start, create, and delete).",
        )
        parser.add_argument(
            "--cold",
            dest="cold",
            action="store_true",
            default=False,
            help="Cold boot the emulator when starting.",
        )
        super().add_arguments(parser)

    def handle(self, options: argparse.Namespace) -> None:
        super().handle(options)
        if self.options:
            self.action = self.options.action
            self.emulator_target = self.options.emulator
            self.emulator_name = self.options.emulator
            self.cold_boot = bool(self.options.cold)

        self.status = console.status(
            "[bold blue]Initializing environment...",
            spinner="bouncingBall",
        )
        with Live(Group(self.status, self.progress), console=console) as self.live:
            self.initialize_command()
            if self.action == "delete":
                if not self.emulator_target:
                    self.skip_flutter_doctor = True
                    self.cleanup(1, "Provide emulator ID or name to delete.")
                self._delete_emulator()
                return
            if self.action == "create":
                if not self.emulator_name:
                    self.skip_flutter_doctor = True
                    self.cleanup(1, "Provide emulator name to create.")
                self._create_emulator()
                return
            if self.action == "start":
                if not self.emulator_target:
                    self.skip_flutter_doctor = True
                    self.cleanup(1, "Provide emulator ID or name to start.")
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
                '\nRun [green]"flet emulators create <name>"[/green] '
                "to create a new emulator.\n"
            )
            self.cleanup(0, Group(Panel("No emulators found."), footer), no_border=True)

        table = Table(
            Column("ID", style="magenta", justify="left", no_wrap=True),
            Column("Name", style="cyan", justify="left"),
            Column("Platform", style="green", justify="center"),
            Column("Manufacturer", style="yellow", justify="left"),
            title="Available emulators",
            header_style="bold",
            show_lines=True,
        )

        for emulator in emulators:
            table.add_row(
                emulator["id"],
                emulator["name"],
                emulator["platform_label"],
                emulator["manufacturer"],
            )

        footer = (
            "\n"
            "Launch an emulator with "
            '[green]"flet emulators start <emulator-id>"[/green].\n'
            "Create a new emulator with "
            '[green]"flet emulators create <name>"[/green].\n'
            "Delete an Android emulator with "
            '[green]"flet emulators delete <emulator-id>"[/green].\n'
            "\n"
            "You can find more information on managing emulators at the links below:\n"
            "  https://developer.android.com/studio/run/managing-avds\n"
            "  https://developer.android.com/studio/command-line/avdmanager"
        )

        self.cleanup(0, message=Group(table, footer), no_border=True)

    def _launch_emulator(self):
        assert self.emulator_target
        self.update_status(
            f"[bold blue]Starting emulator [cyan]{self.emulator_target}[/cyan]..."
        )
        args = [
            self.flutter_exe,
            "emulators",
            "--launch",
            self.emulator_target,
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
                (
                    error_output
                    if error_output
                    else f"Failed to start emulator '{self.emulator_target}'."
                ),
            )
            return

        if output and self.verbose >= 1:
            console.log(output, style=verbose2_style)

        mode = " (cold boot)" if self.cold_boot else ""
        self.cleanup(0, f"Emulator [cyan]{self.emulator_target}[/cyan] started{mode}.")

    def _delete_emulator(self):
        assert self.emulator_target
        self.update_status(
            f"[bold blue]Deleting emulator [cyan]{self.emulator_target}[/cyan]..."
        )
        home_dir = self.env.get("ANDROID_HOME") or AndroidSDK.android_home_dir()
        if not home_dir:
            self.cleanup(
                1, "ANDROID_HOME is not set and Android SDK location cannot be found."
            )

        sdk = AndroidSDK(
            self.env.get("JAVA_HOME", ""), self.log_stdout, progress=self.progress
        )

        try:
            sdk.delete_avd(Path(home_dir), self.emulator_target)
        except Exception as exc:  # pragma: no cover - defensive
            self.skip_flutter_doctor = True
            self.cleanup(
                1, f"Failed to delete emulator '{self.emulator_target}': {exc}"
            )
            return

        self.cleanup(0, f"Deleted emulator [cyan]{self.emulator_target}[/cyan].")

    def _create_emulator(self):
        self.update_status("[bold blue]Creating emulator...")
        if not self._is_valid_emulator_name(self.emulator_name):
            self.skip_flutter_doctor = True
            self.cleanup(
                1,
                "Emulator name is invalid. Allowed characters: a-z A-Z 0-9 . _ -",
            )

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
        error_output = create_result.stderr or output
        invalid_name = (
            "contains invalid characters" in (error_output or "").lower()
            or "contains invalid characters" in output.lower()
        )
        exit_code = create_result.returncode or (1 if invalid_name else 0)
        if exit_code != 0:
            self.cleanup(
                exit_code,
                error_output or "Failed to create emulator.",
            )
            return

        if output and self.verbose >= 1:
            console.log(output, style=verbose2_style)

        created_name = self.emulator_name
        self.cleanup(
            0,
            f"Created emulator [cyan]{created_name}[/cyan]. "
            "Use `flet emulators` to list it or "
            f"`flet emulators start {created_name}` to start it.",
        )

    def _is_valid_emulator_name(self, name: str) -> bool:
        return bool(re.match(r"^[A-Za-z0-9._-]+$", name or ""))

    def _parse_emulators_output(self, output: str) -> list[dict]:
        emulators = []
        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line or "\u2022" not in line:
                continue
            parts = [p.strip() for p in line.split("\u2022") if p.strip()]
            if len(parts) < 2:
                continue

            emulator_id = parts[0]
            name = parts[1]
            # Skip header rows printed by `flutter emulators` (Id • Name • Platform ...)
            lower_head = {p.lower() for p in parts[:4]}
            if {"id", "name", "platform"}.issubset(lower_head):
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
