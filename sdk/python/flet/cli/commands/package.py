import argparse

import flet.__pyinstaller.config as hook_config
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
        parser.add_argument(
            "-i",
            "--icon",
            dest="icon",
            help="path to an icon file (.ico, .png, .icns)",
        )
        parser.add_argument(
            "-n",
            "--name",
            dest="name",
            help="name for the generated executable",
        )

    def handle(self, options: argparse.Namespace) -> None:

        try:
            import PyInstaller.__main__

            pyi_args = [options.script, "--noconsole", "--noconfirm"]
            if options.icon:
                pyi_args.extend(["--icon", options.icon])
                hook_config.icon_file = options.icon
            if options.name:
                pyi_args.extend(["--name", options.name])
            PyInstaller.__main__.run(pyi_args)
        except ImportError:
            print("Please install PyInstaller module to use flet package command.")
            exit(1)
