import argparse
import os
import shutil
from pathlib import Path

import flet.__pyinstaller.config as hook_config
from flet.cli.commands.base import BaseCommand
from flet.utils import is_macos, is_windows


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

        # delete "build" directory
        build_dir = Path(os.getcwd()).joinpath("build")
        if build_dir.exists():
            shutil.rmtree(str(build_dir), ignore_errors=True)

        # delete "dist" directory
        dist_dir = Path(os.getcwd()).joinpath("dist")
        if dist_dir.exists():
            shutil.rmtree(str(dist_dir), ignore_errors=True)

        try:
            import PyInstaller.__main__

            from flet.__pyinstaller.utils import copy_flet_bin

            pyi_args = [options.script, "--noconsole", "--noconfirm"]
            if options.onefile:
                pyi_args.extend(["--onefile"])
            if options.icon:
                pyi_args.extend(["--icon", options.icon])
            if options.name:
                pyi_args.extend(["--name", options.name])
            if options.add_data:
                pyi_args.extend(["--add-data", options.add_data])

            # copy "bin"
            hook_config.temp_bin_dir = copy_flet_bin()

            if hook_config.temp_bin_dir is not None:
                if is_windows():

                    from flet.__pyinstaller.win_utils import (
                        update_flet_view_icon,
                        update_flet_view_version_info,
                    )

                    exe_path = Path(hook_config.temp_bin_dir).joinpath(
                        "flet", "flet.exe"
                    )
                    if os.path.exists(exe_path):
                        # icon
                        if options.icon:
                            icon_path = options.icon
                            if not Path(icon_path).is_absolute():
                                icon_path = Path(os.getcwd()).joinpath(icon_path)
                            update_flet_view_icon(str(exe_path), icon_path)

                        # version info
                        version_info_path = update_flet_view_version_info(
                            exe_path=exe_path,
                            product_name=options.product_name,
                            file_description=options.file_description,
                            product_version=options.product_version,
                            file_version=options.file_version,
                            company_name=options.company_name,
                            copyright=options.copyright,
                        )

                        pyi_args.extend(["--version-file", version_info_path])

                elif is_macos():
                    from flet.__pyinstaller.macos_utils import update_flet_view_icon

                    tar_path = Path(hook_config.temp_bin_dir).joinpath(
                        "flet-macos-amd64.tar.gz"
                    )
                    if tar_path.exists():
                        # icon
                        if options.icon:
                            icon_path = options.icon
                            if not Path(icon_path).is_absolute():
                                icon_path = Path(os.getcwd()).joinpath(icon_path)
                            update_flet_view_icon(str(tar_path), icon_path)

            # run PyInstaller!
            PyInstaller.__main__.run(pyi_args)

            # cleanup
            if hook_config.temp_bin_dir is not None and os.path.exists(
                hook_config.temp_bin_dir
            ):
                print("Deleting temp directory:", hook_config.temp_bin_dir)
                shutil.rmtree(hook_config.temp_bin_dir, ignore_errors=True)
        except ImportError:
            print("Please install PyInstaller module to use flet package command.")
            exit(1)
