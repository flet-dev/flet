import argparse
import glob
import os
import platform
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Optional, cast

import flet.version
import yaml
from flet.utils import cleanup_path, copy_tree, is_windows, slugify
from flet.utils.platform_utils import get_bool_env_var
from flet.version import update_version
from packaging import version
from packaging.requirements import Requirement
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress
from rich.style import Style
from rich.table import Column, Table
from rich.theme import Theme

import flet_cli.utils.processes as processes
from flet_cli.commands.base import BaseCommand
from flet_cli.utils.hash_stamp import HashStamp
from flet_cli.utils.merge import merge_dict
from flet_cli.utils.project_dependencies import (
    get_poetry_dependencies,
    get_project_dependencies,
)
from flet_cli.utils.pyproject_toml import load_pyproject_toml

PYODIDE_ROOT_URL = "https://cdn.jsdelivr.net/pyodide/v0.27.2/full"
DEFAULT_TEMPLATE_URL = "gh:flet-dev/flet-build-template"

MINIMAL_FLUTTER_VERSION = version.Version("3.29.2")

no_rich_output = get_bool_env_var("FLET_CLI_NO_RICH_OUTPUT")

error_style = Style(color="red", bold=True)
warning_style = Style(color="yellow", bold=True)
console = Console(
    log_path=False,
    theme=Theme({"log.message": "green bold"}),
    force_terminal=not no_rich_output,
)
verbose1_style = Style(dim=True, bold=False)
verbose2_style = Style(color="bright_black", bold=False)


