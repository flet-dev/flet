import argparse
import os
import platform
import shutil
import subprocess
import sys

import flet.version
from flet.utils import cleanup_path
from rich.console import Console
from rich.status import Status
from rich.style import Style

from flet_cli.commands.base import BaseCommand

# Rich console setup for styled output
console = Console(log_path=False)


class Command(BaseCommand):
    """
    `flet doctor` command to provide information about the system and environment setup.
    """

    def handle(self, options: argparse.Namespace) -> None:
        """Handle the 'doctor' command."""
        verbose = options.verbose

        # Step-by-step checks (No need to store results)
        self.check_flet_version()
        self.check_python_version()
        self.check_os_info()

        # Extra details in verbose mode
        if verbose:
            self.check_virtual_env()

    def check_flet_version(self) -> None:
        """Check and print Flet version."""
        with console.status("[bold white]Checking Flet version..."):
            flet_version = flet.version.version or "Unknown"
            console.print(f"[green]✔ Flet Version:[/green] {flet_version}")

    def check_python_version(self) -> None:
        """Check and print Python version."""
        with console.status("[bold white]Checking Python version..."):
            console.print(f"[green]✔ Python Version:[/green] {sys.version}")

    def check_os_info(self) -> None:
        """Check and print OS information."""
        with console.status("[bold white]Checking OS information..."):
            os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
            console.print(f"[green]✔ Operating System:[/green] {os_info}")

    def check_virtual_env(self) -> None:
        """Check if a Python virtual environment is active."""
        with console.status("[bold white]Checking Python virtual environment..."):
            venv = os.getenv("VIRTUAL_ENV")
            conda_env = os.getenv("CONDA_PREFIX")

            if venv:
                console.print(f"[green]✔ Virtual Environment active:[/green] {venv}")
            elif conda_env:
                console.print(f"[green]✔ Conda Environment active:[/green] {conda_env}")
            else:
                console.print(
                    "[yellow]⚠ No virtual environment or Conda detected[/yellow]"
                )
