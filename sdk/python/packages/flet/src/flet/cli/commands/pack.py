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
            "-i",
            "--icon",
            dest="icon",
            help="path to an icon file (.ico, .png, .icns)",
        )
        parser.add_argument(
            "-n",
            "--name",
            dest="name",
            help="name for the generated executable (Windows) or app bundle (macOS)",
        )
        parser.add_argument(
            "-D",
            "--onedir",
            dest="onedir",
            action="store_true",
            default=False,
            help="create a one-folder bundle containing an executable (Windows)",
        )
        parser.add_argument(
            "--add-data",
            dest="add_data",
            action="append",
            nargs="*",
            help="additional non-binary files or folders to be added to the executable",
        )
        parser.add_argument(
            "--hidden-import",
            dest="hidden_import",
            action="append",
            nargs="*",
            help="add an import not visible in the code of the script(s)",
        )
        parser.add_argument(
            "--product-name",
            dest="product_name",
            help="executable product name (Windows) or bundle name (macOS)",
        )
        parser.add_argument(
            "--file-description",
            dest="file_description",
            help="executable file description (Windows)",
        )
        parser.add_argument(
            "--product-version",
            dest="product_version",
            help="executable product version (Windows) or bundle version (macOS)",
        )
        parser.add_argument(
            "--file-version",
            dest="file_version",
            help="executable file version, n.n.n.n (Windows)",
        )
        parser.add_argument(
            "--company-name",
            dest="company_name",
            help="executable company name (Windows)",
        )
        parser.add_argument(
            "--copyright",
            dest="copyright",
            help="executable (Windows) or bundle (macOS) copyright",
        )
        parser.add_argument(
            "--bundle-id",
            dest="bundle_id",
            help="bundle identifier (macOS)",
        )

    def handle(self, options: argparse.Namespace) -> None:

        # delete "build" directory
        build_dir = os.path.join(os.getcwd(), "build")
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir, ignore_errors=True)

        # delete "dist" directory
        dist_dir = os.path.join(os.getcwd(), "dist")
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir, ignore_errors=True)

        try:
            import PyInstaller.__main__

            from flet.__pyinstaller.utils import copy_flet_bin

            pyi_args = [options.script, "--noconsole", "--noconfirm"]
            if options.icon:
                pyi_args.extend(["--icon", options.icon])
            if options.name:
                pyi_args.extend(["--name", options.name])
            if options.add_data:
                for add_data_arr in options.add_data:
                    for add_data_item in add_data_arr:
                        pyi_args.extend(["--add-data", add_data_item])
            if options.hidden_import:
                for hidden_import_arr in options.hidden_import:
                    for hidden_import_item in hidden_import_arr:
                        pyi_args.extend(["--hidden-import", hidden_import_item])
            if options.bundle_id:
                pyi_args.extend(["--osx-bundle-identifier", options.bundle_id])
            if options.onedir:
                if is_macos():
                    print("--onedir options is not supported on macOS.")
                    exit(1)
                pyi_args.append("--onedir")
            else:
                pyi_args.append("--onefile")

            # copy "bin"
            hook_config.temp_bin_dir = copy_flet_bin()

            if hook_config.temp_bin_dir is not None:

                # delete fletd/fletd.exe
                fletd_path = os.path.join(
                    hook_config.temp_bin_dir, "fletd.exe" if is_windows() else "fletd"
                )
                if os.path.exists(fletd_path):
                    os.remove(fletd_path)

                if is_windows():

                    from flet.__pyinstaller.win_utils import (
                        update_flet_view_icon,
                        update_flet_view_version_info,
                    )

                    exe_path = os.path.join(
                        hook_config.temp_bin_dir, "flet", "flet.exe"
                    )
                    if os.path.exists(exe_path):
                        # icon
                        if options.icon:
                            icon_path = options.icon
                            if not Path(icon_path).is_absolute():
                                icon_path = str(Path(os.getcwd()).joinpath(icon_path))
                            update_flet_view_icon(exe_path, icon_path)

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
                    from flet.__pyinstaller.macos_utils import (
                        assemble_app_bundle,
                        unpack_app_bundle,
                        update_flet_view_icon,
                        update_flet_view_version_info,
                    )

                    tar_path = os.path.join(
                        hook_config.temp_bin_dir, "flet-macos-amd64.tar.gz"
                    )
                    if os.path.exists(tar_path):

                        # unpack
                        app_path = unpack_app_bundle(tar_path)

                        # icon
                        if options.icon:
                            icon_path = options.icon
                            if not Path(icon_path).is_absolute():
                                icon_path = str(Path(os.getcwd()).joinpath(icon_path))
                            update_flet_view_icon(app_path, icon_path)

                        # version info
                        app_path = update_flet_view_version_info(
                            app_path=app_path,
                            bundle_id=options.bundle_id,
                            product_name=options.product_name,
                            product_version=options.product_version,
                            copyright=options.copyright,
                        )

                        # assemble
                        assemble_app_bundle(app_path, tar_path)

            # run PyInstaller!
            print("Running PyInstaller:", pyi_args)
            PyInstaller.__main__.run(pyi_args)

            # cleanup
            if hook_config.temp_bin_dir is not None and os.path.exists(
                hook_config.temp_bin_dir
            ):
                print("Deleting temp directory:", hook_config.temp_bin_dir)
                shutil.rmtree(hook_config.temp_bin_dir, ignore_errors=True)
        except ImportError as e:
            print("Please install PyInstaller module to use flet pack command:", e)
            exit(1)
