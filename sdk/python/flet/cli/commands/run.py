import argparse
from flet.cli.commands.base import BaseCommand


class Command(BaseCommand):
    """
    Run Flet app
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("script", type=str, help="path to a Python script")
        parser.add_argument(
            "-p",
            "--port",
            dest="port",
            type=int,
            default=None,
            help="custom TCP port to run Flet app on",
        )
        parser.add_argument(
            "-d",
            "--directory",
            dest="directory",
            action="store_true",
            default=False,
            help="watch script directory",
        )
        parser.add_argument(
            "-r",
            "--recursive",
            dest="recursive",
            action="store_true",
            default=False,
            help="watch script directory and all sub-directories recursively",
        )
        parser.add_argument(
            "-n",
            "--hidden",
            dest="hidden",
            action="store_true",
            default=False,
            help="application window is hidden on startup",
        )
        parser.add_argument(
            "-w",
            "--web",
            dest="web",
            action="store_true",
            default=False,
            help="open app in a web browser",
        )

    def handle(self, options: argparse.Namespace) -> None:
        print("RUN COMMAND", options)