class Command(BaseCommand):
    """
    Build an executable app or install bundle.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)

        self.env = {}
        self.pubspec_path = None
        self.rel_out_dir = None
        self.assets_path = None
        self.package_platform = None
        self.config_platform = None
        self.target_platform = None
        self.flutter_dependencies = {}
        self.package_app_path = None
        self.options = None
        self.template_data = None
        self.python_module_filename = None
        self.out_dir = None
        self.python_module_name = None
        self.get_pyproject = None
        self.python_app_path = None
        self.emojis = {}
        self.dart_exe = None
        self.verbose = False
        self.build_dir = None
        self.flutter_dir: Optional[Path] = None
        self.flutter_packages_dir = None
        self.flutter_packages_temp_dir = None
        self.flutter_exe = None
        self.skip_flutter_doctor = get_bool_env_var("FLET_CLI_SKIP_FLUTTER_DOCTOR")
        self.no_rich_output = no_rich_output
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
            nargs="+",
            default=[],
            help="package for specific architectures only. Used with Android and macOS builds only.",
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
            "--bundle-id",
            dest="bundle_id",
            help='bundle ID for the application, e.g. "com.mycompany.app-name" - used as an iOS, Android, macOS and Linux bundle ID',
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
            "--ios-team-id",
            dest="ios_team_id",
            type=str,
            help="team ID to sign iOS bundle (ipa only)",
            required=False,
        )
        parser.add_argument(
            "--ios-export-method",
            dest="ios_export_method",
            type=str,
            help='export method for iOS app. Default is "debugging"',
            required=False,
        )
        parser.add_argument(
            "--ios-provisioning-profile",
            dest="ios_provisioning_profile",
            type=str,
            help="provisioning profile name or UUID that used to sign and export iOS app",
            required=False,
        )
        parser.add_argument(
            "--ios-signing-certificate",
            dest="ios_signing_certificate",
            type=str,
            help="provide a certificate name, SHA-1 hash, or automatic selector to use for signing iOS app bundle",
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
            "--cleanup-app",
            dest="cleanup_app",
            action="store_true",
            default=None,
            help="remove unnecessary app files upon packaging",
        )
        parser.add_argument(
            "--cleanup-app-files",
            dest="cleanup_app_files",
            action="append",
            nargs="*",
            help="the list of globs to delete extra app files and directories",
        )
        parser.add_argument(
            "--cleanup-packages",
            dest="cleanup_packages",
            action="store_true",
            default=None,
            help="remove unnecessary package files upon packaging",
        )
        parser.add_argument(
            "--cleanup-package-files",
            dest="cleanup_package_files",
            action="append",
            nargs="*",
            help="the list of globs to delete extra package files and directories",
        )
        parser.add_argument(
            "--flutter-build-args",
            dest="flutter_build_args",
            action="append",
            nargs="*",
            help="additional arguments for flutter build command",
        )
        parser.add_argument(
            "--source-packages",
            dest="source_packages",
            nargs="+",
            default=[],
            help="the list of Python packages to install from source distributions",
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
        self.status = console.status(
            f"[bold blue]Initializing {self.options.target_platform} build...",
            spinner="bouncingBall",
        )
        self.progress = Progress(transient=True)
        self.no_rich_output = self.no_rich_output or self.options.no_rich_output
        self.verbose = self.options.verbose
        with Live(Group(self.status, self.progress), console=console) as self.live:
            self.initialize_build()
            self.validate_target_platform()
            self.validate_entry_point()
            self.setup_template_data()
            self.create_flutter_project()
            self.package_python_app()
            self.register_flutter_extensions()
            if self.create_flutter_project(second_pass=True):
                self.update_flutter_dependencies()
            self.customize_icons()
            self.customize_splash_images()
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
        self.emojis = {
            "checkmark": "[green]OK[/]" if self.no_rich_output else "✅",
            "loading": "" if self.no_rich_output else "⏳",
            "success": "" if self.no_rich_output else "🥳",
            "directory": "" if self.no_rich_output else "📁",
        }

        self.python_app_path = Path(self.options.python_app_path).resolve()
        self.skip_flutter_doctor = (
            self.skip_flutter_doctor or self.options.skip_flutter_doctor
        )
        self.package_platform = self.platforms[self.options.target_platform][
            "package_platform"
        ]
        self.config_platform = self.platforms[self.options.target_platform][
            "config_platform"
        ]

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

        if (
            not self.flutter_exe
            or not self.dart_exe
            or not self.flutter_version_valid()
        ):
            self.install_flutter()

        if self.verbose > 0:
            console.log("Flutter executable:", self.flutter_exe, style=verbose2_style)
            console.log("Dart executable:", self.dart_exe, style=verbose2_style)

        if self.package_platform == "Android":
            self.install_jdk()
            self.install_android_sdk()

        self.rel_out_dir = self.options.output_dir or os.path.join(
            "build", self.platforms[self.options.target_platform]["dist"]
        )

        self.build_dir = self.python_app_path.joinpath("build")
        self.flutter_dir = self.build_dir.joinpath("flutter")
        self.flutter_packages_dir = self.build_dir.joinpath("flutter-packages")
        self.flutter_packages_temp_dir = self.build_dir.joinpath(
            "flutter-packages-temp"
        )
        self.out_dir = (
            Path(self.options.output_dir).resolve()
            if self.options.output_dir
            else self.python_app_path.joinpath(self.rel_out_dir)
        )
        self.pubspec_path = str(self.flutter_dir.joinpath("pubspec.yaml"))
        self.get_pyproject = load_pyproject_toml(self.python_app_path)

    def flutter_version_valid(self):
        version_results = self.run(
            [
                self.flutter_exe,
                "--version",
                "--no-version-check",
                "--suppress-analytics",
            ],
            cwd=os.getcwd(),
            capture_output=True,
        )
        if version_results.returncode == 0 and version_results.stdout:
            match = re.search(r"Flutter (\d+\.\d+\.\d+)", version_results.stdout)
            if match:
                flutter_version = version.parse(match.group(1))

                # validate installed Flutter version
                return (
                    flutter_version.major == MINIMAL_FLUTTER_VERSION.major
                    and flutter_version.minor == MINIMAL_FLUTTER_VERSION.minor
                )
        else:
            console.log(1, "Failed to validate Flutter version.")
        return False

    def install_flutter(self):
        self.update_status(
            f"[bold blue]Installing Flutter {MINIMAL_FLUTTER_VERSION}..."
        )
        from flet_cli.utils.flutter import install_flutter

        flutter_dir = install_flutter(
            str(MINIMAL_FLUTTER_VERSION), self.log_stdout, progress=self.progress
        )
        ext = ".bat" if platform.system() == "Windows" else ""
        self.flutter_exe = os.path.join(flutter_dir, "bin", f"flutter{ext}")
        self.dart_exe = os.path.join(flutter_dir, "bin", f"dart{ext}")
        path_env = cleanup_path(
            cleanup_path(os.environ.get("PATH", ""), "flutter"), "dart"
        )
        self.env["PATH"] = os.pathsep.join([os.path.join(flutter_dir, "bin"), path_env])

        # desktop mode
        if self.config_platform in ["macos", "windows", "linux"]:
            if self.verbose > 0:
                console.log(
                    f"Ensure Flutter has desktop support enabled",
                    style=verbose1_style,
                )
            config_result = self.run(
                [
                    self.flutter_exe,
                    "config",
                    "--no-version-check",
                    "--suppress-analytics",
                    f"--enable-{self.config_platform}-desktop",
                ],
                cwd=os.getcwd(),
                capture_output=self.verbose < 1,
            )
            if config_result.returncode != 0:
                if config_result.stdout:
                    console.log(config_result.stdout, style=verbose1_style)
                if config_result.stderr:
                    console.log(config_result.stderr, style=error_style)
                self.cleanup(config_result.returncode)

        console.log(
            f"Flutter {MINIMAL_FLUTTER_VERSION} installed {self.emojis['checkmark']}"
        )

    def install_jdk(self):
        from flet_cli.utils.jdk import install_jdk

        self.update_status(f"[bold blue]Installing JDK...")
        jdk_dir = install_jdk(self.log_stdout, progress=self.progress)
        self.env["JAVA_HOME"] = jdk_dir

        # config flutter's JDK dir
        if self.verbose > 0:
            console.log(
                f"Configuring Flutter's path to JDK",
                style=verbose1_style,
            )
        config_result = self.run(
            [
                self.flutter_exe,
                "config",
                "--no-version-check",
                "--suppress-analytics",
                f"--jdk-dir={jdk_dir}",
            ],
            cwd=os.getcwd(),
            capture_output=self.verbose < 1,
        )
        if config_result.returncode != 0:
            if config_result.stdout:
                console.log(config_result.stdout, style=verbose1_style)
            if config_result.stderr:
                console.log(config_result.stderr, style=error_style)
            self.cleanup(config_result.returncode)

        console.log(f"JDK installed {self.emojis['checkmark']}")

    def install_android_sdk(self):
        from flet_cli.utils.android_sdk import AndroidSDK

        self.update_status(f"[bold blue]Installing Android SDK...")
        self.env["ANDROID_HOME"] = AndroidSDK(
            self.env["JAVA_HOME"], self.log_stdout, progress=self.progress
        ).install()
        console.log(f"Android SDK installed {self.emojis['checkmark']}")

    def validate_target_platform(self):
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

    def setup_template_data(self):
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

        target_arch = (
            self.options.target_arch
            or self.get_pyproject(f"tool.flet.{self.config_platform}.target_arch")
            or self.get_pyproject("tool.flet.target_arch")
        )

        ios_export_method = (
            self.options.ios_export_method
            or self.get_pyproject("tool.flet.ios.export_method")
            or "debugging"
        )

        ios_export_method_opts = (
            self.get_pyproject("tool.flet.ios.export_methods").get(ios_export_method)
            if self.get_pyproject("tool.flet.ios.export_methods")
            else {}
        ) or {}

        ios_provisioning_profile = (
            self.options.ios_provisioning_profile
            or self.get_pyproject("tool.flet.ios.provisioning_profile")
            or ios_export_method_opts.get("provisioning_profile")
        )

        ios_signing_certificate = (
            self.options.ios_signing_certificate
            or self.get_pyproject("tool.flet.ios.signing_certificate")
            or ios_export_method_opts.get("signing_certificate")
        )

        ios_export_options = (
            self.get_pyproject("tool.flet.ios.export_options")
            or ios_export_method_opts.get("export_options")
            or {}
        )

        ios_team_id = (
            self.options.ios_team_id
            or self.get_pyproject("tool.flet.ios.team_id")
            or ios_export_method_opts.get("team_id")
        )

        if self.options.target_platform in ["ipa"] and not ios_provisioning_profile:
            console.print(
                Panel(
                    "This build will generate an .xcarchive (Xcode Archive). To produce an .ipa (iOS App Package), please specify a Provisioning Profile.",
                    style=warning_style,
                )
            )

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
            "org_name": self.options.org_name
            or self.get_pyproject(f"tool.flet.{self.config_platform}.org")
            or self.get_pyproject("tool.flet.org"),
            "bundle_id": self.options.bundle_id
            or self.get_pyproject(f"tool.flet.{self.config_platform}.bundle_id")
            or self.get_pyproject("tool.flet.bundle_id"),
            "company_name": (
                self.options.company_name or self.get_pyproject("tool.flet.company")
            ),
            "copyright": self.options.copyright
            or self.get_pyproject("tool.flet.copyright"),
            "ios_export_method": ios_export_method,
            "ios_provisioning_profile": ios_provisioning_profile,
            "ios_signing_certificate": ios_signing_certificate,
            "ios_export_options": ios_export_options,
            "ios_team_id": ios_team_id,
            "options": {
                "package_platform": self.package_platform,
                "config_platform": self.config_platform,
                "target_arch": (
                    target_arch
                    if isinstance(target_arch, list)
                    else [target_arch]
                    if isinstance(target_arch, str)
                    else []
                ),
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
            "pyproject": self.get_pyproject(),
        }

    def create_flutter_project(self, second_pass=False):
        assert self.options
        assert self.get_pyproject
        assert self.flutter_dir
        assert self.template_data
        assert self.build_dir
        assert self.pubspec_path

        hash = HashStamp(
            self.build_dir / ".hash" / f"template-{'2' if second_pass else '1'}"
        )

        template_url = (
            self.options.template
            or self.get_pyproject("tool.flet.template.url")
            or DEFAULT_TEMPLATE_URL
        )
        hash.update(template_url)

        template_ref = self.options.template_ref or self.get_pyproject(
            "tool.flet.template.ref"
        )
        if not template_ref:
            template_ref = (
                version.Version(flet.version.version).base_version
                if flet.version.version
                else update_version()
            )
        hash.update(template_ref)

        template_dir = self.options.template_dir or self.get_pyproject(
            "tool.flet.template.dir"
        )
        hash.update(template_dir)
        hash.update(self.template_data)

        hash_changed = hash.has_changed()

        if hash_changed:
            # if options.clear_cache is set, delete any existing Flutter bootstrap project directory
            if (
                self.options.clear_cache
                and self.flutter_dir.exists()
                and not second_pass
            ):
                if self.verbose > 1:
                    console.log(f"Deleting {self.flutter_dir}", style=verbose2_style)
                shutil.rmtree(self.flutter_dir, ignore_errors=True)

            # create a new Flutter bootstrap project directory, if non-existent
            if not second_pass:
                self.flutter_dir.mkdir(parents=True, exist_ok=True)
                self.update_status(
                    f'[bold blue]Creating Flutter bootstrap project from {template_url} with ref "{template_ref}"...'
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

            pyproject_pubspec = self.get_pyproject("tool.flet.flutter.pubspec")

            if pyproject_pubspec:
                pubspec = self.load_yaml(self.pubspec_path)
                pubspec = merge_dict(pubspec, pyproject_pubspec)
                self.save_yaml(self.pubspec_path, pubspec)

            # make backup of pubspec.yaml
            shutil.copyfile(self.pubspec_path, f"{self.pubspec_path}.orig")

            if not second_pass:
                console.log(
                    f"Created Flutter bootstrap project from {template_url} with ref \"{template_ref}\" {self.emojis['checkmark']}"
                )

        hash.commit()

        return hash_changed

    def register_flutter_extensions(self):
        assert self.flutter_packages_dir
        assert self.flutter_packages_temp_dir
        assert isinstance(self.flutter_dependencies, dict)
        assert self.template_data
        assert self.build_dir

        if self.flutter_packages_temp_dir.exists():
            # copy packages from temp to permanent location
            if self.flutter_packages_dir.exists():
                shutil.rmtree(self.flutter_packages_dir, ignore_errors=True)
            shutil.move(self.flutter_packages_temp_dir, self.flutter_packages_dir)

        if self.flutter_packages_dir.exists():
            self.update_status(f"[bold blue]Registering Flutter user extensions...")

            for fp in os.listdir(self.flutter_packages_dir):
                if (self.flutter_packages_dir / fp / "pubspec.yaml").exists():
                    ext_dir = str(self.flutter_packages_dir / fp)
                    if self.verbose > 0:
                        console.log(f"Found Flutter extension at {ext_dir}")
                    self.flutter_dependencies[fp] = {"path": ext_dir}

            self.template_data["flutter"]["dependencies"] = list(
                self.flutter_dependencies.keys()
            )

            console.log(
                f"Registered Flutter user extensions {self.emojis['checkmark']}"
            )

    def update_flutter_dependencies(self):
        assert self.pubspec_path
        assert self.template_data
        assert self.get_pyproject
        assert self.build_dir
        assert isinstance(self.flutter_dependencies, dict)

        pubspec = self.load_yaml(self.pubspec_path)

        # merge dependencies to a dest pubspec.yaml
        for k, v in self.flutter_dependencies.items():
            pubspec["dependencies"][k] = v

        # make sure project_name is not named as any of the dependencies
        for dep in pubspec["dependencies"].keys():
            if dep == self.template_data["project_name"]:
                self.cleanup(
                    1,
                    f"Project name cannot have the same name as one of its dependencies: {dep}. "
                    f"Use --project option to specify a different project name.",
                )

        self.save_yaml(self.pubspec_path, pubspec)

    def customize_icons(self):
        assert self.package_app_path
        assert self.flutter_dir
        assert self.options
        assert self.get_pyproject
        assert self.pubspec_path
        assert self.build_dir

        hash = HashStamp(self.build_dir / ".hash" / "icons")

        pubspec_origin_path = f"{self.pubspec_path}.orig"
        pubspec = self.load_yaml(pubspec_origin_path)

        copy_ops = []
        self.assets_path = self.package_app_path.joinpath("assets")
        if self.assets_path.exists():

            images_dir = "images"
            images_path = self.flutter_dir.joinpath(images_dir)
            images_path.mkdir(exist_ok=True)

            # copy icons
            default_icon = self.find_platform_image(
                self.assets_path, images_path, "icon", copy_ops, hash
            )
            ios_icon = self.find_platform_image(
                self.assets_path, images_path, "icon_ios", copy_ops, hash
            )
            android_icon = self.find_platform_image(
                self.assets_path, images_path, "icon_android", copy_ops, hash
            )
            web_icon = self.find_platform_image(
                self.assets_path, images_path, "icon_web", copy_ops, hash
            )
            windows_icon = self.find_platform_image(
                self.assets_path, images_path, "icon_windows", copy_ops, hash
            )
            macos_icon = self.find_platform_image(
                self.assets_path, images_path, "icon_macos", copy_ops, hash
            )

            self.fallback_image(
                pubspec, "flutter_launcher_icons.image_path", [default_icon], images_dir
            )
            self.fallback_image(
                pubspec,
                "flutter_launcher_icons.image_path_ios",
                [ios_icon, default_icon],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_launcher_icons.image_path_android",
                [android_icon, default_icon],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_launcher_icons.adaptive_icon_foreground",
                [android_icon, default_icon],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_launcher_icons.web.image_path",
                [web_icon, default_icon],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_launcher_icons.windows.image_path",
                [windows_icon, default_icon],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_launcher_icons.macos.image_path",
                [macos_icon, default_icon],
                images_dir,
            )

        adaptive_icon_background = (
            self.options.android_adaptive_icon_background
            or self.get_pyproject("tool.flet.android.adaptive_icon_background")
        )
        if adaptive_icon_background:
            pubspec["flutter_launcher_icons"][
                "adaptive_icon_background"
            ] = adaptive_icon_background

        # check if pubspec changed
        hash.update(Path(pubspec_origin_path).stat().st_mtime)
        hash.update(pubspec["flutter_launcher_icons"])

        # save pubspec.yaml
        if hash.has_changed():

            if copy_ops:
                self.update_status(f"[bold blue]Customizing app icons...")
                for op in copy_ops:
                    if self.verbose > 0:
                        console.log(
                            f"Copying image {op[0]} to {op[1]}", style=verbose1_style
                        )
                    shutil.copy(op[0], op[1])
                console.log(f"Customized app icons {self.emojis['checkmark']}")

            updated_pubspec = self.load_yaml(self.pubspec_path)
            updated_pubspec["flutter_launcher_icons"] = pubspec[
                "flutter_launcher_icons"
            ]
            self.save_yaml(self.pubspec_path, updated_pubspec)

            self.update_status(f"[bold blue]Generating app icons...")

            # icons
            icons_result = self.run(
                [
                    self.dart_exe,
                    "run",
                    "--suppress-analytics",
                    "flutter_launcher_icons",
                ],
                cwd=str(self.flutter_dir),
                capture_output=self.verbose < 1,
            )
            if icons_result.returncode != 0:
                if icons_result.stdout:
                    console.log(icons_result.stdout, style=verbose1_style)
                if icons_result.stderr:
                    console.log(icons_result.stderr, style=error_style)
                self.cleanup(icons_result.returncode)
            console.log(f"Generated app icons {self.emojis['checkmark']}")

        hash.commit()

    def customize_splash_images(self):
        assert self.package_app_path
        assert self.flutter_dir
        assert self.options
        assert self.get_pyproject
        assert self.pubspec_path
        assert self.build_dir

        if not self.options.target_platform in ["web", "ipa", "apk", "aab"]:
            return

        hash = HashStamp(self.build_dir / ".hash" / "splashes")

        pubspec_origin_path = f"{self.pubspec_path}.orig"

        pubspec = self.load_yaml(pubspec_origin_path)

        copy_ops = []
        self.assets_path = self.package_app_path.joinpath("assets")
        if self.assets_path.exists():

            images_dir = "images"
            images_path = self.flutter_dir.joinpath(images_dir)
            images_path.mkdir(exist_ok=True)

            # copy icons
            default_icon = self.find_platform_image(
                self.assets_path, images_path, "icon", copy_ops, hash
            )

            # copy splash images
            default_splash = self.find_platform_image(
                self.assets_path, images_path, "splash", copy_ops, hash
            )
            default_dark_splash = self.find_platform_image(
                self.assets_path, images_path, "splash_dark", copy_ops, hash
            )
            ios_splash = self.find_platform_image(
                self.assets_path, images_path, "splash_ios", copy_ops, hash
            )
            ios_dark_splash = self.find_platform_image(
                self.assets_path, images_path, "splash_dark_ios", copy_ops, hash
            )
            android_splash = self.find_platform_image(
                self.assets_path, images_path, "splash_android", copy_ops, hash
            )
            android_dark_splash = self.find_platform_image(
                self.assets_path, images_path, "splash_dark_android", copy_ops, hash
            )
            web_splash = self.find_platform_image(
                self.assets_path, images_path, "splash_web", copy_ops, hash
            )
            web_dark_splash = self.find_platform_image(
                self.assets_path, images_path, "splash_dark_web", copy_ops, hash
            )
            self.fallback_image(
                pubspec,
                "flutter_native_splash.image",
                [default_splash, default_icon],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_native_splash.image_dark",
                [default_dark_splash, default_splash, default_icon],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_native_splash.image_ios",
                [ios_splash, default_splash, default_icon],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_native_splash.image_dark_ios",
                [
                    ios_dark_splash,
                    default_dark_splash,
                    ios_splash,
                    default_splash,
                    default_icon,
                ],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_native_splash.image_android",
                [android_splash, default_splash, default_icon],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_native_splash.android_12.image",
                [android_splash, default_splash, default_icon],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_native_splash.image_dark_android",
                [
                    android_dark_splash,
                    default_dark_splash,
                    android_splash,
                    default_splash,
                    default_icon,
                ],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_native_splash.android_12.image_dark",
                [
                    android_dark_splash,
                    default_dark_splash,
                    android_splash,
                    default_splash,
                    default_icon,
                ],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_native_splash.image_web",
                [web_splash, default_splash, default_icon],
                images_dir,
            )
            self.fallback_image(
                pubspec,
                "flutter_native_splash.image_dark_web",
                [
                    web_dark_splash,
                    default_dark_splash,
                    web_splash,
                    default_splash,
                    default_icon,
                ],
                images_dir,
            )

        # splash colors
        splash_color = (
            self.options.splash_color
            or self.get_pyproject(f"tool.flet.{self.config_platform}.splash.color")
            or self.get_pyproject("tool.flet.splash.color")
        )
        if splash_color:
            pubspec["flutter_native_splash"]["color"] = splash_color
            pubspec["flutter_native_splash"]["android_12"]["color"] = splash_color

        splash_dark_color = (
            self.options.splash_dark_color
            or self.get_pyproject(f"tool.flet.{self.config_platform}.splash.dark_color")
            or self.get_pyproject("tool.flet.splash.dark_color")
        )
        if splash_dark_color:
            pubspec["flutter_native_splash"]["color_dark"] = splash_dark_color
            pubspec["flutter_native_splash"]["android_12"][
                "color_dark"
            ] = splash_dark_color

        splash_icon_bgcolor = self.get_pyproject(
            f"tool.flet.{self.config_platform}.splash.icon_bgcolor"
        ) or self.get_pyproject("tool.flet.splash.icon_bgcolor")

        if splash_icon_bgcolor:
            pubspec["flutter_native_splash"]["android_12"][
                "icon_background_color"
            ] = splash_icon_bgcolor

        splash_icon_dark_bgcolor = self.get_pyproject(
            f"tool.flet.{self.config_platform}.splash.icon_dark_bgcolor"
        ) or self.get_pyproject("tool.flet.splash.icon_dark_bgcolor")

        if splash_icon_dark_bgcolor:
            pubspec["flutter_native_splash"]["android_12"][
                "icon_background_color_dark"
            ] = splash_icon_dark_bgcolor

        # enable/disable splashes
        pubspec["flutter_native_splash"]["web"] = (
            not self.options.no_web_splash
            if self.options.no_web_splash is not None
            else (
                self.get_pyproject("tool.flet.splash.web")
                if self.get_pyproject("tool.flet.splash.web") is not None
                else True
            )
        )
        pubspec["flutter_native_splash"]["ios"] = (
            not self.options.no_ios_splash
            if self.options.no_ios_splash is not None
            else (
                self.get_pyproject("tool.flet.splash.ios")
                if self.get_pyproject("tool.flet.splash.ios") is not None
                else True
            )
        )
        pubspec["flutter_native_splash"]["android"] = (
            not self.options.no_android_splash
            if self.options.no_android_splash is not None
            else (
                self.get_pyproject("tool.flet.splash.android")
                if self.get_pyproject("tool.flet.splash.android") is not None
                else True
            )
        )

        # check if pubspec changed
        hash.update(Path(pubspec_origin_path).stat().st_mtime)
        hash.update(pubspec["flutter_native_splash"])

        # save pubspec.yaml
        if hash.has_changed():

            if copy_ops:
                self.update_status(f"[bold blue]Customizing app splash images...")
                for op in copy_ops:
                    if self.verbose > 0:
                        console.log(
                            f"Copying image {op[0]} to {op[1]}", style=verbose1_style
                        )
                    shutil.copy(op[0], op[1])
                console.log(f"Customized app splash images {self.emojis['checkmark']}")

            updated_pubspec = self.load_yaml(self.pubspec_path)
            updated_pubspec["flutter_native_splash"] = pubspec["flutter_native_splash"]
            self.save_yaml(self.pubspec_path, updated_pubspec)

            # splash screens
            self.update_status(f"[bold blue]Generating splash screens...")
            splash_result = self.run(
                [
                    self.dart_exe,
                    "run",
                    "--suppress-analytics",
                    "flutter_native_splash:create",
                ],
                cwd=str(self.flutter_dir),
                capture_output=self.verbose < 1,
            )
            if splash_result.returncode != 0:
                if splash_result.stdout:
                    console.log(splash_result.stdout, style=verbose1_style)
                if splash_result.stderr:
                    console.log(splash_result.stderr, style=error_style)
                self.cleanup(splash_result.returncode)
            console.log(f"Generated splash screens {self.emojis['checkmark']}")

        hash.commit()

    def fallback_image(self, pubspec, yaml_path: str, images: list, images_dir: str):
        d = pubspec
        pp = yaml_path.split(".")
        for p in pp[:-1]:
            d = d[p]
        for image in images:
            if image:
                d[pp[-1]] = f"{images_dir}/{image}"
                return

    def package_python_app(self):
        assert self.options
        assert self.get_pyproject
        assert self.python_app_path
        assert self.package_app_path
        assert self.build_dir
        assert self.flutter_dir
        assert self.flutter_packages_dir
        assert self.flutter_packages_temp_dir
        assert self.template_data

        hash = HashStamp(self.build_dir / ".hash" / "package")

        self.update_status(f"[bold blue]Packaging Python app...")
        package_args = [
            self.dart_exe,
            "run",
            "--suppress-analytics",
            "serious_python:main",
            "package",
            str(self.package_app_path),
            "--platform",
            self.package_platform,
        ]

        if self.template_data["options"]["target_arch"]:
            package_args.extend(
                ["--arch"] + self.template_data["options"]["target_arch"]
            )

        package_env = {}

        # requirements
        requirements_txt = self.python_app_path.joinpath("requirements.txt")

        toml_dependencies = (
            get_poetry_dependencies(self.get_pyproject("tool.poetry.dependencies"))
            or get_project_dependencies(self.get_pyproject("project.dependencies"))
            or []
        )

        platform_dependencies = get_project_dependencies(
            self.get_pyproject(f"tool.flet.{self.config_platform}.dependencies")
        )
        if platform_dependencies:
            toml_dependencies.extend(platform_dependencies)

        dev_packages_configured = False
        if len(toml_dependencies) > 0:
            dev_packages = (
                self.get_pyproject(f"tool.flet.{self.config_platform}.dev_packages")
                or self.get_pyproject(f"tool.flet.dev_packages")
                or []
            )
            if len(dev_packages) > 0:
                for i in range(0, len(toml_dependencies)):
                    package_name = Requirement(toml_dependencies[i]).name
                    if package_name in dev_packages:
                        dev_path = Path(dev_packages[package_name])
                        if not dev_path.is_absolute():
                            dev_path = (self.python_app_path / dev_path).resolve()
                        toml_dependencies[i] = f"{package_name} @ file://{dev_path}"
                        dev_packages_configured = True
                if dev_packages_configured:
                    toml_dependencies.append("--no-cache-dir")

            for toml_dep in toml_dependencies:
                package_args.extend(["-r", toml_dep])

        elif requirements_txt.exists():
            if self.verbose > 1:
                with open(requirements_txt, "r", encoding="utf-8") as f:
                    reqs_txt_contents = f.read()
                    console.log(
                        f"Contents of requirements.txt: {reqs_txt_contents}",
                        style=verbose2_style,
                    )
                    hash.update(reqs_txt_contents)
            package_args.extend(["-r", "-r", "-r", str(requirements_txt)])
        else:
            flet_version = (
                flet.version.version if flet.version.version else update_version()
            )
            package_args.extend(["-r", f"flet=={flet_version}"])

        # site-packages variable
        if self.package_platform != "Pyodide":
            package_env["SERIOUS_PYTHON_SITE_PACKAGES"] = str(
                self.build_dir / "site-packages"
            )

        # flutter-packages variable
        if self.flutter_packages_temp_dir.exists():
            shutil.rmtree(self.flutter_packages_temp_dir)

        package_env["SERIOUS_PYTHON_FLUTTER_PACKAGES"] = str(
            self.flutter_packages_temp_dir
        )

        # exclude
        exclude_list = ["build"]

        app_exclude = (
            self.options.exclude
            or self.get_pyproject(f"tool.flet.{self.config_platform}.app.exclude")
            or self.get_pyproject("tool.flet.app.exclude")
        )
        if app_exclude:
            exclude_list.extend(app_exclude)

        if self.options.target_platform == "web":
            exclude_list.append("assets")
        package_args.extend(["--exclude", ",".join(exclude_list)])

        # source-packages
        source_packages = (
            self.options.source_packages
            or self.get_pyproject(f"tool.flet.{self.config_platform}.source_packages")
            or self.get_pyproject("tool.flet.source_packages")
        )
        if source_packages:
            package_env["SERIOUS_PYTHON_ALLOW_SOURCE_DISTRIBUTIONS"] = ",".join(
                source_packages
            )

        if self.get_bool_setting(self.options.compile_app, "compile.app", False):
            package_args.append("--compile-app")

        if self.get_bool_setting(
            self.options.compile_packages, "compile.packages", False
        ):
            package_args.append("--compile-packages")

        cleanup_app = self.get_bool_setting(
            self.options.cleanup_app, "cleanup.app", False
        )
        cleanup_packages = self.get_bool_setting(
            self.options.cleanup_packages, "cleanup.packages", True
        )

        # TODO: should be depreacted
        if self.get_bool_setting(None, "compile.cleanup", False):
            cleanup_app = cleanup_packages = True

        if cleanup_app_files := (
            self.options.cleanup_app_files
            or self.get_pyproject(f"tool.flet.{self.config_platform}.cleanup.app_files")
            or self.get_pyproject("tool.flet.cleanup.app_files")
        ):
            package_args.extend(["--cleanup-app-files", ",".join(cleanup_app_files)])
            cleanup_app = True

        if cleanup_package_files := (
            self.options.cleanup_package_files
            or self.get_pyproject(
                f"tool.flet.{self.config_platform}.cleanup.package_files"
            )
            or self.get_pyproject("tool.flet.cleanup.package_files")
        ):
            package_args.extend(
                ["--cleanup-package-files", ",".join(cleanup_package_files)]
            )
            cleanup_packages = True

        if cleanup_app:
            package_args.append("--cleanup-app")

        if cleanup_packages:
            package_args.append("--cleanup-packages")

        if self.verbose > 1:
            package_args.append("--verbose")

        # check if site-packages installation could be skipped
        for arg in package_args:
            hash.update(arg)

        if not dev_packages_configured:
            if not hash.has_changed():
                package_args.append("--skip-site-packages")
            else:
                if self.flutter_packages_dir.exists():
                    shutil.rmtree(self.flutter_packages_dir, ignore_errors=True)

        package_result = self.run(
            package_args,
            cwd=str(self.flutter_dir),
            env=package_env,
            capture_output=self.verbose < 1,
        )

        if package_result.returncode != 0:
            if package_result.stdout:
                console.log(package_result.stdout, style=verbose1_style)
            if package_result.stderr:
                console.log(package_result.stderr, style=error_style)
            self.cleanup(package_result.returncode)

        hash.commit()

        # make sure app/app.zip exists
        app_zip_path = self.flutter_dir.joinpath("app", "app.zip")
        if not os.path.exists(app_zip_path):
            self.cleanup(1, "Flet app package app/app.zip was not created.")

        console.log(f"Packaged Python app {self.emojis['checkmark']}")

    def get_bool_setting(self, cli_option, pyproj_setting, default_value):
        assert self.get_pyproject
        return (
            cli_option
            if cli_option is not None
            else (
                self.get_pyproject(f"tool.flet.{self.config_platform}.{pyproj_setting}")
                if self.get_pyproject(
                    f"tool.flet.{self.config_platform}.{pyproj_setting}"
                )
                is not None
                else (
                    self.get_pyproject(f"tool.flet.{pyproj_setting}")
                    if self.get_pyproject(f"tool.flet.{pyproj_setting}") is not None
                    else default_value
                )
            )
        )

    def flutter_build(self):
        assert self.options
        assert self.build_dir
        assert self.get_pyproject
        assert self.template_data

        self.update_status(
            f"[bold blue]Building [cyan]{self.platforms[self.options.target_platform]['status_text']}[/cyan]..."
        )
        # flutter build
        build_args = [
            self.flutter_exe,
            "build",
            self.platforms[self.options.target_platform]["flutter_build_command"],
            "--no-version-check",
            "--suppress-analytics",
        ]

        build_env = {}

        # site-packages variable
        if self.package_platform != "Pyodide":
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

        if self.options.target_platform in ["ipa"]:
            if self.template_data["ios_provisioning_profile"]:
                build_args.extend(
                    [
                        "--export-options-plist",
                        "ios/exportOptions.plist",
                    ]
                )
            else:
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

        if (
            build_result.returncode != 0
            or "Encountered error while creating the IPA" in str(build_result.stderr)
        ):
            if build_result.stdout:
                console.log(build_result.stdout, style=verbose1_style)
            if build_result.stderr:
                console.log(build_result.stderr, style=error_style)
            self.cleanup(build_result.returncode if build_result.returncode else 1)
        console.log(
            f"Built [cyan]{self.platforms[self.options.target_platform]['status_text']}[/cyan] {self.emojis['checkmark']}",
        )

    def copy_build_output(self):
        assert self.template_data
        assert self.options
        assert self.flutter_dir
        assert self.out_dir
        assert self.assets_path

        self.update_status(
            f"[bold blue]Copying build to [cyan]{self.rel_out_dir}[/cyan] directory...",
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
                console.log(
                    "Copying build output from: " + build_output_dir,
                    style=verbose1_style,
                )

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

    def find_platform_image(
        self,
        src_path: Path,
        dest_path: Path,
        image_name: str,
        copy_ops: list,
        hash: HashStamp,
    ):
        images = glob.glob(str(src_path.joinpath(f"{image_name}.*")))
        if len(images) > 0:
            if self.verbose > 0:
                console.log(
                    f'Found "{image_name}" image at {images[0]}', style=verbose1_style
                )
            copy_ops.append((images[0], dest_path))
            hash.update(images[0])
            hash.update(Path(images[0]).stat().st_mtime)
            return Path(images[0]).name
        return None

    def find_flutter_batch(self, exe_filename: str):
        batch_path = shutil.which(exe_filename)
        if not batch_path:
            return None
        if is_windows() and batch_path.endswith(".file"):
            return batch_path.replace(".file", ".bat")
        return batch_path

    def run(self, args, cwd, env: Optional[dict] = None, capture_output=True):

        if self.verbose > 0:
            console.log(f"Run subprocess: {args}", style=verbose1_style)

        return processes.run(
            args,
            cwd,
            env={**self.env, **env} if env else self.env,
            capture_output=capture_output,
            log=self.log_stdout,
        )

    def cleanup(self, exit_code: int, message: Optional[str] = None):
        if exit_code == 0:
            msg = message or f"Success! {self.emojis['success']}"
            self.live.update(Panel(msg), refresh=True)
        else:
            msg = (
                message
                if message is not None
                else "Error building Flet app - see the log of failed command above."
            )

            # windows has been reported to raise encoding errors when running `flutter doctor`
            # so skip running `flutter doctor` if no_rich_output is True and platform is Windows
            if not (
                (self.no_rich_output and self.current_platform == "Windows")
                or self.skip_flutter_doctor
            ):
                status = console.status(
                    f"[bold blue]Running Flutter doctor...",
                    spinner="bouncingBall",
                )
                self.live.update(
                    Group(Panel(msg, style=error_style), status), refresh=True
                )
                self.run_flutter_doctor()
            self.live.update(Panel(msg, style=error_style), refresh=True)

        sys.exit(exit_code)

    def run_flutter_doctor(self):
        flutter_doctor = self.run(
            [self.flutter_exe, "doctor", "--no-version-check", "--suppress-analytics"],
            cwd=os.getcwd(),
            capture_output=True,
        )
        if flutter_doctor.returncode == 0 and flutter_doctor.stdout:
            console.log(flutter_doctor.stdout, style=verbose1_style)

    def update_status(self, status):
        if self.no_rich_output:
            console.log(status)
        else:
            self.status.update(status)

    def log_stdout(self, message):
        if self.verbose > 0:
            console.log(
                message,
                end="",
                style=verbose2_style,
                markup=False,
            )

    def load_yaml(self, path):
        with open(str(path), encoding="utf-8") as f:
            return yaml.safe_load(f)

    def save_yaml(self, path, doc):
        with open(str(path), "w", encoding="utf-8") as f:
            yaml.dump(doc, f)
