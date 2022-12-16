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
        parser.add_argument(
            "--add-data",
            dest="add_data",
            help="additional non-binary files or folders to be added to the executable",
        )
        parser.add_argument(
            "--product-name",
            dest="product_name",
            help="executable product name",
        )
        parser.add_argument(
            "--file-description",
            dest="file_description",
            help="executable file description",
        )
        parser.add_argument(
            "--product-version",
            dest="product_version",
            help="executable product version (any string)",
        )
        parser.add_argument(
            "--file-version",
            dest="file_version",
            help="executable file version (n.n.n.n)",
        )
        parser.add_argument(
            "--company-name",
            dest="company_name",
            help="executable companyname",
        )
        parser.add_argument(
            "--copyright",
            dest="copyright",
            help="executable copyright",
        )

    def handle(self, options: argparse.Namespace) -> None:

        try:
            import pefile
            import PyInstaller.__main__
            from PyInstaller.compat import win32api
            from PyInstaller.utils.win32.versioninfo import (
                FixedFileInfo,
                StringFileInfo,
                StringStruct,
                StringTable,
                VarFileInfo,
                VarStruct,
                VSVersionInfo,
                decode,
            )

            pyi_args = [options.script, "--noconsole", "--noconfirm"]
            if options.icon:
                pyi_args.extend(["--icon", options.icon])
                hook_config.icon_file = options.icon
            if options.name:
                pyi_args.extend(["--name", options.name])
            if options.add_data:
                pyi_args.extend(["--add-data", options.add_data])
            PyInstaller.__main__.run(pyi_args)
        except ImportError:
            print("Please install PyInstaller module to use flet package command.")
            exit(1)
