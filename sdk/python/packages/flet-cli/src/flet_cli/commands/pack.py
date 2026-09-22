import argparse
import gzip
import hashlib
import os
import re
import shutil
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

import flet_cli.__pyinstaller.config as hook_config
from flet.utils import is_linux, is_macos, is_windows
from flet_cli.commands.base import BaseCommand


class Command(BaseCommand):
    """
    Package a Flet application into a standalone desktop executable or app bundle
    using PyInstaller.

    Detailed usage guide: https://flet.dev/docs/publish/using-pyinstaller
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Register command-line options for desktop packaging via PyInstaller.

        Args:
            parser: Argument parser configured by the command runner.
        """

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
            "Supported formats: `.ico` (Windows), `.icns` (macOS) and `.png` "
            "(Linux, where it is written alongside the generated desktop "
            "entry rather than embedded in the executable)",
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
            help="Bundle identifier for the app. Used for macOS app "
            "packaging, and on Linux as the app's taskbar identity — match it "
            "with the `StartupWMClass` key of your desktop entry. Defaults on "
            "Linux to the executable's name.",
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

    def compress_flet_client_dir(self, temp_bin_dir: str, archive_name: str) -> None:
        """Compress the flet/ directory into an archive and remove the original.

        Args:
            temp_bin_dir: Path to the temporary directory containing the flet/
                subdirectory with client binaries.
            archive_name: Target archive filename. Uses zip for `.zip`
                extensions and gzipped tar for everything else.
        """
        from flet_cli.__pyinstaller.utils import normalize_tar_entry

        flet_dir = os.path.join(temp_bin_dir, "flet")
        if not os.path.isdir(flet_dir):
            return
        archive_path = os.path.join(temp_bin_dir, archive_name)
        # Fixed timestamps and sorted entries make the archive deterministic
        # for identical inputs, so the runtime cache fingerprint (and thus the
        # client cache directory) only changes when content actually changes.
        if archive_name.endswith(".zip"):  # windows
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(flet_dir):
                    dirs.sort()
                    for f in sorted(files):
                        full = os.path.join(root, f)
                        arcname = os.path.relpath(full, temp_bin_dir)
                        zi = zipfile.ZipInfo(
                            arcname.replace(os.sep, "/"),
                            date_time=(1980, 1, 1, 0, 0, 0),
                        )
                        zi.compress_type = zipfile.ZIP_DEFLATED
                        zi.external_attr = (os.stat(full).st_mode & 0xFFFF) << 16
                        with open(full, "rb") as src, zf.open(zi, "w") as dest:
                            shutil.copyfileobj(src, dest)
        else:
            with (
                open(archive_path, "wb") as raw,
                gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz,
                tarfile.open(fileobj=gz, mode="w") as tar,
            ):
                tar.add(flet_dir, arcname="flet", filter=normalize_tar_entry)
        shutil.rmtree(flet_dir)
        self.write_archive_fingerprint(archive_path)

    def write_archive_fingerprint(self, archive_path: str) -> None:
        """Write a `<archive>.sha256` sidecar holding `<hash> <size>`.

        `flet_desktop.ensure_client_cached()` uses it at runtime to key the
        client cache directory by content, so this patched client doesn't
        collide with the vanilla client or other apps' patched clients. The
        size lets the runtime detect a stale sidecar next to a replaced
        archive and re-hash instead of trusting it.

        Args:
            archive_path: Path of the client archive to fingerprint.
        """
        h = hashlib.sha256()
        with open(archive_path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                h.update(chunk)
        with open(archive_path + ".sha256", "w") as f:
            f.write(f"{h.hexdigest()} {os.path.getsize(archive_path)}")

    @staticmethod
    def resolve_linux_app_id(options) -> str:
        """
        The identity the packed app will report to the desktop.

        Must stay in step with the PyInstaller runtime hook, which reads a
        bundled `--bundle-id` when there is one and otherwise falls back to
        the executable's own name. The entry written here is useless if the
        two disagree, since `StartupWMClass` would then match nothing.

        Args:
            options: Parsed command-line options.

        Returns:
            The app id, for both `StartupWMClass` and `Icon`.
        """

        app_id = options.bundle_id or (options.name or Path(options.script).stem)
        return app_id.strip()

    @staticmethod
    def escape_desktop_exec(value: str) -> str:
        """
        Escape a path for the quoted `Exec` key of a desktop entry.

        The value crosses two layers: the entry file, where backslash is the
        escape character, and the shell-like parsing of `Exec`, where `"`,
        `` ` ``, `$` and `\\` are reserved inside double quotes. Escape for
        the inner layer first, then the outer one, so a path containing any
        of them still launches.

        Args:
            value: Absolute path to the executable.

        Returns:
            The value, ready to sit between double quotes.
        """

        value = re.sub(r"[\x00-\x1f]", " ", value)
        shell_escaped = re.sub(r'(["`$\\])', r"\\\1", value)
        entry_escaped = shell_escaped.replace("\\", "\\\\")
        # `%` introduces a field code, so a literal one has to be doubled or
        # the desktop silently drops it along with the character after it.
        return entry_escaped.replace("%", "%%")

    @staticmethod
    def escape_desktop_value(value: str) -> str:
        """
        Escape a string for a desktop entry value.

        Desktop entry values are a single line, and backslash is the escape
        character, so escape it first and then flatten every control
        character that would end the line early.

        Args:
            value: Raw value, such as a product name or description.

        Returns:
            The value, safe to write after `Key=`.
        """

        value = value.replace("\\", "\\\\")
        for ch in ("\r", "\n", "\t"):
            value = value.replace(ch, " ")
        return value.strip()

    def write_linux_desktop_entry(self, options, dist_dir: str, app_id: str) -> None:
        """
        Write a desktop entry, and the icon it names, next to the executable.

        The Linux desktop takes an app's launcher name and icon from an
        installed desktop entry, which it matches to the window through
        `StartupWMClass`. Getting that key to equal the app's identity is the
        part that is easy to get wrong and impossible to guess, so `flet pack`
        writes the file rather than describing it.

        Nothing is installed: the entry sits in the dist directory until the
        user copies it into place. Installing it here would change the user's
        application menu as a side effect of building, and leave an entry
        behind pointing at a binary that may since have moved.

        Args:
            options: Parsed command-line options.
            dist_dir: Directory PyInstaller wrote the executable into.
            app_id: The identity the app reports to the desktop.
        """

        # The runtime refuses an id containing a path separator, because GLib
        # would silently reduce it to its last segment. Refuse it here too,
        # rather than crash writing an entry into a directory that does not
        # exist and would not have matched anything anyway.
        # A path separator would make the filename a directory that does not
        # exist, and a control character would break the line it is written
        # on -- Icon= and StartupWMClass= interpolate this value raw.
        if not app_id or "/" in app_id or re.search(r"[\x00-\x1f]", app_id):
            print(
                f"Skipping the desktop entry: {app_id!r} is empty, or contains "
                "a path separator or a control character, none of which can be "
                "an app identity."
            )
            return

        exe_name = options.name or Path(options.script).stem
        # PyInstaller's COLLECT step puts a one-folder build's executable
        # inside a directory named after it, so `dist/<name>` is the folder
        # and `dist/<name>/<name>` is the thing to launch.
        exe_path = Path(dist_dir).joinpath(exe_name)
        if options.onedir:
            exe_path = exe_path.joinpath(exe_name)
        name = options.product_name or exe_name

        lines = [
            "[Desktop Entry]",
            "Type=Application",
            f"Name={self.escape_desktop_value(name)}",
        ]
        if options.file_description:
            lines.append(
                f"Comment={self.escape_desktop_value(options.file_description)}"
            )
        lines += [
            # Absolute, because the desktop resolves nothing against $PATH,
            # and quoted so a path containing spaces stays one argument.
            f'Exec="{self.escape_desktop_exec(str(exe_path))}"',
            f"Icon={app_id}",
            "Terminal=false",
            "Categories=Utility;",
            # The whole point: this is what ties the window to this entry.
            f"StartupWMClass={app_id}",
            "",
        ]
        entry_path = Path(dist_dir).joinpath(f"{app_id}.desktop")
        entry_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"Wrote desktop entry: {entry_path}")

        if options.icon:
            icon_src = Path(options.icon)
            if not icon_src.is_absolute():
                icon_src = Path(os.getcwd()).joinpath(icon_src)
            if icon_src.suffix.lower() != ".png":
                print(
                    f"Note: {icon_src.name} is not a PNG, so it was not copied "
                    "for the desktop entry. Linux icon themes want a .png."
                )
            elif icon_src.is_file():
                icon_dst = Path(dist_dir).joinpath(f"{app_id}.png")
                shutil.copyfile(icon_src, icon_dst)
                print(f"Wrote desktop entry icon: {icon_dst}")

    def handle(self, options: argparse.Namespace) -> None:
        """
        Package the app into a standalone desktop artifact.

        Args:
            options: Parsed command-line options.
        """

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

        # Set only on Linux with --bundle-id; the cleanup below reads it
        # either way, so it has to exist before anything can fail.
        identity_dir = None

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

            # The Linux taskbar identity is chosen here but applied at launch,
            # so carry it into the bundle for the runtime hook to read. Only
            # when asked for: without it the hook falls back to the
            # executable's name, which needs nothing bundled.
            if is_linux() and options.bundle_id:
                identity_dir = tempfile.mkdtemp()
                identity_file = Path(identity_dir).joinpath("flet_app_id")
                identity_file.write_text(options.bundle_id, encoding="utf-8")
                pyi_args.extend(["--add-data", f"{identity_file}{os.pathsep}."])
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
            if is_macos() and options.bundle_id:
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

                    # Compress the patched flet/ directory into flet-windows.zip
                    # so ensure_client_cached() finds it at runtime.
                    self.compress_flet_client_dir(
                        hook_config.temp_bin_dir, "flet-windows.zip"
                    )

                elif is_macos():
                    from flet_cli.__pyinstaller.macos_utils import (
                        assemble_app_bundle,
                        unpack_app_bundle,
                        update_flet_view_icon,
                        update_flet_view_version_info,
                    )

                    tar_path = os.path.join(
                        hook_config.temp_bin_dir, "flet-macos.tar.gz"
                    )

                    # Find the .app bundle: either unpack from tar.gz or
                    # locate an already-extracted bundle (GitHub releases cache).
                    app_path = None
                    if os.path.exists(tar_path):
                        app_path = unpack_app_bundle(tar_path)
                    else:
                        for entry in os.listdir(hook_config.temp_bin_dir):
                            if entry.endswith(".app"):
                                app_path = os.path.join(hook_config.temp_bin_dir, entry)
                                break

                    if not app_path:
                        print(
                            "Error: macOS app bundle not found in "
                            f"{hook_config.temp_bin_dir}. "
                            "Set FLET_VIEW_PATH to the directory "
                            "containing your Flet.app."
                        )
                        sys.exit(1)

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

                    # Compress the patched .app bundle back into flet-macos.tar.gz so
                    # ensure_client_cached() finds it at runtime.
                    assemble_app_bundle(app_path, tar_path)
                    self.write_archive_fingerprint(tar_path)

                    # Remove everything except the tar.gz and its fingerprint so
                    # PyInstaller doesn't try to process loose framework binaries.
                    for entry in os.listdir(hook_config.temp_bin_dir):
                        entry_path = os.path.join(hook_config.temp_bin_dir, entry)
                        if entry_path in (tar_path, tar_path + ".sha256"):
                            continue
                        if os.path.isdir(entry_path):
                            shutil.rmtree(entry_path, ignore_errors=True)
                        else:
                            os.remove(entry_path)

                elif is_linux():
                    from flet_desktop import get_artifact_filename

                    # Compress the flet/ directory into a tar.gz
                    # so ensure_client_cached() finds it at runtime.
                    self.compress_flet_client_dir(
                        hook_config.temp_bin_dir, get_artifact_filename()
                    )

            # run PyInstaller
            print("Running PyInstaller:", pyi_args)
            PyInstaller.__main__.run(pyi_args)

            # Written after the build, because the entry's Exec= needs the
            # path PyInstaller just produced.
            if is_linux():
                self.write_linux_desktop_entry(
                    options, dist_dir, self.resolve_linux_app_id(options)
                )

        except ImportError as e:
            print("Please install PyInstaller module to use flet pack command:", e)
            sys.exit(1)
        finally:
            # In `finally` because a failed build leaks these otherwise: the
            # only handler above catches ImportError, so anything PyInstaller
            # raises would skip the cleanup entirely.
            if hook_config.temp_bin_dir is not None and os.path.exists(
                hook_config.temp_bin_dir
            ):
                print("Deleting temp directory:", hook_config.temp_bin_dir)
                shutil.rmtree(hook_config.temp_bin_dir, ignore_errors=True)
            if identity_dir is not None:
                shutil.rmtree(identity_dir, ignore_errors=True)
