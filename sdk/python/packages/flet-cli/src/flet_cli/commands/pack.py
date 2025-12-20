import argparse
import os
import shutil
import sys
from pathlib import Path

import flet_cli.__pyinstaller.config as hook_config
from flet.utils import is_macos, is_windows
from flet_cli.commands.base import BaseCommand


class Command(BaseCommand):
    """
    Package a Flet application into a standalone desktop executable or app bundle
    using PyInstaller.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "script",
            type=str,
            help="Path to the Python script that launches your Flet app",
        )
        parser.add_argument(
            "-i",
            "--icon",
            dest="icon",
            help="Path to an icon file for your executable or app bundle. "
            "Supported formats: `.ico` (Windows), `.png` (Linux) and `.icns` (macOS)",
        )
        parser.add_argument(
            "-n",
            "--name",
            dest="name",
            help="Name for the generated executable (Windows) or app bundle (macOS)",
        )
        parser.add_argument(
            "-D",
            "--onedir",
            dest="onedir",
            action="store_true",
            default=False,
            help="Create a one-folder bundle instead of a "
            "single-file executable (Windows only)",
        )
        parser.add_argument(
            "--distpath",
            dest="distpath",
            default="dist",
            help="Directory where the packaged app will be placed",
        )
        parser.add_argument(
            "--add-data",
            dest="add_data",
            action="append",
            nargs="*",
            help="Add additional non-binary files or folders to the bundle. "
            "Accepts one or more arguments in the form `source:destination`",
        )
        parser.add_argument(
            "--add-binary",
            dest="add_binary",
            action="append",
            nargs="*",
            help="Additional binary files to be added to the executable."
            "Format: `source:destination[:platform]`",
        )
        parser.add_argument(
            "--hidden-import",
            dest="hidden_import",
            action="append",
            nargs="*",
            help="Add Python modules that are dynamically imported "
            "and not detected by static analysis",
        )
        parser.add_argument(
            "--product-name",
            dest="product_name",
            help="Product name to be embedded in the "
            "executable (Windows) or bundle (macOS)",
        )
        parser.add_argument(
            "--file-description",
            dest="file_description",
            help="File description to embed in the executable (Windows)",
        )
        parser.add_argument(
            "--product-version",
            dest="product_version",
            help="Product version for the executable (Windows) or bundle (macOS)",
        )
        parser.add_argument(
            "--file-version",
            dest="file_version",
            help="File version for the executable in `n.n.n.n` format (Windows only)",
        )
        parser.add_argument(
            "--company-name",
            dest="company_name",
            help="Company name metadata for the Windows executable",
        )
        parser.add_argument(
            "--copyright",
            dest="copyright",
            help="Copyright string embedded in the "
            "executable (Windows) or bundle (macOS)",
        )
        parser.add_argument(
            "--codesign-identity",
            dest="codesign_identity",
            help="Code signing identity to sign the app bundle (macOS only)",
        )
        parser.add_argument(
            "--bundle-id",
            dest="bundle_id",
            help="Bundle identifier used for macOS app packaging",
        )
        parser.add_argument(
            "--debug-console",
            dest="debug_console",
            help="Show python debug console window (ensure correct DEBUG level). "
            "Useful for troubleshooting runtime errors",
        )
        parser.add_argument(
            "--uac-admin",
            dest="uac_admin",
            default=False,
            action="store_true",
            help="Request elevated (admin) permissions on application "
            "start (Windows only). Adds a UAC manifest to the executable",
        )
        parser.add_argument(
            "--pyinstaller-build-args",
            dest="pyinstaller_build_args",
            action="append",
            nargs="*",
            help="Additional raw arguments to the underlying pyinstaller build command",
        )
        parser.add_argument(
            "-y",
            "--yes",
            dest="non_interactive",
            default=False,
            action="store_true",
            help="Enable non-interactive mode. All prompts will be skipped",
        )

    def handle(self, options: argparse.Namespace) -> None:
        from flet.utils.pip import ensure_flet_desktop_package_installed

        ensure_flet_desktop_package_installed()

        is_dir_not_empty = lambda dir: os.path.isdir(dir) and len(os.listdir(dir)) != 0  # noqa: E731

        # delete "build" directory
        build_dir = os.path.join(os.getcwd(), "build")
        if is_dir_not_empty(build_dir):
            if options.non_interactive:
                shutil.rmtree(build_dir, ignore_errors=True)
            else:
                delete_dir_prompt = input(
                    'Do you want to delete "build" directory? (y/n) '
                )
                if delete_dir_prompt.lower() != "n":
                    shutil.rmtree(build_dir, ignore_errors=True)
                else:
                    print('Failing... "build" directory must be empty to proceed.')
                    exit(1)

        # delete "dist" directory or DISTPATH directory
        # if --distpath cli option is specified
        if options.distpath:
            dist_dir = os.path.join(os.getcwd(), options.distpath)
        else:
            dist_dir = os.path.join(os.getcwd(), "dist")

        if is_dir_not_empty(dist_dir):
            if options.non_interactive:
                shutil.rmtree(dist_dir, ignore_errors=True)
            else:
                delete_dir_prompt = input(
                    f'Do you want to delete "{os.path.basename(dist_dir)}" '
                    f"directory? (y/n) "
                )
                if delete_dir_prompt.lower() != "n":
                    shutil.rmtree(dist_dir, ignore_errors=True)
                else:
                    print(
                        f'Failing... DISTPATH "{os.path.basename(dist_dir)}" directory '
                        f"must be empty to proceed."
                    )
                    exit(1)

        try:
            import PyInstaller.__main__

            from flet_cli.__pyinstaller.utils import copy_flet_bin

            pyi_args = [options.script, "--noconfirm"]
            if not options.debug_console:
                pyi_args.extend(["--noconsole"])
            if options.icon:
                pyi_args.extend(["--icon", options.icon])
            if options.name:
                pyi_args.extend(["--name", options.name])
            if options.distpath:
                pyi_args.extend(["--distpath", options.distpath])
            if options.add_data:
                for add_data_arr in options.add_data:
                    for add_data_item in add_data_arr:
                        pyi_args.extend(["--add-data", add_data_item])
            if options.add_binary:
                for add_binary_arr in options.add_binary:
                    for add_binary_item in add_binary_arr:
                        pyi_args.extend(["--add-binary", add_binary_item])
            if options.hidden_import:
                for hidden_import_arr in options.hidden_import:
                    for hidden_import_item in hidden_import_arr:
                        pyi_args.extend(["--hidden-import", hidden_import_item])
            if options.codesign_identity:
                pyi_args.extend(["--codesign-identity", options.codesign_identity])
            if options.bundle_id:
                pyi_args.extend(["--osx-bundle-identifier", options.bundle_id])
            if options.uac_admin:
                if is_macos():
                    print("--uac-admin options is not supported on macOS.")
                    sys.exit(1)
                pyi_args.append("--uac-admin")
            if options.onedir:
                if is_macos():
                    print("--onedir options is not supported on macOS.")
                    sys.exit(1)
                pyi_args.append("--onedir")
            else:
                pyi_args.append("--onefile")

            if options.pyinstaller_build_args:
                for pyinstaller_build_arg_arr in options.pyinstaller_build_args:
                    pyi_args.extend(pyinstaller_build_arg_arr)

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
                    from flet_cli.__pyinstaller.win_utils import (
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
                    from flet_cli.__pyinstaller.macos_utils import (
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
            sys.exit(1)
