import argparse
import glob
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Optional

import flet.version
import yaml
from flet.cli.commands.base import BaseCommand
from flet_core.utils import random_string, slugify
from flet_runtime.utils import calculate_file_hash, copy_tree, is_windows
from packaging import version
from rich import print

if is_windows():
    from ctypes import windll

PYODIDE_ROOT_URL = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full"
DEFAULT_TEMPLATE_URL = "gh:flet-dev/flet-build-template"
MINIMAL_FLUTTER_VERSION = "3.19.0"


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
                "outputs": ["build/windows/x64/runner/Release/*"],
                "dist": "windows",
                "can_be_run_on": ["Windows"],
            },
            "macos": {
                "build_command": "macos",
                "status_text": "macOS bundle",
                "outputs": ["build/macos/Build/Products/Release/{product_name}.app"],
                "dist": "macos",
                "can_be_run_on": ["Darwin"],
            },
            "linux": {
                "build_command": "linux",
                "status_text": "app for Linux",
                "outputs": ["build/linux/{arch}/release/bundle/*"],
                "dist": "linux",
                "can_be_run_on": ["Linux"],
            },
            "web": {
                "build_command": "web",
                "status_text": "web app",
                "outputs": ["build/web/*"],
                "dist": "web",
                "can_be_run_on": ["Darwin", "Windows", "Linux"],
            },
            "apk": {
                "build_command": "apk",
                "status_text": ".apk for Android",
                "outputs": ["build/app/outputs/flutter-apk/*"],
                "dist": "apk",
                "can_be_run_on": ["Darwin", "Windows", "Linux"],
            },
            "aab": {
                "build_command": "appbundle",
                "status_text": ".aab bundle for Android",
                "outputs": ["build/app/outputs/bundle/release/*"],
                "dist": "aab",
                "can_be_run_on": ["Darwin", "Windows", "Linux"],
            },
            "ipa": {
                "build_command": "ipa",
                "status_text": ".ipa bundle for iOS",
                "outputs": ["build/ios/archive/*", "build/ios/ipa/*"],
                "dist": "ipa",
                "can_be_run_on": ["Darwin"],
            },
        }

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "target_platform",
            type=str,
            choices=["macos", "linux", "windows", "web", "apk", "aab", "ipa"],
            help="the type of a package or target platform to build",
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
            "--output",
            dest="output_dir",
            help="where to put resulting executable or bundle (default is <python_app_directory>/build/<target_platform>)",
            required=False,
        )
        parser.add_argument(
            "--project",
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
            "--product",
            dest="product_name",
            help="project display name that is shown in window titles and about app dialogs",
            required=False,
        )
        parser.add_argument(
            "--org",
            dest="org_name",
            help='org name in reverse domain name notation, e.g. "com.mycompany" - combined with project name and used as an iOS and Android bundle ID',
            required=False,
        )
        parser.add_argument(
            "--company",
            dest="company_name",
            help="company name to display in about app dialogs",
            required=False,
        )
        parser.add_argument(
            "--copyright",
            dest="copyright",
            help="copyright text to display in about app dialogs",
            required=False,
        )
        parser.add_argument(
            "--android-adaptive-icon-background",
            dest="android_adaptive_icon_background",
            help="the color which will be used to fill out the background of the adaptive icon",
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
        parser.add_argument(
            "--no-web-splash",
            dest="no_web_splash",
            action="store_true",
            default=False,
            help="disable web app splash screen",
        )
        parser.add_argument(
            "--no-ios-splash",
            dest="no_ios_splash",
            action="store_true",
            default=False,
            help="disable iOS app splash screen",
        )
        parser.add_argument(
            "--no-android-splash",
            dest="no_android_splash",
            action="store_true",
            default=False,
            help="disable Android app splash screen",
        )
        parser.add_argument(
            "--team",
            dest="team_id",
            type=str,
            help="Team ID to sign iOS bundle (ipa only)",
            required=False,
        )
        parser.add_argument(
            "--base-url",
            dest="base_url",
            type=str,
            default="/",
            help="base URL for the app (web only)",
        )
        parser.add_argument(
            "--web-renderer",
            dest="web_renderer",
            choices=["canvaskit", "html"],
            default="canvaskit",
            help="renderer to use (web only)",
        )
        parser.add_argument(
            "--use-color-emoji",
            dest="use_color_emoji",
            action="store_true",
            default=False,
            help="enables color emojis with CanvasKit renderer (web only)",
        )
        parser.add_argument(
            "--route-url-strategy",
            dest="route_url_strategy",
            choices=["path", "hash"],
            default="path",
            help="URL routing strategy (web only)",
        )
        parser.add_argument(
            "--flutter-build-args",
            dest="flutter_build_args",
            action="append",
            nargs="*",
            help="additional arguments for flutter build command",
        )
        parser.add_argument(
            "--include-packages",
            dest="flutter_packages",
            nargs="+",
            default=[],
            help="include extra Flutter Flet packages, such as flet_video, flet_audio, etc.",
        )
        parser.add_argument(
            "--build-number",
            dest="build_number",
            type=int,
            help="build number - an identifier used as an internal version number",
        )
        parser.add_argument(
            "--build-version",
            dest="build_version",
            help='build version - a "x.y.z" string used as the version number shown to users',
        )
        parser.add_argument(
            "--module-name",
            dest="module_name",
            default="main",
            help="python module name with an app entry point",
        )
        parser.add_argument(
            "--template",
            dest="template",
            type=str,
            help="a directory containing Flutter bootstrap template, or a URL to a git repository template",
        )
        parser.add_argument(
            "--template-dir",
            dest="template_dir",
            type=str,
            help="relative path to a Flutter bootstrap template in a repository",
        )
        parser.add_argument(
            "--template-ref",
            dest="template_ref",
            type=str,
            help="the branch, tag or commit ID to checkout after cloning the repository with Flutter bootstrap template",
        )

    def handle(self, options: argparse.Namespace) -> None:
        from cookiecutter.main import cookiecutter

        self.verbose = options.verbose
        self.flutter_dir = None

        # get `flutter` and `dart` executables from PATH
        self.flutter_exe = self.find_flutter_batch("flutter")
        self.dart_exe = self.find_flutter_batch("dart")

        if self.verbose > 1:
            print("Flutter executable:", self.flutter_exe)
            print("Dart executable:", self.dart_exe)

        target_platform = options.target_platform.lower()
        # platform check
        current_platform = platform.system()
        if current_platform not in self.platforms[target_platform]["can_be_run_on"]:
            # make the platform name more user friendly
            if current_platform == "Darwin":
                current_platform = "macOS"

            self.cleanup(1, f"Can't build {target_platform} on {current_platform}")

        python_app_path = Path(options.python_app_path).resolve()
        if not os.path.exists(python_app_path) or not os.path.isdir(python_app_path):
            self.cleanup(
                1,
                f"Path to Flet app does not exist or is not a directory: {python_app_path}",
            )

        python_module_name = Path(options.module_name).stem
        python_module_filename = f"{python_module_name}.py"
        if not os.path.exists(os.path.join(python_app_path, python_module_filename)):
            self.cleanup(
                1,
                f"{python_module_filename} not found in the root of Flet app directory. Use --module-name option to specify an entry point for your Flet app.",
            )

        self.flutter_dir = Path(tempfile.gettempdir()).joinpath(
            f"flet_flutter_build_{random_string(10)}"
        )

        if self.verbose > 0:
            print("Flutter bootstrap directory:", self.flutter_dir)
        self.flutter_dir.mkdir(exist_ok=True)

        rel_out_dir = (
            options.output_dir
            if options.output_dir
            else os.path.join("build", self.platforms[target_platform]["dist"])
        )
        out_dir = (
            Path(options.output_dir).resolve()
            if options.output_dir
            else python_app_path.joinpath(rel_out_dir)
        )

        template_data = {}
        template_data["out_dir"] = self.flutter_dir.name

        project_name = slugify(
            options.project_name if options.project_name else python_app_path.name
        ).replace("-", "_")

        product_name = options.product_name if options.product_name else project_name

        template_data["project_name"] = project_name

        if options.description is not None:
            template_data["description"] = options.description

        template_data["sep"] = os.sep
        template_data["python_module_name"] = python_module_name
        template_data["product_name"] = product_name
        if options.org_name:
            template_data["org_name"] = options.org_name
        if options.company_name:
            template_data["company_name"] = options.company_name
        if options.copyright:
            template_data["copyright"] = options.copyright
        if options.team_id:
            template_data["team_id"] = options.team_id

        base_url = options.base_url.strip("/").strip()
        template_data["base_url"] = "/" if base_url == "" else f"/{base_url}/"
        template_data["route_url_strategy"] = options.route_url_strategy
        template_data["web_renderer"] = options.web_renderer
        template_data["use_color_emoji"] = (
            "true" if options.use_color_emoji else "false"
        )

        src_pubspec = None
        src_pubspec_path = python_app_path.joinpath("pubspec.yaml")
        if src_pubspec_path.exists():
            with open(src_pubspec_path, encoding="utf8") as f:
                src_pubspec = pubspec = yaml.safe_load(f)

        flutter_dependencies = (
            src_pubspec["dependencies"]
            if src_pubspec and src_pubspec["dependencies"]
            else {}
        )

        if options.flutter_packages:
            for package in options.flutter_packages:
                pspec = package.split(":")
                flutter_dependencies[pspec[0]] = pspec[1] if len(pspec) > 1 else "any"

        if self.verbose > 0:
            print("Additional Flutter dependencies:", flutter_dependencies)

        template_data["flutter"] = {"dependencies": list(flutter_dependencies.keys())}

        template_url = options.template
        template_ref = options.template_ref
        if not template_url:
            template_url = DEFAULT_TEMPLATE_URL
            if flet.version.version and not template_ref:
                template_ref = version.Version(flet.version.version).base_version

        # create Flutter project from a template
        print("Creating Flutter bootstrap project...", end="")
        try:
            cookiecutter(
                template=template_url,
                checkout=template_ref,
                directory=options.template_dir,
                output_dir=str(self.flutter_dir.parent),
                no_input=True,
                overwrite_if_exists=True,
                extra_context=template_data,
            )
        except Exception as e:
            self.cleanup(1, f"{e}")
        print("[spring_green3]OK[/spring_green3]")

        # load pubspec.yaml
        pubspec_path = str(self.flutter_dir.joinpath("pubspec.yaml"))
        with open(pubspec_path, encoding="utf8") as f:
            pubspec = yaml.safe_load(f)

        # merge dependencies to a dest pubspec.yaml
        for k, v in flutter_dependencies.items():
            pubspec["dependencies"][k] = v

        if src_pubspec and src_pubspec["dependency_overrides"]:
            pubspec["dependency_overrides"] = {}
            for k, v in src_pubspec["dependency_overrides"].items():
                pubspec["dependency_overrides"][k] = v

        # make sure project name is not named as any of dependencies
        for dep in pubspec["dependencies"].keys():
            if dep == project_name:
                self.cleanup(
                    1,
                    f"Project name cannot have the same name as one of its dependencies: {dep}. Use --project option to specify a different project name.",
                )

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
            if options.android_adaptive_icon_background:
                fallback_image(
                    "flutter_launcher_icons/adaptive_icon_foreground",
                    [android_icon, default_icon],
                )
                pubspec["flutter_launcher_icons"][
                    "adaptive_icon_background"
                ] = options.android_adaptive_icon_background
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

        # enable/disable splashes
        pubspec["flutter_native_splash"]["web"] = not options.no_web_splash
        pubspec["flutter_native_splash"]["ios"] = not options.no_ios_splash
        pubspec["flutter_native_splash"]["android"] = not options.no_android_splash

        print("[spring_green3]OK[/spring_green3]")

        # save pubspec.yaml
        with open(pubspec_path, "w", encoding="utf8") as f:
            yaml.dump(pubspec, f)

        # generate icons
        print("Generating app icons...", end="")
        icons_result = self.run(
            [self.dart_exe, "run", "flutter_launcher_icons"],
            cwd=str(self.flutter_dir),
            capture_output=self.verbose < 1,
        )
        if icons_result.returncode != 0:
            if icons_result.stdout:
                print(icons_result.stdout)
            if icons_result.stderr:
                print(icons_result.stderr)
            self.cleanup(icons_result.returncode, check_flutter_version=True)

        print("[spring_green3]OK[/spring_green3]")

        # generate splash
        if target_platform in ["web", "ipa", "apk", "aab"]:
            print("Generating splash screens...", end="")
            splash_result = self.run(
                [self.dart_exe, "run", "flutter_native_splash:create"],
                cwd=str(self.flutter_dir),
                capture_output=self.verbose < 1,
            )
            if splash_result.returncode != 0:
                if splash_result.stdout:
                    print(splash_result.stdout)
                if splash_result.stderr:
                    print(splash_result.stderr)
                self.cleanup(splash_result.returncode, check_flutter_version=True)

            print("[spring_green3]OK[/spring_green3]")

        # package Python app
        print(f"Packaging Python app...", end="")
        package_args = [
            self.dart_exe,
            "run",
            "serious_python:main",
            "package",
            str(python_app_path),
        ]
        if target_platform == "web":
            pip_platform, find_links_path = self.create_pyodide_find_links()
            package_args.extend(
                [
                    "--web",
                    "--dep-mappings",
                    "flet=flet-pyodide",
                    "--req-deps",
                    "flet-pyodide,micropip",
                    "--platform",
                    pip_platform,
                    "--find-links",
                    find_links_path,
                    "--exclude",
                    "assets,build",
                ]
            )
        else:
            if target_platform in ["apk", "aab", "ipa"]:
                package_args.extend(
                    [
                        "--mobile",
                        "--platform",
                        "mobile",
                    ]
                )
            package_args.extend(
                [
                    "--dep-mappings",
                    "flet=flet-embed",
                    "--req-deps",
                    "flet-embed",
                    "--exclude",
                    "build",
                ]
            )

        if self.verbose > 1:
            package_args.append("--verbose")

        package_result = self.run(
            package_args, cwd=str(self.flutter_dir), capture_output=self.verbose < 1
        )

        if package_result.returncode != 0:
            if package_result.stdout:
                print(package_result.stdout)
            if package_result.stderr:
                print(package_result.stderr)
            self.cleanup(package_result.returncode)

        # make sure app/app.zip exists
        app_zip_path = self.flutter_dir.joinpath("app", "app.zip")
        if not os.path.exists(app_zip_path):
            self.cleanup(1, "Flet app package app/app.zip was not created.")

        # create {flutter_dir}/app/app.hash
        app_hash_path = self.flutter_dir.joinpath("app", "app.zip.hash")
        with open(app_hash_path, "w", encoding="utf8") as hf:
            hf.write(calculate_file_hash(app_zip_path))
        print("[spring_green3]OK[/spring_green3]")

        # run `flutter build`
        print(
            f"Building [cyan]{self.platforms[target_platform]['status_text']}[/cyan]...",
            end="",
        )
        build_args = [
            self.flutter_exe,
            "build",
            self.platforms[target_platform]["build_command"],
        ]

        if target_platform in ["ipa"] and not options.team_id:
            build_args.extend(["--no-codesign"])

        if options.build_number:
            build_args.extend(["--build-number", str(options.build_number)])

        if options.build_version:
            build_args.extend(["--build-name", options.build_version])

        if options.flutter_build_args:
            for flutter_build_arg_arr in options.flutter_build_args:
                for flutter_build_arg in flutter_build_arg_arr:
                    build_args.append(flutter_build_arg)

        if self.verbose > 1:
            build_args.append("--verbose")

        build_result = self.run(
            build_args, cwd=str(self.flutter_dir), capture_output=self.verbose < 1
        )

        if build_result.returncode != 0:
            if build_result.stdout:
                print(build_result.stdout)
            if build_result.stderr:
                print(build_result.stderr)
            self.cleanup(build_result.returncode, check_flutter_version=True)
        print("[spring_green3]OK[/spring_green3]")

        # copy build results to `out_dir`
        print(
            f"Copying build to [cyan]{rel_out_dir}[/cyan] directory...",
            end="",
        )
        arch = platform.machine().lower()
        if arch == "x86_64" or arch == "amd64":
            arch = "x64"
        elif arch == "arm64" or arch == "aarch64":
            arch = "arm64"

        for build_output in self.platforms[target_platform]["outputs"]:
            build_output_dir = (
                str(self.flutter_dir.joinpath(build_output))
                .replace("{arch}", arch)
                .replace("{project_name}", project_name)
                .replace("{product_name}", product_name)
            )

            if self.verbose > 0:
                print("Copying build output from:", build_output_dir)

            build_output_glob = os.path.basename(build_output_dir)
            build_output_dir = os.path.dirname(build_output_dir)
            if not os.path.exists(build_output_dir):
                continue

            if out_dir.exists():
                shutil.rmtree(str(out_dir), ignore_errors=False, onerror=None)
            out_dir.mkdir(parents=True, exist_ok=True)

            def ignore_build_output(path, files):
                if path == build_output_dir and build_output_glob != "*":
                    return [f for f in os.listdir(path) if f != build_output_glob]
                return []

            copy_tree(build_output_dir, str(out_dir), ignore=ignore_build_output)

        if target_platform == "web" and assets_path.exists():
            # copy `assets` directory contents to the output directory
            copy_tree(str(assets_path), str(out_dir))

        print("[spring_green3]OK[/spring_green3]")

        self.cleanup(0)

    def create_pyodide_find_links(self):
        with urllib.request.urlopen(f"{PYODIDE_ROOT_URL}/pyodide-lock.json") as j:
            data = json.load(j)
        find_links_path = str(self.flutter_dir.joinpath("find-links.html"))
        with open(find_links_path, "w", encoding="utf8") as f:
            for package in data["packages"].values():
                file_name = package["file_name"]
                f.write(f'<a href="{PYODIDE_ROOT_URL}/{file_name}">{file_name}</a>\n')
        return f"{data['info']['platform']}_{data['info']['arch']}", find_links_path

    def copy_icon_image(self, src_path: Path, dest_path: Path, image_name: str):
        images = glob.glob(str(src_path.joinpath(f"{image_name}.*")))
        if len(images) > 0:
            if self.verbose > 0:
                print(f"Copying {images[0]} to {dest_path}")
            shutil.copy(images[0], dest_path)
            return Path(images[0]).name
        return None

    def find_flutter_batch(self, exe_filename: str):
        batch_path = shutil.which(exe_filename)
        if not batch_path:
            self.cleanup(
                1,
                f"`{exe_filename}` command is not available in PATH. Install Flutter SDK.",
            )
            return
        if is_windows() and batch_path.endswith(".file"):
            return batch_path.replace(".file", ".bat")
        return batch_path

    def run(self, args, cwd, capture_output=True):
        if is_windows():
            # Source: https://stackoverflow.com/a/77374899/1435891
            # Save the current console output code page and switch to 65001 (UTF-8)
            previousCp = windll.kernel32.GetConsoleOutputCP()
            windll.kernel32.SetConsoleOutputCP(65001)

        if self.verbose > 0:
            print(f"\nRun subprocess: {args}")

        r = subprocess.run(
            args,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            encoding="utf8",
        )

        if is_windows():
            # Restore the previous output console code page.
            windll.kernel32.SetConsoleOutputCP(previousCp)

        return r

    def cleanup(
        self, exit_code: int, message: Optional[str] = None, check_flutter_version=False
    ):
        if self.flutter_dir and os.path.exists(self.flutter_dir):
            if self.verbose > 0:
                print(f"Deleting Flutter bootstrap directory {self.flutter_dir}")
            shutil.rmtree(str(self.flutter_dir), ignore_errors=True, onerror=None)
        if exit_code == 0:
            msg = message if message else "Success!"
            print(f"[spring_green3]{msg}[/spring_green3]")
        else:
            msg = (
                message
                if message
                else "Error building Flet app - see the log of failed command above."
            )
            if check_flutter_version:
                version_results = self.run(
                    [self.flutter_exe, "--version"],
                    cwd=os.getcwd(),
                    capture_output=True,
                )
                if version_results.returncode == 0 and version_results.stdout:
                    match = re.search(
                        r"Flutter (\d+\.\d+\.\d+)", version_results.stdout
                    )
                    if match:
                        flutter_version = version.parse(match.group(1))
                        if flutter_version < version.parse(MINIMAL_FLUTTER_VERSION):
                            flutter_msg = (
                                "Incorrect version of Flutter SDK installed. "
                                + f"Flet build requires Flutter {MINIMAL_FLUTTER_VERSION} or above. "
                                + f"You have {flutter_version}."
                            )
                            msg = f"{msg}\n{flutter_msg}"
            print(f"[red]{msg}[/red]")
        sys.exit(exit_code)
