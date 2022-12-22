import argparse

from flet.cli.commands.base import BaseCommand


class Command(BaseCommand):
    """
    Package Flet app to a standalone bundle
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("script", type=str, help="path to a Python script")
        parser.add_argument(
            "-F",
            "--onefile",
            dest="onefile",
            action="store_true",
            default=False,
            help="create a one-file bundled executable",
        )

    def handle(self, options: argparse.Namespace) -> None:
        # print("BUILD COMMAND", options)
        raise NotImplementedError("Build command is not implemented yet.")
