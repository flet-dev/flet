import argparse
import glob
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
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
        parser.add_argument(
            "--splash-color",
            dest="splash_color",
            help="background color of app splash screen on iOS, Android and web",
            required=False,
        )
        parser.add_argument(
            "--splash-dark-color",
            dest="splash_dark_color",
            help="background color in dark mode of app splash screen on iOS, Android and web",
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
        self.verbose = options.verbose
        template_name = "flet_build"
        template_data = {"template_name": template_name}

        python_app_path = Path(options.python_app_path).resolve()

        self.flutter_dir = Path(tempfile.gettempdir()).joinpath(
            f"flet_flutter_build_{random_string(10)}"
        )

        if self.verbose > 0:
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

        # load pubspec.yaml
        pubspec_path = str(self.flutter_dir.joinpath("pubspec.yaml"))
        with open(pubspec_path) as f:
            pubspec = yaml.safe_load(f)

        # copy icons to `flutter_dir`
        print("Customizing app icons and splash images...", end="")
        assets_path = python_app_path.joinpath("assets")
        if assets_path.exists():
            images_dir = "images"
            images_path = self.flutter_dir.joinpath(images_dir)
            images_path.mkdir(exist_ok=True)

            def fallback_image(yaml_path: str, images: list):
                d = pubspec
                pp = yaml_path.split("/")
                for p in pp[:-1]:
                    d = d[p]
                for image in images:
                    if image:
                        d[pp[-1]] = f"{images_dir}/{image}"
                        return

            # copy icons
            default_icon = self.copy_icon_image(assets_path, images_path, "icon")
            ios_icon = self.copy_icon_image(assets_path, images_path, "icon_ios")
            android_icon = self.copy_icon_image(
                assets_path, images_path, "icon_android"
            )
            web_icon = self.copy_icon_image(assets_path, images_path, "icon_web")
            windows_icon = self.copy_icon_image(
                assets_path, images_path, "icon_windows"
            )
            macos_icon = self.copy_icon_image(assets_path, images_path, "icon_macos")

            fallback_image("flutter_launcher_icons/image_path", [default_icon])
            fallback_image(
                "flutter_launcher_icons/image_path_ios", [ios_icon, default_icon]
            )
            fallback_image(
                "flutter_launcher_icons/image_path_android",
                [android_icon, default_icon],
            )
            fallback_image(
                "flutter_launcher_icons/web/image_path", [web_icon, default_icon]
            )
            fallback_image(
                "flutter_launcher_icons/windows/image_path",
                [windows_icon, default_icon],
            )
            fallback_image(
                "flutter_launcher_icons/macos/image_path", [macos_icon, default_icon]
            )

            # copy splash images
            default_splash = self.copy_icon_image(assets_path, images_path, "splash")
            default_dark_splash = self.copy_icon_image(
                assets_path, images_path, "splash_dark"
            )
            ios_splash = self.copy_icon_image(assets_path, images_path, "splash_ios")
            ios_dark_splash = self.copy_icon_image(
                assets_path, images_path, "splash_dark_ios"
            )
            android_splash = self.copy_icon_image(
                assets_path, images_path, "splash_android"
            )
            android_dark_splash = self.copy_icon_image(
                assets_path, images_path, "splash_dark_android"
            )
            web_splash = self.copy_icon_image(assets_path, images_path, "splash_web")
            web_dark_splash = self.copy_icon_image(
                assets_path, images_path, "splash_dark_web"
            )
            fallback_image(
                "flutter_native_splash/image",
                [default_splash, default_icon],
            )
            fallback_image(
                "flutter_native_splash/image_dark",
                [default_dark_splash, default_splash, default_icon],
            )
            fallback_image(
                "flutter_native_splash/image_ios",
                [ios_splash, default_splash, default_icon],
            )
            fallback_image(
                "flutter_native_splash/image_dark_ios",
                [
                    ios_dark_splash,
                    default_dark_splash,
                    ios_splash,
                    default_splash,
                    default_icon,
                ],
            )
            fallback_image(
                "flutter_native_splash/image_android",
                [android_splash, default_splash, default_icon],
            )
            fallback_image(
                "flutter_native_splash/android_12/image",
                [android_splash, default_splash, default_icon],
            )
            fallback_image(
                "flutter_native_splash/image_dark_android",
                [
                    android_dark_splash,
                    default_dark_splash,
                    android_splash,
                    default_splash,
                    default_icon,
                ],
            )
            fallback_image(
                "flutter_native_splash/android_12/image_dark",
                [
                    android_dark_splash,
                    default_dark_splash,
                    android_splash,
                    default_splash,
                    default_icon,
                ],
            )
            fallback_image(
                "flutter_native_splash/image_web",
                [web_splash, default_splash, default_icon],
            )
            fallback_image(
                "flutter_native_splash/image_dark_web",
                [
                    web_dark_splash,
                    default_dark_splash,
                    web_splash,
                    default_splash,
                    default_icon,
                ],
            )

            # splash colors
            if options.splash_color:
                pubspec["flutter_native_splash"]["color"] = options.splash_color
                pubspec["flutter_native_splash"]["android_12"][
                    "color"
                ] = options.splash_color
            if options.splash_dark_color:
                pubspec["flutter_native_splash"][
                    "color_dark"
                ] = options.splash_dark_color
                pubspec["flutter_native_splash"]["android_12"][
                    "color_dark"
                ] = options.splash_dark_color

        print("[spring_green3]OK[/spring_green3]")

        # save pubspec.yaml
        with open(pubspec_path, "w") as f:
            yaml.dump(pubspec, f)

        # generate icons
        print("Generating app icons...", end="")
        icons_result = subprocess.run(
            [dart_exe, "run", "flutter_launcher_icons"],
            cwd=str(self.flutter_dir),
            capture_output=self.verbose < 2,
            text=True,
        )
        if icons_result.returncode != 0:
            if icons_result.stdout:
                print(icons_result.stdout)
            if icons_result.stderr:
                print(icons_result.stderr)
            self.cleanup()

        print("[spring_green3]OK[/spring_green3]")

        # generate splash
        print("Generating splash screens...", end="")
        splash_result = subprocess.run(
            [dart_exe, "run", "flutter_native_splash:create"],
            cwd=str(self.flutter_dir),
            capture_output=self.verbose < 2,
            text=True,
        )
        if splash_result.returncode != 0:
            if splash_result.stdout:
                print(splash_result.stdout)
            if splash_result.stderr:
                print(splash_result.stderr)
            self.cleanup()

        print("[spring_green3]OK[/spring_green3]")

        # package Python app
        print(f"Packaging Python app...", end="")
        package_args = [
            dart_exe,
            "run",
            "serious_python:main",
            "package",
            str(python_app_path),
        ]
        if platform == "web":
            package_args.extend(
                [
                    "--web",
                    "--dep-mappings",
                    "flet=flet-pyodide",
                    "--req-deps",
                    "flet-pyodide",
                    "--platform",
                    "emscripten_3_1_45_wasm32",
                ]
            )
        else:
            if platform in ["apk", "aab", "ipa"]:
                package_args.extend(
                    [
                        "--mobile",
                    ]
                )
            package_args.extend(
                [
                    "--dep-mappings",
                    "flet=flet-embed",
                    "--req-deps",
                    "flet-embed",
                ]
            )
        package_result = subprocess.run(
            package_args,
            cwd=str(self.flutter_dir),
            capture_output=self.verbose < 2,
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
            capture_output=self.verbose < 2,
            text=True,
        )

        if build_result.returncode != 0:
            if build_result.stdout:
                print(build_result.stdout)
            if build_result.stderr:
                print(build_result.stderr)
            self.cleanup()
        print("[spring_green3]OK[/spring_green3]")

        print(self.flutter_dir)
        return

        # copy build results to `out_dir`

        self.cleanup()

    def copy_icon_image(self, src_path: Path, dest_path: Path, image_name: str):
        images = glob.glob(str(src_path.joinpath(f"{image_name}.*")))
        if len(images) > 0:
            if self.verbose > 0:
                print(f"Copying {images[0]} to {dest_path}")
            shutil.copy(images[0], dest_path)
            return Path(images[0]).name
        return None

    def cleanup(self):
        print("Cleaning up...", end="")
        shutil.rmtree(str(self.flutter_dir), ignore_errors=False, onerror=None)
        print("[spring_green3]OK[/spring_green3]")
        sys.exit(1)
