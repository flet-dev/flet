import argparse
import platform
import sys
import shutil
import subprocess
from rich.console import Console
from rich.style import Style

import flet.version
from flet.utils import cleanup_path
from flet_cli.commands.base import BaseCommand

# Rich console setup for styled output
error_style = Style(color="red1", bold=True)
console = Console(log_path=False)


class Command(BaseCommand):
    """
    Check the health of your Flet environment.
    """

    

    def handle(self, options: argparse.Namespace) -> None:
        """Handle the 'doctor' command."""
        verbose = options.verbose

        # Gather system information
        flet_version = flet.version.version or "Unknown"
        python_version = sys.version
        os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
        flutter_status = self.check_flutter()

        # Print out the information
        console.print("\n=== Flet Environment Diagnostics ===\n")
        console.print(f"Flet Version: {flet_version}")
        console.print(f"Python Version: {python_version}")
        console.print(f"Operating System: {os_info}")
        console.print(f"Flutter Status:\n{flutter_status}\n")
        console.print("====================================\n")

        if verbose:
            self.print_detailed_info()

    def check_flutter(self) -> str:
        """Check if Flutter is installed and provide status."""
        if shutil.which("flutter"):
            return self.run_command("flutter doctor")
        return "Flutter is not installed"

    def run_command(self, command: str) -> str:
        """Helper function to run a command and return its output."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else f"Error running {command}"
        except Exception as e:
            return str(e)

    def print_detailed_info(self) -> None:
        """Print detailed information if verbose flag is set."""
        console.print("[cyan]Additional Info:[/cyan]")
        console.print(f"[green]Flet Version:[/green] {flet.version.version}")
        console.print(f"[green]Python Version:[/green] {sys.version}")
        console.print(f"[green]Operating System:[/green] {platform.system()} {platform.release()}")
        console.print(f"[green]Flutter Status:[/green] {self.check_flutter()}")

        console.print("Detailed check completed.\n")
