import argparse
import platform
import sys

from rich.console import Console

import flet.version
from flet_cli.commands.base import BaseCommand

# Rich console setup for styled output
console = Console(log_path=False)


class Command(BaseCommand):
    """
    Get information about the system and environment setup.
    """

    def handle(self, options: argparse.Namespace) -> None:
        """Handle the 'doctor' command."""
        verbose = options.verbose

        os_name = platform.system()
        if os_name == "Darwin":
            os_name = "macOS"
            os_version = platform.mac_ver()[0]
        else:
            os_version = platform.release()

        arch = platform.machine()
        console.print(
            f"Flet {flet.version.flet_version} on {os_name} {os_version} ({arch})"
            if arch
            else f"Flet {flet.version.flet_version} on {os_name} {os_version}"
        )

        console.print(f"Python {platform.python_version()} ({sys.executable})")

        # TODO: output Flutter version, if installed
