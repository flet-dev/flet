import argparse
import shutil
from pathlib import Path

from rich.console import Console
from rich.style import Style

from flet_cli.commands.base import BaseCommand

error_style = Style(color="red1", bold=True)
success_style = Style(color="green", bold=True)
console = Console(log_path=False)


class Command(BaseCommand):
    """
    Delete the build output directory of a Flet app.

    Removes the `build` directory (created by `flet build` and `flet debug`)
    located in the given app directory, including the Flutter bootstrap
    project, cached artifacts, and generated output.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Register command-line options for cleaning a project's build directory.

        Args:
            parser: Argument parser configured by the command runner.
        """

        parser.add_argument(
            "python_app_path",
            type=str,
            nargs="?",
            default=".",
            help="Path to a directory with a Flet Python program "
            "whose `build` directory should be deleted",
        )

    def handle(self, options: argparse.Namespace) -> None:
        """
        Delete the `build` directory of the specified Flet app.

        Args:
            options: Parsed command-line options.
        """

        verbose = options.verbose

        app_path = Path(options.python_app_path).resolve()
        if not app_path.is_dir():
            console.print(
                f"Path to Flet app does not exist or is not a directory: {app_path}",
                style=error_style,
            )
            exit(1)

        build_dir = app_path.joinpath("build")
        if not build_dir.exists():
            console.print(f"Nothing to clean: no `build` directory at {build_dir}.")
            return

        if verbose > 0:
            console.print(f"[cyan]Deleting[/cyan] {build_dir}")

        try:
            shutil.rmtree(build_dir)
        except OSError as e:
            console.print(
                f"Error deleting build directory {build_dir}: {e}",
                style=error_style,
            )
            exit(1)

        console.print(f"Removed build directory: {build_dir}", style=success_style)
