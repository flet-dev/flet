import argparse
import platform
import sys
import os
import shutil
import subprocess
from rich.console import Console
from rich.style import Style
from rich.status import Status

import flet.version
from flet.utils import cleanup_path
from flet_cli.commands.base import BaseCommand

# Rich console setup for styled output
console = Console(log_path=False)


class Command(BaseCommand):
    """
    Check the health of your Flet environment.
    """

    def handle(self, options: argparse.Namespace) -> None:
        """Handle the 'doctor' command."""
        verbose = options.verbose

        console.print("\n[bold cyan]=== Flet Environment Diagnostics ===[/bold cyan]\n")

        # Step-by-step checks
        flet_version = self.check_flet_version()
        python_version = self.check_python_version()
        os_info = self.check_os_info()
        flutter_status = self.check_flutter()

        console.print("\n[bold cyan]====================================[/bold cyan]\n")

        # Only show extra details in verbose mode
        if verbose:
            self.print_detailed_info()

    def check_flet_version(self) -> str:
        """Check and print Flet version."""
        with console.status("[bold white]Checking Flet version..."):
            flet_version = flet.version.version or "Unknown"
            console.print(f"[green]✔ Flet Version:[/green] {flet_version}")
        return flet_version

    def check_python_version(self) -> str:
        """Check and print Python version."""
        with console.status("[bold white]Checking Python version..."):
            python_version = sys.version
            console.print(f"[green]✔ Python Version:[/green] {python_version}")
        return python_version

    def check_os_info(self) -> str:
        """Check and print OS information."""
        with console.status("[bold white]Checking OS information..."):
            os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
            console.print(f"[green]✔ Operating System:[/green] {os_info}")
        return os_info

    def check_flutter(self) -> str:
        """Check if Flutter is installed and print status."""
        with console.status("[bold white]Checking Flutter status..."):
            if shutil.which("flutter"):
                flutter_status = self.run_command("flutter doctor")
            else:
                flutter_status = "[red]⚠ Flutter is not installed[/red]"
            console.print(f"[green]✔ Flutter Status:[/green] {flutter_status}")
        return flutter_status

    def check_permissions(self) -> str:
        """Check if the user has necessary permissions."""
        with console.status("[bold white]Checking user permissions..."):
            if os.name == "nt":
                is_admin = os.system("net session >nul 2>&1") == 0
            else:
                is_admin = os.geteuid() == 0

            permission_status = "[green]✔ User has administrative privileges[/green]" if is_admin else "[yellow]⚠ Running without admin/root privileges[/yellow]"
            console.print(permission_status)
        return permission_status

    def check_virtual_env(self) -> str:
        """Check if a Python virtual environment is active."""
        with console.status("[bold white]Checking Python virtual environment..."):
            venv = os.getenv("VIRTUAL_ENV")
            venv_status = f"[green]✔ Virtual Environment active:[/green] {venv}" if venv else "[yellow]⚠ No virtual environment detected[/yellow]"
            console.print(venv_status)
        return venv_status

    def run_command(self, command: str) -> str:
        """Helper function to run a command and return its output."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else f"[red]⚠ Error running {command}[/red]"
        except Exception as e:
            return f"[red]⚠ {str(e)}[/red]"

    def print_detailed_info(self) -> None:
        """Print additional details in verbose mode."""
        console.print("\n[cyan]=== Additional Debug Info ===[/cyan]\n")
        self.check_permissions()
        self.check_virtual_env()
        console.print("[cyan]Detailed check completed.[/cyan]\n")
