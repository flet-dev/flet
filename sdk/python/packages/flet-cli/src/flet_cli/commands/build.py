import argparse
import glob
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Union, cast

import flet.version
import yaml
from flet.utils import copy_tree, is_windows, slugify
from flet.utils.platform_utils import get_bool_env_var
from flet.version import update_version
from flet_cli.commands.base import BaseCommand
from flet_cli.utils.merge import merge_dict
from flet_cli.utils.project_dependencies import (
    get_poetry_dependencies,
    get_project_dependencies,
)
from flet_cli.utils.pyproject_toml import load_pyproject_toml
from packaging import version
from rich.console import Console
from rich.style import Style
from rich.table import Column, Table
from rich.theme import Theme

if is_windows():
    from ctypes import windll

PYODIDE_ROOT_URL = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full"
DEFAULT_TEMPLATE_URL = "gh:flet-dev/flet-build-template"
MINIMAL_FLUTTER_VERSION = "3.24.0"

error_style = Style(color="red", bold=True)
console = Console(log_path=False, theme=Theme({"log.message": "green bold"}))


class Command(BaseCommand):
    """
    Build an executable app or install bundle.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)

        self.pubspec_path = None
        self.rel_out_dir = None
        self.assets_path = None
        self.package_platform = None
        self.config_platform = None
        self.target_platform = None
        self.flutter_dependencies = None
        self.package_app_path = None
        self.options = None
        self.pubspec = None
        self.template_data = None
        self.python_module_filename = None
        self.out_dir = None
        self.python_module_name = None
        self.get_pyproject = None
        self.python_app_path = None
        self.no_rich_output = None
        self.emojis = {}
        self.dart_exe = None
        self.verbose = False
        self.build_dir = None
        self.flutter_dir: Optional[Path] = None
        self.flutter_exe = None
        self.skip_flutter_doctor = get_bool_env_var("FLET_CLI_SKIP_FLUTTER_DOCTOR")
        self.no_rich_output = get_bool_env_var("FLET_CLI_NO_RICH_OUTPUT")
        self.current_platform = platform.system()
        self.platforms = {
            "windows": {
                "package_platform": "Windows",
                "config_platform": "windows",
                "flutter_build_command": "windows",
                "status_text": "Windows app",
                "outputs": ["build/windows/x64/runner/Release/*"],
                "dist": "windows",
                "can_be_run_on": ["Windows"],
            },
            "macos": {
                "package_platform": "Darwin",
                "config_platform": "macos",
                "flutter_build_command": "macos",
                "status_text": "macOS bundle",
                "outputs": ["build/macos/Build/Products/Release/{product_name}.app"],
                "dist": "macos",
                "can_be_run_on": ["Darwin"],
            },
            "linux": {
                "package_platform": "Linux",
                "config_platform": "linux",
                "flutter_build_command": "linux",
                "status_text": "app for Linux",
                "outputs": ["build/linux/{arch}/release/bundle/*"],
                "dist": "linux",
                "can_be_run_on": ["Linux"],
            },
            "web": {
                "package_platform": "Pyodide",
                "config_platform": "web",
                "flutter_build_command": "web",
                "status_text": "web app",
                "outputs": ["build/web/*"],
                "dist": "web",
                "can_be_run_on": ["Darwin", "Windows", "Linux"],
            },
            "apk": {
                "package_platform": "Android",
                "config_platform": "android",
                "flutter_build_command": "apk",
                "status_text": ".apk for Android",
                "outputs": ["build/app/outputs/flutter-apk/*"],
                "dist": "apk",
                "can_be_run_on": ["Darwin", "Windows", "Linux"],
            },
            "aab": {
                "package_platform": "Android",
                "config_platform": "android",
                "flutter_build_command": "appbundle",
                "status_text": ".aab bundle for Android",
                "outputs": ["build/app/outputs/bundle/release/*"],
                "dist": "aab",
                "can_be_run_on": ["Darwin", "Windows", "Linux"],
            },
            "ipa": {
                "package_platform": "iOS",
                "config_platform": "ios",
                "flutter_build_command": "ipa",
                "status_text": ".ipa bundle for iOS",
                "outputs": ["build/ios/archive/*", "build/ios/ipa/*"],
                "dist": "ipa",
                "can_be_run_on": ["Darwin"],
            },
        }

        self.cross_platform_permissions = {
            "location": {
                "info_plist": {
                    "NSLocationWhenInUseUsageDescription": "This app uses location service when in use.",
                    "NSLocationAlwaysAndWhenInUseUsageDescription": "This app uses location service.",
                },
                "macos_entitlements": {
                    "com.apple.security.personal-information.location": True
                },
                "android_permissions": {
                    "android.permission.ACCESS_FINE_LOCATION": True,
                    "android.permission.ACCESS_COARSE_LOCATION": True,
                    "android.permission.ACCESS_BACKGROUND_LOCATION": True,
                },
                "android_features": {
                    "android.hardware.location.network": False,
                    "android.hardware.location.gps": False,
                },
            },
            "camera": {
                "info_plist": {
                    "NSCameraUsageDescription": "This app uses the camera to capture photos and videos."
                },
                "macos_entitlements": {"com.apple.security.device.camera": True},
                "android_permissions": {"android.permission.CAMERA": True},
                "android_features": {
                    "android.hardware.camera": False,
                    "android.hardware.camera.any": False,
                    "android.hardware.camera.front": False,
                    "android.hardware.camera.external": False,
                    "android.hardware.camera.autofocus": False,
                },
            },
            "microphone": {
                "info_plist": {
                    "NSMicrophoneUsageDescription": "This app uses microphone to record sounds.",
                },
                "macos_entitlements": {"com.apple.security.device.audio-input": True},
                "android_permissions": {
                    "android.permission.RECORD_AUDIO": True,
                    "android.permission.WRITE_EXTERNAL_STORAGE": True,
                    "android.permission.READ_EXTERNAL_STORAGE": True,
                },
                "android_features": {},
            },
            "photo_library": {
                "info_plist": {
                    "NSPhotoLibraryUsageDescription": "This app saves photos and videos to the photo library."
                },
                "macos_entitlements": {
                    "com.apple.security.personal-information.photos-library": True
                },
                "android_permissions": {
                    "android.permission.READ_MEDIA_VISUAL_USER_SELECTED": True
                },
                "android_features": {},
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
            "--arch",
            dest="target_arch",
            required=False,
            choices=["arm64-v8a", "armeabi-v7a", "x86_64", "x86", "arm64"],
            help="package for specific architecture only. Used with Android and macOS builds only.",
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
            "--clear-cache",
            dest="clear_cache",
            action="store_true",
            default=None,
            help="clear build cache",
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
            default=None,
            help="disable web app splash screen",
        )
        parser.add_argument(
            "--no-ios-splash",
            dest="no_ios_splash",
            action="store_true",
            default=None,
            help="disable iOS app splash screen",
        )
        parser.add_argument(
            "--no-android-splash",
            dest="no_android_splash",
            action="store_true",
            default=None,
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
            help="base URL for the app (web only)",
        )
        parser.add_argument(
            "--web-renderer",
            dest="web_renderer",
            choices=["canvaskit", "html"],
            help="renderer to use (web only)",
        )
        parser.add_argument(
            "--use-color-emoji",
            dest="use_color_emoji",
            action="store_true",
            help="enables color emojis with CanvasKit renderer (web only)",
        )
        parser.add_argument(
            "--route-url-strategy",
            dest="route_url_strategy",
            choices=["path", "hash"],
            help="URL routing strategy (web only)",
        )
        parser.add_argument(
            "--pwa-background-color",
            dest="pwa_background_color",
            help="an initial background color for your web application",
            required=False,
        )
        parser.add_argument(
            "--pwa-theme-color",
            dest="pwa_theme_color",
            help="default color for your web application's user interface",
            required=False,
        )
        parser.add_argument(
            "--split-per-abi",
            dest="split_per_abi",
            action="store_true",
            default=None,
            help="whether to split the APKs per ABIs.",
        )
        parser.add_argument(
            "--compile-app",
            dest="compile_app",
            action="store_true",
            default=None,
            help="compile app's .py files to .pyc",
        )
        parser.add_argument(
            "--compile-packages",
            dest="compile_packages",
            action="store_true",
            default=None,
            help="compile site packages' .py files to .pyc",
        )
        parser.add_argument(
            "--cleanup-on-compile",
            dest="cleanup_on_compile",
            action="store_true",
            default=None,
            help="remove unnecessary app and package files after compiling",
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
            "--info-plist",
            dest="info_plist",
            nargs="+",
            default=[],
            help='the list of "<key>=<value>|True|False" pairs to add to Info.plist for macOS and iOS builds',
        )
        parser.add_argument(
            "--macos-entitlements",
            dest="macos_entitlements",
            nargs="+",
            default=[],
            help='the list of "<key>=<value>|True|False" entitlements for macOS builds',
        )
        parser.add_argument(
            "--android-features",
            dest="android_features",
            nargs="+",
            default=[],
            help='the list of "<feature_name>=True|False" features to add to AndroidManifest.xml',
        )
        parser.add_argument(
            "--android-permissions",
            dest="android_permissions",
            nargs="+",
            default=[],
            help='the list of "<permission_name>=True|False" permissions to add to AndroidManifest.xml',
        )
        parser.add_argument(
            "--android-meta-data",
            dest="android_meta_data",
            nargs="+",
            default=[],
            help='the list of "<name>=<value>" app meta-data entries to add to AndroidManifest.xml',
        )
        parser.add_argument(
            "--permissions",
            dest="permissions",
            nargs="+",
            default=[],
            choices=["location", "camera", "microphone", "photo_library"],
            help="the list of cross-platform permissions for iOS, Android and macOS apps",
        )
        parser.add_argument(
            "--deep-linking-scheme",
            dest="deep_linking_scheme",
            help='deep linking URL scheme to configure for iOS and Android builds, i.g. "https" or "myapp"',
        )
        parser.add_argument(
            "--deep-linking-host",
            dest="deep_linking_host",
            help="deep linking URL host for iOS and Android builds",
        )
        parser.add_argument(
            "--android-signing-key-store",
            dest="android_signing_key_store",
            help="path to an upload keystore .jks file for Android apps",
        )
        parser.add_argument(
            "--android-signing-key-store-password",
            dest="android_signing_key_store_password",
            help="Android signing store password",
        )
        parser.add_argument(
            "--android-signing-key-password",
            dest="android_signing_key_password",
            help="Android signing key password",
        )
        parser.add_argument(
            "--android-signing-key-alias",
            dest="android_signing_key_alias",
            default="upload",
            help='Android signing key alias. Default is "upload".',
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
        parser.add_argument(
            "--skip-flutter-doctor",
            action="store_true",
            default=False,
            help="whether to skip running Flutter doctor in failed builds",
        )

    def handle(self, options: argparse.Namespace) -> None:
        self.options = options
        with console.status(
            f"[bold blue]Initializing {self.options.target_platform} build... ",
            spinner="bouncingBall",
        ) as self.status:
            self.initialize_build()
            self.validate_target_platform()
            self.validate_entry_point()
            self.setup_template_data()
            self.create_flutter_project()
            self.load_pubspec()
            self.customize_icons_and_splash_images()
            self.generate_icons_and_splash_screens()
            self.package_python_app()
            self.flutter_build()
            self.copy_build_output()

            self.cleanup(
                0,
                message=(
                    f"Successfully built your [cyan]{self.platforms[self.options.target_platform]['status_text']}[/cyan]! {self.emojis['success']} "
                    f"Find it in [cyan]{self.rel_out_dir}[/cyan] directory. {self.emojis['directory']}"
                    + (
                        f"\nRun [cyan]python -m http.server --directory {self.rel_out_dir}[/cyan] command to start dev web server with your app. "
                        if self.options.target_platform == "web"
                        else ""
                    )
                ),
            )

    def initialize_build(self):
        assert self.options
        self.python_app_path = Path(self.options.python_app_path).resolve()
        if not (
            os.path.exists(self.python_app_path) or os.path.isdir(self.python_app_path)
        ):
            self.cleanup(
                1,
                f"Path to Flet app does not exist or is not a directory: {self.python_app_path}",
            )

        # get `flutter` and `dart` executables from PATH
        self.flutter_exe = self.find_flutter_batch("flutter")
        self.dart_exe = self.find_flutter_batch("dart")

        self.verbose = self.options.verbose
        if self.verbose > 1:
            console.log("Flutter executable:", self.flutter_exe)
            console.log("Dart executable:", self.dart_exe)

        self.no_rich_output = self.no_rich_output or self.options.no_rich_output
        self.skip_flutter_doctor = (
            self.skip_flutter_doctor or self.options.skip_flutter_doctor
        )
        self.emojis = {
            "checkmark": "[green]OK[/]" if self.no_rich_output else "✅",
            "loading": "" if self.no_rich_output else "⏳",
            "success": "" if self.no_rich_output else "🥳",
            "directory": "" if self.no_rich_output else "📁",
        }
        self.package_platform = self.platforms[self.options.target_platform][
            "package_platform"
        ]
        self.config_platform = self.platforms[self.options.target_platform][
            "config_platform"
        ]
        self.rel_out_dir = self.options.output_dir or os.path.join(
            "build", self.platforms[self.options.target_platform]["dist"]
        )

        self.build_dir = self.python_app_path.joinpath("build")
        self.flutter_dir = Path(self.build_dir).joinpath("flutter")
        self.out_dir = (
            Path(self.options.output_dir).resolve()
            if self.options.output_dir
            else self.python_app_path.joinpath(self.rel_out_dir)
        )
        self.pubspec_path = str(self.flutter_dir.joinpath("pubspec.yaml"))
        self.get_pyproject = load_pyproject_toml(self.python_app_path)

    def validate_target_platform(
        self,
    ):
        assert self.options
        if (
            self.current_platform
            not in self.platforms[self.options.target_platform]["can_be_run_on"]
            or self.options.show_platform_matrix
        ):
            can_build_message = (
                "can't"
                if self.current_platform
                not in self.platforms[self.options.target_platform]["can_be_run_on"]
                else "can"
            )
            # replace "Darwin" with "macOS" for user-friendliness
            self.current_platform = (
                "macOS" if self.current_platform == "Darwin" else self.current_platform
            )
            # highlight the current platform in the build matrix table
            self.platform_matrix_table.rows[
                list(self.platforms.keys()).index(self.options.target_platform)
            ].style = "bold red1"
            console.log(self.platform_matrix_table)

            message = f"You {can_build_message} build [cyan]{self.options.target_platform}[/] on [magenta]{self.current_platform}[/]."
            self.cleanup(1, message)

    def validate_entry_point(self):
        assert self.options
        assert self.python_app_path
        assert self.get_pyproject

        self.package_app_path = Path(self.python_app_path)
        if self.get_pyproject("tool.flet.app.path"):
            self.package_app_path = self.python_app_path.joinpath(
                cast(str, self.get_pyproject("tool.flet.app.path"))
            )

        self.python_module_name = Path(
            self.options.module_name
            or cast(str, self.get_pyproject("tool.flet.app.module"))
            or "main"
        ).stem
        self.python_module_filename = f"{self.python_module_name}.py"
        if not self.package_app_path.joinpath(self.python_module_filename).exists():
            self.cleanup(
                1,
                f"{self.python_module_filename} not found in the root of Flet app directory. "
                f"Use --module-name option to specify an entry point for your Flet app.",
            )

    def setup_template_data(
        self,
    ):
        assert self.options
        assert self.python_app_path
        assert self.get_pyproject

        base_url = (
            (
                self.options.base_url
                or cast(str, self.get_pyproject("tool.flet.web.base_url"))
                or "/"
            )
            .strip("/")
            .strip()
        )
        project_name_orig = (
            self.options.project_name
            or self.get_pyproject("project.name")
            or self.get_pyproject("tool.poetry.name")
            or self.python_app_path.name
        )
        project_name_slug = slugify(cast(str, project_name_orig))
        project_name = project_name_slug.replace("-", "_")
        product_name = (
            self.options.product_name
            or self.get_pyproject("tool.flet.product")
            or project_name_orig
        )
        self.flutter_dependencies = self.get_flutter_dependencies()
        if self.verbose > 0:
            console.log(
                f"Additional Flutter dependencies: {self.flutter_dependencies}"
                if self.flutter_dependencies
                else "No additional Flutter dependencies!"
            )

        split_per_abi = (
            self.options.split_per_abi
            if self.options.split_per_abi is not None
            else (
                self.get_pyproject("tool.flet.android.split_per_abi")
                if self.get_pyproject("tool.flet.android.split_per_abi") is not None
                else False
            )
        )

        info_plist = {}
        macos_entitlements = {
            "com.apple.security.app-sandbox": False,
            "com.apple.security.cs.allow-jit": True,
            "com.apple.security.network.client": True,
            "com.apple.security.network.server": True,
        }
        android_permissions = {"android.permission.INTERNET": True}
        android_features = {
            "android.software.leanback": False,
            "android.hardware.touchscreen": False,
        }
        android_meta_data = {"io.flutter.embedding.android.EnableImpeller": "false"}

        # merge values from "--permissions" arg:
        for p in (
            self.options.permissions
            or self.get_pyproject("tool.flet.permissions")
            or []
        ):
            if p in self.cross_platform_permissions:
                info_plist.update(self.cross_platform_permissions[p]["info_plist"])
                macos_entitlements.update(
                    self.cross_platform_permissions[p]["macos_entitlements"]
                )
                android_permissions.update(
                    self.cross_platform_permissions[p]["android_permissions"]
                )
                android_features.update(
                    self.cross_platform_permissions[p]["android_features"]
                )

        info_plist = merge_dict(
            info_plist,
            (
                self.get_pyproject("tool.flet.macos.info")
                if self.package_platform == "Darwin"
                else self.get_pyproject("tool.flet.ios.info")
            )
            or {},
        )

        # parse --info-plist
        for p in self.options.info_plist:
            i = p.find("=")
            if i > -1:
                k = p[:i]
                v = p[i + 1 :]
                info_plist[k] = True if v == "True" else False if v == "False" else v
            else:
                self.cleanup(1, f"Invalid Info.plist option: {p}")

        macos_entitlements = merge_dict(
            macos_entitlements,
            self.get_pyproject("tool.flet.macos.entitlement") or {},
        )

        # parse --macos-entitlements
        for p in self.options.macos_entitlements:
            i = p.find("=")
            if i > -1:
                macos_entitlements[p[:i]] = True if p[i + 1 :] == "True" else False
            else:
                self.cleanup(1, f"Invalid macOS entitlement option: {p}")

        android_permissions = merge_dict(
            android_permissions,
            self.get_pyproject("tool.flet.android.permission") or {},
        )

        # parse --android-permissions
        for p in self.options.android_permissions:
            i = p.find("=")
            if i > -1:
                android_permissions[p[:i]] = True if p[i + 1 :] == "True" else False
            else:
                self.cleanup(1, f"Invalid Android permission option: {p}")

        android_features = merge_dict(
            android_features,
            self.get_pyproject("tool.flet.android.feature") or {},
        )

        # parse --android-features
        for p in self.options.android_features:
            i = p.find("=")
            if i > -1:
                android_features[p[:i]] = True if p[i + 1 :] == "True" else False
            else:
                self.cleanup(1, f"Invalid Android feature option: {p}")

        android_meta_data = merge_dict(
            android_meta_data,
            self.get_pyproject("tool.flet.android.meta_data") or {},
        )

        # parse --android-meta-data
        for p in self.options.android_meta_data:
            i = p.find("=")
            if i > -1:
                android_meta_data[p[:i]] = p[i + 1 :]
            else:
                self.cleanup(1, f"Invalid Android meta-data option: {p}")

        deep_linking_scheme = (
            self.get_pyproject("tool.flet.ios.deep_linking.scheme")
            if self.package_platform == "iOS"
            else (
                self.get_pyproject("tool.flet.android.deep_linking.scheme")
                if self.package_platform == "Android"
                else self.get_pyproject("tool.flet.deep_linking.scheme")
            )
        )

        deep_linking_host = (
            self.get_pyproject("tool.flet.ios.deep_linking.host")
            if self.package_platform == "iOS"
            else (
                self.get_pyproject("tool.flet.android.deep_linking.host")
                if self.package_platform == "Android"
                else self.get_pyproject("tool.flet.deep_linking.host")
            )
        )

        if self.options.deep_linking_scheme and self.options.deep_linking_host:
            deep_linking_scheme = self.options.deep_linking_scheme
            deep_linking_host = self.options.deep_linking_host

        assert self.flutter_dir
        self.template_data = {
            "out_dir": self.flutter_dir.name,
            "sep": os.sep,
            "python_module_name": self.python_module_name,
            "route_url_strategy": (
                self.options.route_url_strategy
                or self.get_pyproject("tool.flet.web.route_url_strategy")
                or "path"
            ),
            "web_renderer": (
                self.options.web_renderer
                or self.get_pyproject("tool.flet.web.renderer")
                or "canvaskit"
            ),
            "use_color_emoji": (
                "true"
                if self.options.use_color_emoji
                or self.get_pyproject("tool.flet.web.use_color_emoji")
                else "false"
            ),
            "pwa_background_color": (
                self.options.pwa_background_color
                or self.get_pyproject("tool.flet.web.pwa_background_color")
            ),
            "pwa_theme_color": (
                self.options.pwa_theme_color
                or self.get_pyproject("tool.flet.web.pwa_theme_color")
            ),
            "base_url": f"/{base_url}/" if base_url else "/",
            "split_per_abi": split_per_abi,
            "project_name": project_name,
            "project_name_slug": project_name_slug,
            "product_name": product_name,
            "description": (
                self.options.description
                or self.get_pyproject("project.description")
                or self.get_pyproject("tool.poetry.description")
            ),
            "org_name": self.options.org_name or self.get_pyproject("tool.flet.org"),
            "company_name": (
                self.options.company_name or self.get_pyproject("tool.flet.company")
            ),
            "copyright": self.options.copyright
            or self.get_pyproject("tool.flet.copyright"),
            "team_id": self.options.team_id or self.get_pyproject("tool.flet.ios.team"),
            "options": {
                "info_plist": info_plist,
                "macos_entitlements": macos_entitlements,
                "android_permissions": android_permissions,
                "android_features": android_features,
                "android_meta_data": android_meta_data,
                "deep_linking": {
                    "scheme": deep_linking_scheme,
                    "host": deep_linking_host,
                },
                "android_signing": self.options.android_signing_key_store is not None,
            },
            "flutter": {"dependencies": list(self.flutter_dependencies.keys())},
        }

    def get_flutter_dependencies(self) -> dict:
        assert self.options
        assert self.get_pyproject

        flutter_dependencies = (
            self.get_pyproject("tool.flet.flutter.dependencies") or {}
        )
        if isinstance(flutter_dependencies, list):
            flutter_dependencies = {d: "any" for d in flutter_dependencies}

        if self.options.flutter_packages:
            for package in self.options.flutter_packages:
                pspec = package.split(":")
                flutter_dependencies[pspec[0]] = pspec[1] if len(pspec) > 1 else "any"

        return flutter_dependencies

    def create_flutter_project(self):
        assert self.options
        assert self.get_pyproject
        assert self.flutter_dir
        assert self.template_data

        template_url = (
            self.options.template
            or self.get_pyproject("tool.flet.template.url")
            or DEFAULT_TEMPLATE_URL
        )
        template_ref = self.options.template_ref or self.get_pyproject(
            "tool.flet.template.ref"
        )
        if not template_ref:
            template_ref = (
                version.Version(flet.version.version).base_version
                if flet.version.version
                else update_version()
            )
        template_dir = self.options.template_dir or self.get_pyproject(
            "tool.flet.template.dir"
        )

        # if options.clear_cache is set, delete any existing Flutter bootstrap project directory
        if self.options.clear_cache and self.flutter_dir.exists():
            if self.verbose > 1:
                console.log(f"Deleting {self.flutter_dir}")
            shutil.rmtree(self.flutter_dir, ignore_errors=True)

        # create a new Flutter bootstrap project directory, if non-existent
        self.flutter_dir.mkdir(parents=True, exist_ok=True)
        self.status.update(
            f"[bold blue]Creating Flutter bootstrap project from {template_url} with ref {template_ref} {self.emojis['loading']}... "
        )

        try:
            from cookiecutter.main import cookiecutter

            cookiecutter(
                template=template_url,
                checkout=template_ref,
                directory=template_dir,
                output_dir=str(self.flutter_dir.parent),
                no_input=True,
                overwrite_if_exists=True,
                extra_context={
                    k: v for k, v in self.template_data.items() if v is not None
                },
            )
        except Exception as e:
            shutil.rmtree(self.flutter_dir)
            self.cleanup(1, f"{e}")
        console.log(
            f"Created Flutter bootstrap project from {template_url} with ref {template_ref} {self.emojis['checkmark']}"
        )

    def load_pubspec(self):
        assert self.pubspec_path
        assert self.template_data
        assert self.get_pyproject
        assert isinstance(self.flutter_dependencies, dict)

        with open(self.pubspec_path, encoding="utf8") as f:
            self.pubspec = yaml.safe_load(f)

        # merge dependencies to a dest pubspec.yaml
        for k, v in self.flutter_dependencies.items():
            self.pubspec["dependencies"][k] = v

        self.pubspec = merge_dict(
            self.pubspec, self.get_pyproject("tool.flet.flutter.pubspec") or {}
        )

        # make sure project_name is not named as any of the dependencies
        for dep in self.pubspec["dependencies"].keys():
            if dep == self.template_data["project_name"]:
                self.cleanup(
                    1,
                    f"Project name cannot have the same name as one of its dependencies: {dep}. "
                    f"Use --project option to specify a different project name.",
                )

    def customize_icons_and_splash_images(self):
        assert self.package_app_path
        assert self.flutter_dir
        assert self.options
        assert self.get_pyproject
        assert self.pubspec
        assert self.pubspec_path

        self.status.update(
            f"[bold blue]Customizing app icons and splash images {self.emojis['loading']}... "
        )
        self.assets_path = self.package_app_path.joinpath("assets")
        if self.assets_path.exists():
            images_dir = "images"
            images_path = self.flutter_dir.joinpath(images_dir)
            images_path.mkdir(exist_ok=True)

            def fallback_image(yaml_path: str, images: list):
                assert self.pubspec
                d = self.pubspec
                pp = yaml_path.split("/")
                for p in pp[:-1]:
                    d = d[p]
                for image in images:
                    if image:
                        d[pp[-1]] = f"{images_dir}/{image}"
                        return

            # copy icons
            default_icon = self.copy_icon_image(self.assets_path, images_path, "icon")
            ios_icon = self.copy_icon_image(self.assets_path, images_path, "icon_ios")
            android_icon = self.copy_icon_image(
                self.assets_path, images_path, "icon_android"
            )
            web_icon = self.copy_icon_image(self.assets_path, images_path, "icon_web")
            windows_icon = self.copy_icon_image(
                self.assets_path, images_path, "icon_windows"
            )
            macos_icon = self.copy_icon_image(
                self.assets_path, images_path, "icon_macos"
            )

            fallback_image("flutter_launcher_icons/image_path", [default_icon])
            fallback_image(
                "flutter_launcher_icons/image_path_ios", [ios_icon, default_icon]
            )
            fallback_image(
                "flutter_launcher_icons/image_path_android",
                [android_icon, default_icon],
            )
            fallback_image(
                "flutter_launcher_icons/adaptive_icon_foreground",
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
                "flutter_launcher_icons/macos/image_path",
                [macos_icon, default_icon],
            )

            # copy splash images
            default_splash = self.copy_icon_image(
                self.assets_path, images_path, "splash"
            )
            default_dark_splash = self.copy_icon_image(
                self.assets_path, images_path, "splash_dark"
            )
            ios_splash = self.copy_icon_image(
                self.assets_path, images_path, "splash_ios"
            )
            ios_dark_splash = self.copy_icon_image(
                self.assets_path, images_path, "splash_dark_ios"
            )
            android_splash = self.copy_icon_image(
                self.assets_path, images_path, "splash_android"
            )
            android_dark_splash = self.copy_icon_image(
                self.assets_path, images_path, "splash_dark_android"
            )
            web_splash = self.copy_icon_image(
                self.assets_path, images_path, "splash_web"
            )
            web_dark_splash = self.copy_icon_image(
                self.assets_path, images_path, "splash_dark_web"
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
            splash_color = self.options.splash_color or self.get_pyproject(
                "tool.flet.splash.color"
            )
            if splash_color:
                self.pubspec["flutter_native_splash"]["color"] = splash_color
                self.pubspec["flutter_native_splash"]["android_12"][
                    "color"
                ] = splash_color
            splash_dark_color = self.options.splash_dark_color or self.get_pyproject(
                "tool.flet.splash.dark_color"
            )
            if splash_dark_color:
                self.pubspec["flutter_native_splash"]["color_dark"] = splash_dark_color
                self.pubspec["flutter_native_splash"]["android_12"][
                    "color_dark"
                ] = splash_dark_color

        adaptive_icon_background = (
            self.options.android_adaptive_icon_background
            or self.get_pyproject("tool.flet.android.adaptive_icon_background")
        )
        if adaptive_icon_background:
            self.pubspec["flutter_launcher_icons"][
                "adaptive_icon_background"
            ] = adaptive_icon_background

        # enable/disable splashes
        self.pubspec["flutter_native_splash"]["web"] = (
            not self.options.no_web_splash
            if self.options.no_web_splash is not None
            else (
                self.get_pyproject("tool.flet.splash.web")
                if self.get_pyproject("tool.flet.splash.web") is not None
                else True
            )
        )
        self.pubspec["flutter_native_splash"]["ios"] = (
            not self.options.no_ios_splash
            if self.options.no_ios_splash is not None
            else (
                self.get_pyproject("tool.flet.splash.ios")
                if self.get_pyproject("tool.flet.splash.ios") is not None
                else True
            )
        )
        self.pubspec["flutter_native_splash"]["android"] = (
            not self.options.no_android_splash
            if self.options.no_android_splash is not None
            else (
                self.get_pyproject("tool.flet.splash.android")
                if self.get_pyproject("tool.flet.splash.android") is not None
                else True
            )
        )

        # save pubspec.yaml
        with open(self.pubspec_path, "w", encoding="utf8") as f:
            yaml.dump(self.pubspec, f)

        console.log(
            f"Customized app icons and splash images {self.emojis['checkmark']}"
        )

    def generate_icons_and_splash_screens(self):
        assert self.options

        self.status.update(
            f"[bold blue]Generating app icons {self.emojis['loading']}... "
        )
        # icons
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

        # splash screens
        if self.options.target_platform in ["web", "ipa", "apk", "aab"]:
            self.status.update(
                f"[bold blue]Generating splash screens {self.emojis['loading']}... "
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

    def package_python_app(self):
        assert self.options
        assert self.get_pyproject
        assert self.python_app_path
        assert self.build_dir
        assert self.flutter_dir

        self.status.update(
            f"[bold blue]Packaging Python app {self.emojis['loading']}... "
        )
        package_args = [
            self.dart_exe,
            "run",
            "serious_python:main",
            "package",
            str(self.python_app_path),
            "--platform",
            self.package_platform,
        ]

        target_arch = (
            self.options.target_arch
            or self.get_pyproject(f"tool.flet.{self.config_platform}.build_arch")
            or self.get_pyproject("tool.flet.build_arch")
        )
        if target_arch:
            package_args.extend(["--arch", self.options.target_arch])

        package_env = {}

        # requirements
        requirements_txt = self.python_app_path.joinpath("requirements.txt")

        toml_dependencies = get_poetry_dependencies(
            self.get_pyproject("tool.poetry.dependencies")
        ) or get_project_dependencies(self.get_pyproject("project.dependencies"))

        if toml_dependencies:
            package_args.extend(
                [
                    "--requirements",
                    ",".join(toml_dependencies),
                ]
            )
        elif requirements_txt.exists():
            package_args.extend(["--requirements", f"-r,{requirements_txt}"])

        # site-packages variable
        if self.package_platform in ["Android", "iOS"]:
            package_env["SERIOUS_PYTHON_SITE_PACKAGES"] = str(
                self.build_dir / "site-packages"
            )

        # exclude
        exclude_list = ["build"]

        app_exclude = self.options.exclude or self.get_pyproject(
            "tool.flet.app.exclude"
        )
        if app_exclude:
            exclude_list.extend(app_exclude)

        if self.options.target_platform == "web":
            exclude_list.append("assets")
        package_args.extend(["--exclude", ",".join(exclude_list)])

        if (
            self.options.compile_app
            if self.options.compile_app is not None
            else (
                self.get_pyproject("tool.flet.compile.app")
                if self.get_pyproject("tool.flet.compile.app") is not None
                else False
            )
        ):
            package_args.append("--compile-app")

        if (
            self.options.compile_packages
            if self.options.compile_packages is not None
            else (
                self.get_pyproject("tool.flet.compile.packages")
                if self.get_pyproject("tool.flet.compile.packages") is not None
                else False
            )
        ):
            package_args.append("--compile-packages")

        if (
            self.options.cleanup_on_compile
            if self.options.cleanup_on_compile is not None
            else (
                self.get_pyproject("tool.flet.compile.cleanup")
                if self.get_pyproject("tool.flet.compile.cleanup") is not None
                else True
            )
        ):
            package_args.append("--cleanup")

        if self.verbose > 1:
            package_args.append("--verbose")

        package_result = self.run(
            package_args,
            cwd=str(self.flutter_dir),
            env=package_env,
            capture_output=self.verbose < 1,
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

        console.log(f"Packaged Python app {self.emojis['checkmark']}")

    def flutter_build(self):
        assert self.options
        assert self.build_dir
        assert self.get_pyproject
        assert self.template_data

        self.status.update(
            f"[bold blue]Building [cyan]{self.platforms[self.options.target_platform]['status_text']}[/cyan] {self.emojis['loading']}... "
        )
        # flutter build
        build_args = [
            self.flutter_exe,
            "build",
            self.platforms[self.options.target_platform]["flutter_build_command"],
        ]

        build_env = {}

        # site-packages variable
        if self.package_platform in ["Android", "iOS"]:
            build_env["SERIOUS_PYTHON_SITE_PACKAGES"] = str(
                self.build_dir / "site-packages"
            )

        android_signing_key_store = (
            self.options.android_signing_key_store
            or self.get_pyproject("tool.flet.android.signing.key_store")
        )
        if android_signing_key_store:
            build_env["FLET_ANDROID_SIGNING_KEY_STORE"] = android_signing_key_store

        key_store_password = (
            self.options.android_signing_key_store_password
            or os.getenv("FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD")
        )
        key_password = self.options.android_signing_key_password or os.getenv(
            "FLET_ANDROID_SIGNING_KEY_PASSWORD"
        )
        if key_store_password or key_password:
            build_env["FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD"] = (
                key_store_password if key_store_password else key_password
            )
            build_env["FLET_ANDROID_SIGNING_KEY_PASSWORD"] = (
                key_password if key_password else key_store_password
            )

        android_signing_key_alias = (
            self.options.android_signing_key_alias
            or self.get_pyproject("tool.flet.android.signing.key_alias")
        )
        if android_signing_key_alias:
            build_env["FLET_ANDROID_SIGNING_KEY_ALIAS"] = android_signing_key_alias

        if (
            self.options.target_platform in "apk"
            and self.template_data["split_per_abi"]
        ):
            build_args.append("--split-per-abi")

        if (
            self.options.target_platform in ["ipa"]
            and not self.template_data["team_id"]
        ):
            build_args.append("--no-codesign")

        build_number = self.options.build_number or self.get_pyproject(
            "tool.flet.build_number"
        )
        if build_number:
            build_args.extend(["--build-number", str(build_number)])

        build_version = (
            self.options.build_version
            or self.get_pyproject("project.version")
            or self.get_pyproject("tool.poetry.version")
        )
        if build_version:
            build_args.extend(["--build-name", build_version])

        for arg in self.get_pyproject("tool.flet.flutter.build_args") or []:
            build_args.append(arg)

        if self.options.flutter_build_args:
            for flutter_build_arg_arr in self.options.flutter_build_args:
                build_args.extend(flutter_build_arg_arr)

        if self.verbose > 1:
            build_args.append("--verbose")

        build_result = self.run(
            build_args,
            cwd=str(self.flutter_dir),
            env=build_env,
            capture_output=self.verbose < 1,
        )

        if build_result.returncode != 0:
            if build_result.stdout:
                console.log(build_result.stdout)
            if build_result.stderr:
                console.log(build_result.stderr, style=error_style)
            self.cleanup(build_result.returncode, check_flutter_version=True)
        console.log(
            f"Built [cyan]{self.platforms[self.options.target_platform]['status_text']}[/cyan] {self.emojis['checkmark']}",
        )

    def copy_build_output(self):
        assert self.template_data
        assert self.options
        assert self.flutter_dir
        assert self.out_dir
        assert self.assets_path

        self.status.update(
            f"[bold blue]Copying build to [cyan]{self.rel_out_dir}[/cyan] directory {self.emojis['loading']}... ",
        )
        arch = platform.machine().lower()
        if arch in {"x86_64", "amd64"}:
            arch = "x64"
        elif arch in {"arm64", "aarch64"}:
            arch = "arm64"

        for build_output in self.platforms[self.options.target_platform]["outputs"]:
            build_output_dir = (
                str(self.flutter_dir.joinpath(build_output))
                .replace("{arch}", arch)
                .replace("{project_name}", self.template_data["project_name"])
                .replace("{product_name}", self.template_data["product_name"])
            )

            if self.verbose > 0:
                console.log("Copying build output from: " + build_output_dir)

            build_output_glob = os.path.basename(build_output_dir)
            build_output_dir = os.path.dirname(build_output_dir)
            if not os.path.exists(build_output_dir):
                continue

            if self.out_dir.exists():
                shutil.rmtree(str(self.out_dir))
            self.out_dir.mkdir(parents=True, exist_ok=True)

            def ignore_build_output(path, files):
                if path == build_output_dir and build_output_glob != "*":
                    return [f for f in os.listdir(path) if f != build_output_glob]
                return []

            # copy build result to out_dir
            copy_tree(build_output_dir, str(self.out_dir), ignore=ignore_build_output)

        if self.options.target_platform == "web" and self.assets_path.exists():
            # copy `assets` directory contents to the output directory
            copy_tree(str(self.assets_path), str(self.out_dir))

        console.log(
            f"Copied build to [cyan]{self.rel_out_dir}[/cyan] directory {self.emojis['checkmark']}"
        )

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

    def run(self, args, cwd, env: Optional[dict] = None, capture_output=True):
        if is_windows():
            # Source: https://stackoverflow.com/a/77374899/1435891
            # Save the current console output code page and switch to 65001 (UTF-8)
            previousCp = windll.kernel32.GetConsoleOutputCP()
            windll.kernel32.SetConsoleOutputCP(65001)

        if self.verbose > 0:
            console.log(f"Run subprocess: {args}")

        cmd_env = None
        if env is not None:
            cmd_env = os.environ.copy()
            for k, v in env.items():
                cmd_env[k] = v

        r = subprocess.run(
            args,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            encoding="utf8",
            env=cmd_env,
        )

        if is_windows():
            # Restore the previous output console code page.
            windll.kernel32.SetConsoleOutputCP(previousCp)

        return r

    def cleanup(
        self, exit_code: int, message: Optional[str] = None, check_flutter_version=False
    ):
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

            # windows has been reported to raise encoding errors when running `flutter doctor`
            # so skip running `flutter doctor` if no_rich_output is True and platform is Windows
            if not (
                (self.no_rich_output and self.current_platform == "Windows")
                or self.skip_flutter_doctor
            ):
                self.run_flutter_doctor()

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
