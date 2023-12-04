import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from flet.cli.commands.base import BaseCommand
from flet_core.utils import random_string, slugify
from flet_runtime.utils import copy_tree, is_windows
from rich import print


class Command(BaseCommand):
    """
    Build an executable app or install bundle.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)

        self.platforms = {
            "windows": {
                "build_command": "windows",
                "status_text": "Windows app",
                "output": "build/windows/x64/runner/Release",
                "dist": "windows",
            },
            "macos": {
                "build_command": "macos",
                "status_text": "macOS bundle",
                "output": "build/macos/Build/Products/Release",
                "dist": "macos",
            },
            "linux": {
                "build_command": "linux",
                "status_text": "app for Linux",
                "output": "build/linux/x64/release/bundle",
                "dist": "linux",
            },
            "web": {
                "build_command": "web",
                "status_text": "web app",
                "output": "build/web",
                "dist": "web",
            },
            "apk": {
                "build_command": "apk",
                "status_text": ".apk for Android",
                "output": "build/app/outputs/flutter-apk",
                "dist": "apk",
            },
            "aab": {
                "build_command": "appbundle",
                "status_text": ".aab bundle for Android",
                "output": "build/app/outputs/bundle/release",
                "dist": "aab",
            },
            "ipa": {
                "build_command": "ipa",
                "status_text": ".ipa bundle for iOS",
                "output": "build/app/outputs/bundle/release",
                "dist": "ipa",
            },
        }

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "platform",
            type=str,
            choices=["macos", "linux", "windows", "web", "apk", "aab", "ipa"],
            help="platform to build against",
        )
        parser.add_argument(
            "python_app_path",
            type=str,
            nargs="?",
            default=".",
            help="path to a directory with a Python program",
        )
        parser.add_argument(
            "-o",
            "--output_dir",
            dest="output_dir",
            help="where to put built app (default: ./build)",
            required=False,
        )
        parser.add_argument(
            "--project-name",
            dest="project_name",
            help="project name for executable or bundle",
            required=False,
        )
        parser.add_argument(
            "--description",
            dest="description",
            help="the description to use for executable or bundle",
            required=False,
        )

    def handle(self, options: argparse.Namespace) -> None:
        from cookiecutter.main import cookiecutter

        flutter_exe = "flutter.exe" if is_windows() else "flutter"
        dart_exe = "dart.exe" if is_windows() else "dart"

        # check if `flutter` executable is available in the path
        if not shutil.which(flutter_exe):
            print("`flutter` command is not available in PATH. Install Flutter SDK.")
            sys.exit(1)

        # check if `dart` executable is available in the path
        if not shutil.which(dart_exe):
            print("`dart` command is not available in PATH. Install Flutter SDK.")
            sys.exit(1)

        platform = options.platform.lower()
        verbose = options.verbose
        template_name = "flet_build"
        template_data = {"template_name": template_name}

        python_app_path = Path(options.python_app_path).resolve()

        self.flutter_dir = Path(tempfile.gettempdir()).joinpath(
            f"flet_flutter_build_{random_string(10)}"
        )

        if verbose > 0:
            print("Flutter bootstrap directory:", self.flutter_dir)
        self.flutter_dir.mkdir(exist_ok=True)

        out_dir = (
            Path(options.output_dir).resolve()
            if options.output_dir
            else python_app_path.joinpath("build").joinpath(
                self.platforms[platform]["dist"]
            )
        )

        template_data["out_dir"] = self.flutter_dir.name

        project_name = slugify(
            options.project_name if options.project_name else python_app_path.name
        ).replace("-", "_")
        template_data["project_name"] = project_name

        if options.description is not None:
            template_data["description"] = options.description

        # create Flutter project from a template
        print("Creating Flutter bootstrap project...", end="")
        cookiecutter(
            f"gh:flet-dev/flet-app-templates",
            directory=template_name,
            output_dir=str(self.flutter_dir.parent),
            no_input=True,
            overwrite_if_exists=True,
            extra_context=template_data,
        )
        print("[spring_green3]OK[/spring_green3]")

        # copy icons to `flutter_dir`
        assets_path = python_app_path.joinpath("assets")
        if assets_path.exists():
            # copy icons
            copy_tree(str(assets_path), self.flutter_dir.joinpath("images"))

        # convert icons

        # package Python app
        print(f"Packaging Python app...", end="")
        package_result = subprocess.run(
            [dart_exe, "run", "serious_python:main", "package", str(python_app_path)],
            cwd=str(self.flutter_dir),
            capture_output=verbose < 2,
            text=True,
        )

        if package_result.returncode != 0:
            if package_result.stdout:
                print(package_result.stdout)
            if package_result.stderr:
                print(package_result.stderr)
            self.cleanup()
        print("[spring_green3]OK[/spring_green3]")

        # run `flutter build`
        print(
            f"Building [cyan]{self.platforms[platform]['status_text']}[/cyan]...",
            end="",
        )
        build_result = subprocess.run(
            [flutter_exe, "build", self.platforms[platform]["build_command"]],
            cwd=str(self.flutter_dir),
            capture_output=verbose < 2,
            text=True,
        )

        if build_result.returncode != 0:
            if build_result.stdout:
                print(build_result.stdout)
            if build_result.stderr:
                print(build_result.stderr)
            self.cleanup()
        print("[spring_green3]OK[/spring_green3]")

        # copy build results to `out_dir`

        self.cleanup()

    def cleanup(self):
        print("Cleaning up...", end="")
        shutil.rmtree(str(self.flutter_dir), ignore_errors=False, onerror=None)
        print("[spring_green3]OK[/spring_green3]")
        sys.exit(1)
