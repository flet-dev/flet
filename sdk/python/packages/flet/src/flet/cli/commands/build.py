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
from typing import Optional, Union

import yaml
from packaging import version
from rich.console import Console, Style
from rich.table import Table, Column

import flet.version
from flet.cli.commands.base import BaseCommand
from flet.version import update_version
from flet_core.utils import random_string, slugify
from flet_runtime.utils import (
    calculate_file_hash,
    copy_tree,
    is_windows,
    get_bool_env_var,
)

if is_windows():
    from ctypes import windll

PYODIDE_ROOT_URL = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full"
DEFAULT_TEMPLATE_URL = "gh:flet-dev/flet-build-template"
MINIMAL_FLUTTER_VERSION = "3.19.0"

error_style = Style(color="red1")
console = Console(log_path=False, style=Style(color="green", bold=True))


class Command(BaseCommand):
    """
    Build an executable app or install bundle.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)

        self.emojis = {}
        self.dart_exe = None
        self.verbose = None
        self.flutter_dir = None
        self.flutter_exe = None
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

        # create and display build-platform-matrix table
        self.platform_matrix_table = Table(
            Column("Command", style="cyan", justify="left"),
            Column("Platform", style="magenta", justify="center"),
            title="Build Platform Matrix",
            header_style="bold",
            show_lines=True,
        )
        for p, info in self.platforms.items():
            self.platform_matrix_table.add_row(
                "flet build " + p,
                ", ".join(info["can_be_run_on"]).replace("Darwin", "macOS"),
                # style="bold red1" if p == target_platform else None,
            )

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
            "--exclude",
            dest="exclude",
            nargs="+",
            default=[],
            help="exclude files and directories from a Python app package",
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
        parser.add_argument(
            "--show-platform-matrix",
            action="store_true",
            default=False,
            help="displays the build platform matrix in a table, then exits",
        )
        parser.add_argument(
            "--no-rich-output",
            action="store_true",
            default=False,
            help="disables rich output and uses plain text instead",
        )

    def handle(self, options: argparse.Namespace) -> None:
        self.verbose = options.verbose
        self.flutter_dir = None
        no_rich_output = options.no_rich_output or get_bool_env_var(
            "FLET_CLI_NO_RICH_OUTPUT"
        )
        self.emojis = {
            "checkmark": "[green]OK[/]" if no_rich_output else "✅",
            "loading": "" if no_rich_output else "⏳",
            "success": "" if no_rich_output else "🥳",
            "directory": "" if no_rich_output else "📁",
        }
        target_platform = options.target_platform.lower()
        # platform check
        current_platform = platform.system()
        if (
            current_platform not in self.platforms[target_platform]["can_be_run_on"]
            or options.show_platform_matrix
        ):
            can_build_message = (
                "can't"
                if current_platform
                not in self.platforms[target_platform]["can_be_run_on"]
                else "can"
            )
            # replace "Darwin" with "macOS" for user-friendliness
            current_platform = (
                "macOS" if current_platform == "Darwin" else current_platform
            )
            # highlight the current platform in the build matrix table
            self.platform_matrix_table.rows[
                list(self.platforms.keys()).index(target_platform)
            ].style = "bold red1"
            console.log(self.platform_matrix_table)

            message = f"You {can_build_message} build [cyan]{target_platform}[/] on [magenta]{current_platform}[/]."
            self.cleanup(1, message)

        with console.status(
            f"[bold blue]Initializing {target_platform} build... ",
            spinner="bouncingBall",
        ) as self.status:
            from cookiecutter.main import cookiecutter

            # get `flutter` and `dart` executables from PATH
            self.flutter_exe = self.find_flutter_batch("flutter")
            self.dart_exe = self.find_flutter_batch("dart")

            if self.verbose > 1:
                console.log("Flutter executable:", self.flutter_exe)
                console.log("Dart executable:", self.dart_exe)

            python_app_path = Path(options.python_app_path).resolve()
            if not os.path.exists(python_app_path) or not os.path.isdir(
                python_app_path
            ):
                self.cleanup(
                    1,
                    f"Path to Flet app does not exist or is not a directory: {python_app_path}",
                )

            python_module_name = Path(options.module_name).stem
            python_module_filename = f"{python_module_name}.py"
            if not os.path.exists(
                os.path.join(python_app_path, python_module_filename)
            ):
                self.cleanup(
                    1,
                    f"{python_module_filename} not found in the root of Flet app directory. "
                    f"Use --module-name option to specify an entry point for your Flet app.",
                )

            self.flutter_dir = Path(tempfile.gettempdir()).joinpath(
                f"flet_flutter_build_{random_string(10)}"
            )

            if self.verbose > 0:
                console.log("Flutter bootstrap directory:", self.flutter_dir)
            self.flutter_dir.mkdir(exist_ok=True)

            rel_out_dir = options.output_dir or os.path.join(
                "build", self.platforms[target_platform]["dist"]
            )

            out_dir = (
                Path(options.output_dir).resolve()
                if options.output_dir
                else python_app_path.joinpath(rel_out_dir)
            )

            base_url = options.base_url.strip("/").strip()
            project_name = slugify(
                options.project_name or python_app_path.name
            ).replace("-", "_")
            product_name = options.product_name or project_name

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
                    flutter_dependencies[pspec[0]] = (
                        pspec[1] if len(pspec) > 1 else "any"
                    )

            if self.verbose > 0:
                console.log(
                    f"Additional Flutter dependencies: {flutter_dependencies}"
                    if flutter_dependencies
                    else "No additional Flutter dependencies!"
                )

            template_data = {
                "out_dir": self.flutter_dir.name,
                "sep": os.sep,
                "python_module_name": python_module_name,
                "route_url_strategy": options.route_url_strategy,
                "web_renderer": options.web_renderer,
                "use_color_emoji": "true" if options.use_color_emoji else "false",
                "base_url": f"/{base_url}/" if base_url else "/",
                "project_name": project_name,
                "product_name": product_name,
                "description": options.description,
                "org_name": options.org_name,
                "company_name": options.company_name,
                "copyright": options.copyright,
                "team_id": options.team_id,
                "flutter": {"dependencies": list(flutter_dependencies.keys())},
            }
            # Remove None values from the dictionary
            template_data = {k: v for k, v in template_data.items() if v is not None}

            template_url = options.template
            template_ref = options.template_ref
            if not template_url:
                template_url = DEFAULT_TEMPLATE_URL
                if not template_ref:
                    template_ref = (
                        version.Version(flet.version.version).base_version
                        if flet.version.version
                        else update_version()
                    )

            # create Flutter project from a template
            self.status.update(
                f"[bold blue]Creating Flutter bootstrap project from {template_url} with ref {template_ref} {self.emojis['loading']}... ",
            )
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
            console.log(
                f"Created Flutter bootstrap project from {template_url} with ref {template_ref} {self.emojis['checkmark']}",
            )

            # load pubspec.yaml
            pubspec_path = str(self.flutter_dir.joinpath("pubspec.yaml"))
            with open(pubspec_path, encoding="utf8") as f:
                pubspec = yaml.safe_load(f)

            # merge dependencies to a dest pubspec.yaml
            for k, v in flutter_dependencies.items():
                pubspec["dependencies"][k] = v

            if src_pubspec and "dependency_overrides" in src_pubspec:
                pubspec["dependency_overrides"] = {}
                for k, v in src_pubspec["dependency_overrides"].items():
                    pubspec["dependency_overrides"][k] = v

            # make sure project name is not named as any of dependencies
            for dep in pubspec["dependencies"].keys():
                if dep == project_name:
                    self.cleanup(
                        1,
                        f"Project name cannot have the same name as one of its dependencies: {dep}. "
                        f"Use --project option to specify a different project name.",
                    )

            # copy icons to `flutter_dir`
            self.status.update(
                f"[bold blue]Customizing app icons and splash images {self.emojis['loading']}... ",
            )
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
                macos_icon = self.copy_icon_image(
                    assets_path, images_path, "icon_macos"
                )

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
                    "flutter_launcher_icons/macos/image_path",
                    [macos_icon, default_icon],
                )

                # copy splash images
                default_splash = self.copy_icon_image(
                    assets_path, images_path, "splash"
                )
                default_dark_splash = self.copy_icon_image(
                    assets_path, images_path, "splash_dark"
                )
                ios_splash = self.copy_icon_image(
                    assets_path, images_path, "splash_ios"
                )
                ios_dark_splash = self.copy_icon_image(
                    assets_path, images_path, "splash_dark_ios"
                )
                android_splash = self.copy_icon_image(
                    assets_path, images_path, "splash_android"
                )
                android_dark_splash = self.copy_icon_image(
                    assets_path, images_path, "splash_dark_android"
                )
                web_splash = self.copy_icon_image(
                    assets_path, images_path, "splash_web"
                )
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

            console.log(
                f"Customized app icons and splash images {self.emojis['checkmark']}"
            )

            # save pubspec.yaml
            with open(pubspec_path, "w", encoding="utf8") as f:
                yaml.dump(pubspec, f)

            # generate icons
            self.status.update(
                f"[bold blue]Generating app icons {self.emojis['loading']}... "
            )
            icons_result = self.run(
                [self.dart_exe, "run", "flutter_launcher_icons"],
                cwd=str(self.flutter_dir),
                capture_output=self.verbose < 1,
            )
            if icons_result.returncode != 0:
                if icons_result.stdout:
                    console.log(icons_result.stdout)
                if icons_result.stderr:
                    console.log(icons_result.stderr, style=error_style)
                self.cleanup(icons_result.returncode, check_flutter_version=True)

            console.log(f"Generated app icons {self.emojis['checkmark']}")
            # generate splash
            if target_platform in ["web", "ipa", "apk", "aab"]:
                self.status.update(
                    f"[bold blue]Generating splash screens {self.emojis['loading']}... ",
                )
                splash_result = self.run(
                    [self.dart_exe, "run", "flutter_native_splash:create"],
                    cwd=str(self.flutter_dir),
                    capture_output=self.verbose < 1,
                )
                if splash_result.returncode != 0:
                    if splash_result.stdout:
                        console.log(splash_result.stdout)
                    if splash_result.stderr:
                        console.log(splash_result.stderr, style=error_style)
                    self.cleanup(splash_result.returncode, check_flutter_version=True)

                console.log(f"Generated splash screens {self.emojis['checkmark']}")

            exclude_list = ["build"]

            if options.exclude:
                exclude_list.extend(options.exclude)

            # package Python app
            self.status.update(
                f"[bold blue]Packaging Python app {self.emojis['loading']}... ",
            )
            package_args = [
                self.dart_exe,
                "run",
                "serious_python:main",
                "package",
                str(python_app_path),
            ]
            if target_platform == "web":
                pip_platform, find_links_path = self.create_pyodide_find_links()
                exclude_list.append("assets")
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
                        ",".join(exclude_list),
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
                        ",".join(exclude_list),
                    ]
                )

            if self.verbose > 1:
                package_args.append("--verbose")

            package_result = self.run(
                package_args, cwd=str(self.flutter_dir), capture_output=self.verbose < 1
            )

            if package_result.returncode != 0:
                if package_result.stdout:
                    console.log(package_result.stdout)
                if package_result.stderr:
                    console.log(package_result.stderr, style=error_style)
                self.cleanup(package_result.returncode)

            # make sure app/app.zip exists
            app_zip_path = self.flutter_dir.joinpath("app", "app.zip")
            if not os.path.exists(app_zip_path):
                self.cleanup(1, "Flet app package app/app.zip was not created.")

            # create {flutter_dir}/app/app.hash
            app_hash_path = self.flutter_dir.joinpath("app", "app.zip.hash")
            with open(app_hash_path, "w", encoding="utf8") as hf:
                hf.write(calculate_file_hash(app_zip_path))
            console.log(f"Packaged Python app {self.emojis['checkmark']}")

            # run `flutter build`
            self.status.update(
                f"[bold blue]Building [cyan]{self.platforms[target_platform]['status_text']}[/cyan] {self.emojis['loading']}... ",
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
                    console.log(build_result.stdout)
                if build_result.stderr:
                    console.log(build_result.stderr, style=error_style)
                self.cleanup(build_result.returncode, check_flutter_version=True)
            console.log(
                f"Built [cyan]{self.platforms[target_platform]['status_text']}[/cyan] {self.emojis['checkmark']}",
            )

            # copy build results to `out_dir`
            self.status.update(
                f"[bold blue]Copying build to [cyan]{rel_out_dir}[/cyan] directory {self.emojis['loading']}... ",
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
                    console.log("Copying build output from: " + build_output_dir)

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

            console.log(
                f"Copied build to [cyan]{rel_out_dir}[/cyan] directory {self.emojis['checkmark']}"
            )

            self.cleanup(
                0,
                message=f"Successfully built your [cyan]{self.platforms[target_platform]['status_text']}[/cyan]! {self.emojis['success']} "
                f"Find it in [cyan]{rel_out_dir}[/cyan] directory. {self.emojis['directory']}",
            )

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
                console.log(f"Copying {images[0]} to {dest_path}")
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
            console.log(f"Run subprocess: {args}")

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
                console.log(f"Deleting Flutter bootstrap directory {self.flutter_dir}")
            shutil.rmtree(str(self.flutter_dir), ignore_errors=True, onerror=None)
        if exit_code == 0:
            msg = message or f"Success! {self.emojis['success']}"
            console.log(msg)
        else:
            msg = (
                message
                if message is not None
                else "Error building Flet app - see the log of failed command above."
            )
            console.log(msg, style=error_style)

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
                            console.log(flutter_msg, style=error_style)
            # run flutter doctor
            self.run_flutter_doctor(style=error_style)
        sys.exit(exit_code)

    def run_flutter_doctor(self, style: Optional[Union[Style, str]] = None):
        self.status.update(
            f"[bold blue]Running Flutter doctor {self.emojis['loading']}... "
        )
        flutter_doctor = self.run(
            [self.flutter_exe, "doctor"],
            cwd=os.getcwd(),
            capture_output=True,
        )
        if flutter_doctor.returncode == 0 and flutter_doctor.stdout:
            console.log(flutter_doctor.stdout, style=style)
