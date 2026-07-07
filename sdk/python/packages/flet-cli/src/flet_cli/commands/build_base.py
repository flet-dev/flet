import argparse
import base64
import copy
import glob
import json
import os
import platform
import shutil
from pathlib import Path
from typing import Optional, cast

import yaml
from packaging.requirements import Requirement
from rich.panel import Panel
from rich.table import Column, Table

import flet.version
import flet_cli.utils.processes as processes
from flet.utils import copy_tree, slugify
from flet.utils.deprecated import deprecated_warning
from flet_cli.commands.flutter_base import (
    BaseFlutterCommand,
    console,
    error_style,
    verbose1_style,
    verbose2_style,
    warning_style,
)
from flet_cli.utils.android import (
    ANDROID_ARCH_TO_FLUTTER_TARGET_PLATFORM,
    excluded_android_abis,
)
from flet_cli.utils.cli import parse_cli_bool_value
from flet_cli.utils.hash_stamp import HashStamp
from flet_cli.utils.merge import merge_dict
from flet_cli.utils.plist import is_supported_plist_value, parse_cli_plist_value
from flet_cli.utils.project_dependencies import (
    get_poetry_dependencies,
    get_project_dependencies,
)
from flet_cli.utils.pyproject_toml import load_pyproject_toml
from flet_cli.utils.python_versions import (
    UnsupportedPythonVersionError,
    resolve_python_version,
)

DEFAULT_TEMPLATE_URL = (
    "https://github.com/flet-dev/flet/releases/download/"
    "v{version}/flet-build-template.zip"
)

# Android (serious_python native-mmap packaging): pure Python ships in stored zips
# read via zipimport, which breaks packages that read bundled data through a real
# filesystem path (__file__ / pkg_resources) instead of importlib.resources. Such
# packages are shipped extracted to disk via --android-extract-packages or
# [tool.flet.android].extract_packages.
#
# The default set is empty: the common offenders read their data via
# importlib.resources, which is zip-safe (e.g. certifi.where() works from the zip —
# importlib.resources.as_file() extracts cacert.pem to a temp file on demand). Add
# real offenders here as they are found.
ANDROID_DEFAULT_EXTRACT_PACKAGES: list[str] = []


class BaseBuildCommand(BaseFlutterCommand):
    """
    A base build-related CLI command.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)

        self.pubspec_path = None
        self.rel_out_dir = None
        self.assets_path = None
        self.target_platform = None
        self.package_platform = None
        self.config_platform = None
        self.debug_platform = None
        self.flutter_dependencies = {}
        self.package_app_path = None
        self.template_data = None
        self.python_module_filename = None
        self.out_dir = None
        self.python_module_name = None
        self.get_pyproject = None
        self.python_app_path = None
        self.build_dir = None
        self.flutter_dir: Optional[Path] = None
        self.flutter_packages_dir = None
        self.flutter_packages_temp_dir = None
        self.site_packages_skipped = False
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
                "outputs": ["build/macos/Build/Products/Release/{artifact_name}.app"],
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
                "package_platform": "Emscripten",
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
            "ios-simulator": {
                "package_platform": "iOS",
                "config_platform": "ios",
                "flutter_build_command": "ios",
                "status_text": ".app bundle for iOS Simulator",
                "outputs": ["build/ios/iphonesimulator/*"],
                "dist": "ios-simulator",
                "can_be_run_on": ["Darwin"],
            },
        }

        self.cross_platform_permissions = {
            "location": {
                "ios_info_plist": {
                    "NSLocationWhenInUseUsageDescription": "This app uses location service when in use.",  # noqa: E501
                    "NSLocationAlwaysAndWhenInUseUsageDescription": "This app uses location service.",  # noqa: E501
                },
                "macos_info_plist": {
                    "NSLocationUsageDescription": "This app needs access to your location.",  # noqa: E501
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
                "ios_info_plist": {
                    "NSCameraUsageDescription": "This app uses the camera to capture photos and videos."  # noqa: E501
                },
                "macos_info_plist": {
                    "NSCameraUsageDescription": "This app uses the camera to capture photos and videos."  # noqa: E501
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
                "ios_info_plist": {
                    "NSMicrophoneUsageDescription": "This app uses microphone to record sounds.",  # noqa: E501
                },
                "macos_info_plist": {
                    "NSMicrophoneUsageDescription": "This app uses microphone to record sounds.",  # noqa: E501
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
                "ios_info_plist": {
                    "NSPhotoLibraryUsageDescription": "This app saves photos and videos to the photo library."  # noqa: E501
                },
                "macos_info_plist": {
                    "NSPhotoLibraryUsageDescription": "This app saves photos and videos to the photo library."  # noqa: E501
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
        """
        Register shared build arguments used by all concrete build commands.

        Args:
            parser: Argument parser configured by the command runner.
        """

        parser.add_argument(
            "python_app_path",
            type=str,
            nargs="?",
            default=".",
            help="Path to a directory with a Flet Python program",
        )
        parser.add_argument(
            "--arch",
            dest="target_arch",
            action="extend",
            nargs="+",
            default=[],
            help="Build for specific CPU architectures "
            "(used in macOS and Android builds only). "
            "Android: arm64-v8a, armeabi-v7a, x86_64; macOS: arm64, x64. "
            "Example: `--arch arm64-v8a`",
        )
        parser.add_argument(
            "--exclude",
            dest="exclude",
            action="extend",
            nargs="+",
            default=[],
            help="Files and/or directories to exclude from the package"
            "; can be used multiple times",
        )
        parser.add_argument(
            "--clear-cache",
            dest="clear_cache",
            action="store_true",
            default=None,
            help="Remove any existing build cache before starting the build process. "
            "Deprecated: use the `flet clean` command instead",
        )
        parser.add_argument(
            "--project",
            dest="project_name",
            required=False,
            help="Project name for bundle IDs and identifiers; used as the default "
            "for artifact and product names",
        )
        parser.add_argument(
            "--artifact",
            dest="artifact_name",
            required=False,
            help="Executable or bundle name on disk",
        )
        parser.add_argument(
            "--description",
            dest="description",
            required=False,
            help="Short description of the application",
        )
        parser.add_argument(
            "--product",
            dest="product_name",
            required=False,
            help="Display name shown in app launchers, window titles, "
            "and about dialogs.",
        )
        parser.add_argument(
            "--org",
            dest="org_name",
            required=False,
            help="Organization name in reverse domain name notation, "
            "e.g. `com.mycompany`, combined with project name and "
            "used in bundle IDs and signing",
        )
        parser.add_argument(
            "--bundle-id",
            dest="bundle_id",
            required=False,
            help="Bundle ID for the application, e.g. `com.mycompany.app-name`. "
            "It is used as an iOS, Android, macOS and Linux bundle ID",
        )
        parser.add_argument(
            "--company",
            dest="company_name",
            required=False,
            help="Company name to display in about app dialogs",
        )
        parser.add_argument(
            "--copyright",
            dest="copyright",
            required=False,
            help="Copyright text to display in about app dialogs",
        )
        parser.add_argument(
            "--android-adaptive-icon-background",
            dest="android_adaptive_icon_background",
            required=False,
            help="The color to be used to fill out the background of "
            "Android adaptive icons",
        )
        parser.add_argument(
            "--splash-color",
            dest="splash_color",
            required=False,
            help="Background color of app splash screen on iOS, Android and web",
        )
        parser.add_argument(
            "--splash-dark-color",
            dest="splash_dark_color",
            required=False,
            help="Background color in dark mode of app splash screen on "
            "iOS, Android and web",
        )
        parser.add_argument(
            "--no-web-splash",
            dest="no_web_splash",
            action="store_true",
            default=None,
            help="Disable splash screen on web platform",
        )
        parser.add_argument(
            "--no-ios-splash",
            dest="no_ios_splash",
            action="store_true",
            default=None,
            help="Disable splash screen on iOS platform",
        )
        parser.add_argument(
            "--no-android-splash",
            dest="no_android_splash",
            action="store_true",
            default=None,
            help="Disable splash screen on Android platform",
        )
        parser.add_argument(
            "--ios-team-id",
            dest="ios_team_id",
            type=str,
            help="Apple developer team ID for signing iOS app bundle (ipa only)",
            required=False,
        )
        parser.add_argument(
            "--ios-export-method",
            dest="ios_export_method",
            type=str,
            required=False,
            help="Export method for iOS app bundle (default: debugging)",
        )
        parser.add_argument(
            "--ios-provisioning-profile",
            dest="ios_provisioning_profile",
            type=str,
            required=False,
            help="Provisioning profile name or UUID that should be used to sign and "
            "export iOS app bundle",
        )
        parser.add_argument(
            "--ios-signing-certificate",
            dest="ios_signing_certificate",
            type=str,
            required=False,
            help="Signing certificate name, SHA-1 hash, or automatic selector to use "
            "for signing iOS app bundle",
        )
        parser.add_argument(
            "--base-url",
            dest="base_url",
            type=str,
            help="Base URL from which the app is served (web only)",
        )
        parser.add_argument(
            "--web-renderer",
            dest="web_renderer",
            type=str.lower,
            choices=["auto", "canvaskit", "skwasm"],
            help="Flutter web renderer to use (web only) [env: FLET_WEB_RENDERER=]",
        )
        parser.add_argument(
            "--route-url-strategy",
            dest="route_url_strategy",
            type=str.lower,
            choices=["path", "hash"],
            help="Base URL path to serve the app from. "
            "Useful if the app is hosted in a subdirectory (web only) "
            "[env: FLET_WEB_ROUTE_URL_STRATEGY=]",
        )
        parser.add_argument(
            "--pwa-background-color",
            dest="pwa_background_color",
            required=False,
            help="Initial background color for your web app (web only)",
        )
        parser.add_argument(
            "--pwa-theme-color",
            dest="pwa_theme_color",
            required=False,
            help="Default color for your web app's user interface (web only)",
        )
        parser.add_argument(
            "--no-wasm",
            dest="no_wasm",
            action="store_true",
            default=False,
            help="Disable WASM target for web build (web only)",
        )
        parser.add_argument(
            "--no-cdn",
            dest="no_cdn",
            action="store_true",
            default=False,
            help="Disable loading of CanvasKit, Pyodide and fonts from CDN "
            "[env: FLET_WEB_NO_CDN=]",
        )
        parser.add_argument(
            "--split-per-abi",
            dest="split_per_abi",
            action="store_true",
            default=None,
            help="Split the APKs per ABIs (Android only)",
        )
        parser.add_argument(
            "--compile-app",
            dest="compile_app",
            action=argparse.BooleanOptionalAction,
            default=None,
            help="Pre-compile app's `.py` files to `.pyc` (on by default; "
            "use --no-compile-app to disable)",
        )
        parser.add_argument(
            "--compile-packages",
            dest="compile_packages",
            action=argparse.BooleanOptionalAction,
            default=None,
            help="Pre-compile site packages' `.py` files to `.pyc` (on by default; "
            "use --no-compile-packages to disable)",
        )
        parser.add_argument(
            "--swift-package-manager",
            dest="swift_package_manager",
            action=argparse.BooleanOptionalAction,
            default=None,
            help="Integrate the embedded Python runtime via Swift Package Manager "
            "(default) or CocoaPods for iOS/macOS builds. On by default, matching "
            "Flutter 3.44+ which uses SPM by default (other non-SPM plugins still "
            "build with CocoaPods alongside it). Use --no-swift-package-manager (or "
            "`swift_package_manager = false` under [tool.flet]) only if you've "
            "disabled Swift Package Manager in Flutter.",
        )
        parser.add_argument(
            "--cleanup-app",
            dest="cleanup_app",
            action="store_true",
            default=None,
            help="Remove unnecessary app files upon packaging",
        )
        parser.add_argument(
            "--cleanup-app-files",
            dest="cleanup_app_files",
            action="extend",
            nargs="+",
            help="The list of globs to delete extra app files and directories",
        )
        parser.add_argument(
            "--cleanup-packages",
            dest="cleanup_packages",
            action="store_true",
            default=None,
            help="Remove unnecessary package files upon packaging",
        )
        parser.add_argument(
            "--cleanup-package-files",
            dest="cleanup_package_files",
            action="extend",
            nargs="+",
            help="The list of globs to delete extra package files and directories",
        )
        parser.add_argument(
            "--flutter-build-args",
            dest="flutter_build_args",
            action="append",
            nargs="*",
            help="Additional arguments for flutter build command",
        )
        parser.add_argument(
            "--source-packages",
            dest="source_packages",
            action="extend",
            nargs="+",
            default=[],
            help="The list of Python packages to install from source distributions",
        )
        parser.add_argument(
            "--android-extract-packages",
            dest="android_extract_packages",
            nargs="+",
            default=[],
            help="Android only: Python packages (relative paths) to ship extracted "
            "to disk instead of inside the app zip — for packages that read bundled "
            "data via __file__ / pkg_resources rather than importlib.resources",
        )
        parser.add_argument(
            "--python-version",
            dest="python_version",
            type=str,
            default=None,
            help="Python version to bundle (e.g. 3.13). Defaults to the latest "
            "supported version, or is parsed from project.requires-python.",
        )
        parser.add_argument(
            "--info-plist",
            dest="info_plist",
            action="extend",
            nargs="+",
            default=[],
            help="The list of `<key>=<value>` pairs to add to Info.plist. Values can "
            "be booleans, strings, numbers, TOML arrays, or TOML inline tables "
            "(macos, ipa and ios-simulator only); can be used multiple times",
        )
        parser.add_argument(
            "--macos-entitlements",
            dest="macos_entitlements",
            action="extend",
            nargs="+",
            default=[],
            help="The list of `<key>=<value>` entitlements. Values can be booleans, "
            "strings, numbers, TOML arrays, or TOML inline tables "
            "(macos only); can be used multiple times",
        )
        parser.add_argument(
            "--android-features",
            dest="android_features",
            action="extend",
            nargs="+",
            default=[],
            help="The list of `<feature_name>=true|false` features to add to "
            "AndroidManifest.xml (android only); can be used multiple times",
        )
        parser.add_argument(
            "--android-permissions",
            dest="android_permissions",
            action="extend",
            nargs="+",
            default=[],
            help="The list of `<permission_name>=true|false` permissions to add to "
            "AndroidManifest.xml (android only); can be used multiple times",
        )
        parser.add_argument(
            "--android-meta-data",
            dest="android_meta_data",
            action="extend",
            nargs="+",
            default=[],
            help="The list of `<name>=<value>` app meta-data entries to add to "
            "AndroidManifest.xml (android only); can be used multiple times",
        )
        parser.add_argument(
            "--permissions",
            dest="permissions",
            type=str.lower,
            action="extend",
            nargs="+",
            default=[],
            choices=["location", "camera", "microphone", "photo_library"],
            help="The list of pre-defined cross-platform permissions for iOS, Android "
            "and macOS builds",
        )
        parser.add_argument(
            "--deep-linking-scheme",
            dest="deep_linking_scheme",
            help="Deep linking URL scheme to configure for iOS and Android builds, "
            "i.g. `https` or `myapp`",
        )
        parser.add_argument(
            "--deep-linking-host",
            dest="deep_linking_host",
            help="Deep linking URL host for iOS and Android builds",
        )
        parser.add_argument(
            "--android-signing-key-store",
            dest="android_signing_key_store",
            help="path to an upload keystore `.jks` file for Android apps "
            "[env: FLET_ANDROID_SIGNING_KEY_STORE=]",
        )
        parser.add_argument(
            "--android-signing-key-store-password",
            dest="android_signing_key_store_password",
            help="Android signing store password "
            "[env: FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD=]",
        )
        parser.add_argument(
            "--android-signing-key-password",
            dest="android_signing_key_password",
            help="Android signing key password "
            "[env: FLET_ANDROID_SIGNING_KEY_PASSWORD=]",
        )
        parser.add_argument(
            "--android-signing-key-alias",
            dest="android_signing_key_alias",
            default=None,
            help="Android signing key alias [env: FLET_ANDROID_SIGNING_KEY_ALIAS=]",
        )
        parser.add_argument(
            "--build-number",
            dest="build_number",
            type=int,
            help="Build number - an identifier used as an internal version number",
        )
        parser.add_argument(
            "--build-version",
            dest="build_version",
            help="Build version - a `x.y.z` string used as the version number "
            "shown to users",
        )
        parser.add_argument(
            "--module-name",
            dest="module_name",
            help="Python module name with an app entry point",
        )
        parser.add_argument(
            "--template",
            dest="template",
            type=str,
            help="Directory containing Flutter bootstrap template, or a URL "
            "to a git repository template",
        )
        parser.add_argument(
            "--template-dir",
            dest="template_dir",
            type=str,
            help="Relative path to a Flutter bootstrap template in a repository",
        )
        parser.add_argument(
            "--template-ref",
            dest="template_ref",
            type=str,
            help="The branch, tag or commit ID to checkout after cloning "
            "the repository with Flutter bootstrap template",
        )
        parser.add_argument(
            "--show-platform-matrix",
            action="store_true",
            default=False,
            help="Display the build platform matrix in a table, then exit",
        )
        super().add_arguments(parser)

    def handle(self, options: argparse.Namespace) -> None:
        """
        Store build command options and resolve requested target platform.

        Args:
            options: Parsed command-line options.
        """

        super().handle(options)

        if getattr(self.options, "clear_cache", None):
            deprecated_warning(
                name="--clear-cache",
                reason="Use the `flet clean` command instead.",
                version="0.86.0",
                delete_version="0.89.0",
                type="flag",
            )
            console.print(
                "Warning: the `--clear-cache` flag is deprecated since version "
                "0.86.0 and will be removed in version 0.89.0. "
                "Use the `flet clean` command instead.",
                style=warning_style,
            )

        if "target_platform" in self.options:
            self.target_platform = self.options.target_platform

    def initialize_command(self):
        """
        Initialize build paths, target metadata, and shared Flutter prerequisites.
        """

        assert self.options
        assert self.target_platform

        self.package_platform = self.platforms[self.target_platform]["package_platform"]
        self.config_platform = self.platforms[self.target_platform]["config_platform"]
        self.require_android_sdk = self.package_platform == "Android"

        super().initialize_command()

        self.python_app_path = Path(self.options.python_app_path).resolve()

        if not (
            os.path.exists(self.python_app_path) or os.path.isdir(self.python_app_path)
        ):
            self.cleanup(
                1,
                f"Path to Flet app does not exist or is not a directory: "
                f"{self.python_app_path}",
            )

        self.rel_out_dir = self.options.output_dir or os.path.join(
            "build", self.platforms[self.target_platform]["dist"]
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

        try:
            self.python_release = resolve_python_version(
                self.options.python_version, self.get_pyproject
            )
        except UnsupportedPythonVersionError as e:
            self.cleanup(1, str(e))

        # Changing the bundled Python version invalidates the compiled bytecode
        # baked into the previous build's native bundles (stdlib/site-packages
        # .pyc). Reusing the build directory would mix versions and crash at
        # runtime with "bad magic number". Force a clean rebuild on a switch.
        version_marker = self.build_dir / ".python-version"
        if self.build_dir.exists() and version_marker.exists():
            previous = version_marker.read_text(encoding="utf-8").strip()
            if previous and previous != self.python_release.short:
                console.log(
                    f"Bundled Python version changed ({previous} -> "
                    f"{self.python_release.short}); cleaning the build directory."
                )
                shutil.rmtree(self.build_dir, ignore_errors=True)
        self.build_dir.mkdir(parents=True, exist_ok=True)
        version_marker.write_text(self.python_release.short, encoding="utf-8")

    def validate_target_platform(self):
        """
        Validate whether current host OS can build the selected target platform.

        Displays build matrix context and exits when target is unsupported or
        when matrix display is explicitly requested.
        """

        assert self.options
        assert self.target_platform
        if (
            self.current_platform
            not in self.platforms[self.target_platform]["can_be_run_on"]
            or self.options.show_platform_matrix
        ):
            can_build_message = (
                "can't"
                if self.current_platform
                not in self.platforms[self.target_platform]["can_be_run_on"]
                else "can"
            )
            # replace "Darwin" with "macOS" for user-friendliness
            self.current_platform = (
                "macOS" if self.current_platform == "Darwin" else self.current_platform
            )
            # highlight the current platform in the build matrix table
            self.platform_matrix_table.rows[
                list(self.platforms.keys()).index(self.target_platform)
            ].style = "bold red1"
            console.log(self.platform_matrix_table)

            message = f"You {can_build_message} build "
            f"[cyan]{self.target_platform}[/] on "
            f"[magenta]{self.current_platform}[/]."
            self.cleanup(1, message)

    def validate_entry_point(self):
        """
        Resolve app entry-point module and ensure corresponding Python file exists.
        """

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
                f"{self.python_module_filename} not found in the root of Flet "
                "app directory. Use --module-name option to specify an entry point "
                "for your Flet app.",
            )

    def setup_template_data(self):
        """
        Build template context by merging CLI options, project config, and defaults.

        The resulting context is stored in `self.template_data` and later used
        to render Flutter bootstrap templates.
        """

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
        project_name_raw = (
            self.options.project_name
            or self.get_pyproject("project.name")
            or self.python_app_path.name
        )
        project_name_slug = slugify(cast(str, project_name_raw))
        project_name = project_name_slug.replace("-", "_")
        artifact_name = (
            self.options.artifact_name
            or self.get_pyproject(f"tool.flet.{self.config_platform}.artifact")
            or self.get_pyproject("tool.flet.artifact")
            or self.options.project_name
            or self.get_pyproject("project.name")
            or self.python_app_path.name
        )
        # Under integration test, `flutter test -d <desktop>` launches the built
        # binary by the project name (the Flutter pubspec `name`), but the
        # Windows/Linux runner sets the executable's OUTPUT_NAME to artifact_name.
        # When they differ (e.g. `artifact = "my-app"` vs project `my_app`) the
        # test host can't find the binary. Pin them equal in test mode.
        if getattr(self, "test_mode", False):
            artifact_name = project_name
        product_name = (
            self.options.product_name
            or self.get_pyproject("tool.flet.product")
            or self.options.project_name
            or self.get_pyproject("project.name")
            or self.python_app_path.name
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
            "com.apple.security.files.user-selected.read-write": True,
        }
        android_permissions = {"android.permission.INTERNET": True}
        android_features = {
            "android.software.leanback": False,
            "android.hardware.touchscreen": False,
        }
        android_meta_data = {}
        android_providers = {}

        # merge values from "--permissions" arg:
        for p in (
            self.options.permissions
            or self.get_pyproject("tool.flet.permissions")
            or []
        ):
            if p in self.cross_platform_permissions:
                permission_config = self.cross_platform_permissions[p]
                info_plist.update(
                    permission_config.get(f"{self.config_platform}_info_plist", {})
                    or permission_config.get("info_plist", {})
                )
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
                info_plist[k] = parse_cli_plist_value(v)
            else:
                self.cleanup(1, f"Invalid Info.plist option: {p}")

        for key, value in info_plist.items():
            if not is_supported_plist_value(value):
                self.cleanup(
                    1,
                    "Unsupported Info.plist value type for "
                    f"{key}: {type(value).__name__}. Supported types are "
                    "string, boolean, integer, float, dictionary, and arrays "
                    "containing those values.",
                )

        macos_entitlements = merge_dict(
            macos_entitlements,
            self.get_pyproject("tool.flet.macos.entitlement") or {},
        )

        # parse --macos-entitlements
        for p in self.options.macos_entitlements:
            i = p.find("=")
            if i > -1:
                macos_entitlements[p[:i]] = parse_cli_plist_value(p[i + 1 :])
            else:
                self.cleanup(1, f"Invalid macOS entitlement option: {p}")

        for key, value in macos_entitlements.items():
            if not is_supported_plist_value(value):
                self.cleanup(
                    1,
                    "Unsupported macOS entitlement value type for "
                    f"{key}: {type(value).__name__}. Supported types are "
                    "string, boolean, integer, float, dictionary, and arrays "
                    "containing those values.",
                )

        android_permissions = merge_dict(
            android_permissions,
            self.get_pyproject("tool.flet.android.permission") or {},
        )

        # parse --android-permissions
        for p in self.options.android_permissions:
            i = p.find("=")
            if i > -1:
                try:
                    android_permissions[p[:i]] = parse_cli_bool_value(p[i + 1 :])
                except ValueError:
                    self.cleanup(
                        1,
                        f"Invalid Android permission option value for {p[:i]}: "
                        f"{p[i + 1 :]}. Expected true or false.",
                    )
            else:
                self.cleanup(1, f"Invalid Android permission option: {p}")

        for key, value in android_permissions.items():
            if isinstance(value, bool):
                continue
            if isinstance(value, dict):
                for ak, av in value.items():
                    if not isinstance(av, (str, bool, int, float)):
                        self.cleanup(
                            1,
                            f"Invalid Android permission attribute value for "
                            f"{key}.{ak}: {type(av).__name__}. "
                            "Expected string, boolean, or number.",
                        )
                continue
            self.cleanup(
                1,
                f"Invalid Android permission value for {key}: "
                f"{type(value).__name__}. Expected boolean or inline table.",
            )

        android_features = merge_dict(
            android_features,
            self.get_pyproject("tool.flet.android.feature") or {},
        )

        # parse --android-features
        for p in self.options.android_features:
            i = p.find("=")
            if i > -1:
                try:
                    android_features[p[:i]] = parse_cli_bool_value(p[i + 1 :])
                except ValueError:
                    self.cleanup(
                        1,
                        f"Invalid Android feature option value for {p[:i]}: "
                        f"{p[i + 1 :]}. Expected true or false.",
                    )
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

        android_providers = merge_dict(
            android_providers,
            self.get_pyproject("tool.flet.android.provider") or {},
        )

        def _xml_attr_value(v):
            # Android XML expects lowercase booleans.
            if isinstance(v, bool):
                return "true" if v else "false"
            return v

        normalized_providers = {}
        for key, value in android_providers.items():
            if value is False or value == {}:
                continue
            if value is True:
                self.cleanup(
                    1,
                    f"Invalid Android provider value for {key}: 'true' is not "
                    "supported. Use an inline table of attributes, or 'false' "
                    "to skip.",
                )
            if not isinstance(value, dict):
                self.cleanup(
                    1,
                    f"Invalid Android provider value for {key}: "
                    f"{type(value).__name__}. Expected boolean or inline table.",
                )
            normalized = {}
            for ak, av in value.items():
                if ak == "name":
                    self.cleanup(
                        1,
                        f"Invalid Android provider attribute for {key}: "
                        "'name' is reserved and is taken from the table key.",
                    )
                if ak == "meta_data":
                    if not isinstance(av, dict):
                        self.cleanup(
                            1,
                            f"Invalid Android provider meta_data for {key}: "
                            f"{type(av).__name__}. Expected inline table.",
                        )
                    normalized_meta = {}
                    for mk, mv in av.items():
                        if isinstance(mv, (str, bool, int, float)):
                            normalized_meta[mk] = _xml_attr_value(mv)
                            continue
                        if isinstance(mv, dict):
                            normalized_attrs = {}
                            for attr_key, attr_value in mv.items():
                                if not isinstance(attr_value, (str, bool, int, float)):
                                    self.cleanup(
                                        1,
                                        f"Invalid Android provider meta-data "
                                        f"attribute value for "
                                        f"{key}.meta_data.{mk}.{attr_key}: "
                                        f"{type(attr_value).__name__}. "
                                        "Expected string, boolean, or number.",
                                    )
                                normalized_attrs[attr_key] = _xml_attr_value(attr_value)
                            normalized_meta[mk] = normalized_attrs
                            continue
                        self.cleanup(
                            1,
                            f"Invalid Android provider meta-data value for "
                            f"{key}.meta_data.{mk}: {type(mv).__name__}. "
                            "Expected string, boolean, number, or inline table.",
                        )
                    normalized["meta_data"] = normalized_meta
                    continue
                if not isinstance(av, (str, bool, int, float)):
                    self.cleanup(
                        1,
                        f"Invalid Android provider attribute value for "
                        f"{key}.{ak}: {type(av).__name__}. "
                        "Expected string, boolean, or number.",
                    )
                normalized[ak] = _xml_attr_value(av)
            normalized_providers[key] = normalized
        android_providers = normalized_providers

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
        target_arch = (
            target_arch
            if isinstance(target_arch, list)
            else [target_arch]
            if isinstance(target_arch, str)
            else []
        )
        if self.package_platform == "Android":
            invalid_archs = [
                arch
                for arch in target_arch
                if arch not in ANDROID_ARCH_TO_FLUTTER_TARGET_PLATFORM
            ]
            if invalid_archs:
                self.cleanup(
                    1,
                    f"Invalid Android architecture(s): {', '.join(invalid_archs)}.\n"
                    f"Supported: "
                    f"{', '.join(ANDROID_ARCH_TO_FLUTTER_TARGET_PLATFORM)}.\n"
                    f"Docs: https://flet.dev/docs/publish/android#supported-target-architectures",
                )
            python_abis = list(self.python_release.android_abis)
            unsupported_archs = [a for a in target_arch if a not in python_abis]
            if unsupported_archs:
                self.cleanup(
                    1,
                    f"Architecture(s) not supported by Python "
                    f"{self.python_release.short}: {', '.join(unsupported_archs)}.\n"
                    f"Supported: {', '.join(python_abis)}.\n"
                    f"Docs: https://flet.dev/docs/publish/android#supported-target-architectures",
                )
            if not target_arch:
                # Build only for the ABIs the bundled Python supports.
                target_arch = python_abis

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

        if (
            self.target_platform in ["ipa"]
            and not ios_provisioning_profile
            and not self.debug_platform
            and not getattr(self, "test_mode", False)
        ):
            console.print(
                Panel(
                    "This build will generate an .xcarchive (Xcode Archive). "
                    "To produce an .ipa (iOS App Package), please specify "
                    "a Provisioning Profile.",
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
                or "auto"
            ),
            "pwa_background_color": (
                self.options.pwa_background_color
                or self.get_pyproject("tool.flet.web.pwa_background_color")
            ),
            "pwa_theme_color": (
                self.options.pwa_theme_color
                or self.get_pyproject("tool.flet.web.pwa_theme_color")
            ),
            "no_wasm": (
                self.options.no_wasm
                or self.get_pyproject("tool.flet.web.wasm") == False  # noqa: E712
            ),
            "no_cdn": (
                self.options.no_cdn or self.get_pyproject("tool.flet.web.cdn") == False  # noqa: E712
            ),
            # Surface the resolved Pyodide release to the cookiecutter
            # context so the web template's index.html can wire the
            # correct jsdelivr URL when CDN mode is on.
            "pyodide_version": self.python_release.pyodide,
            "base_url": f"/{base_url}/" if base_url else "/",
            "split_per_abi": split_per_abi,
            # Enabled by `flet test` to scaffold integration-test wiring
            # (integration_test/ + flutter_test dev deps). Default False so
            # normal `flet build`/`flet debug` output is unaffected.
            "test_mode": getattr(self, "test_mode", False),
            "project_name": project_name,
            "project_name_slug": project_name_slug,
            "artifact_name": artifact_name,
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
                "python_version": self.python_release.short,
                "target_arch": target_arch,
                "android_excluded_abis": (
                    excluded_android_abis(target_arch)
                    if self.package_platform == "Android"
                    else []
                ),
                "info_plist": info_plist,
                "macos_entitlements": macos_entitlements,
                "android_permissions": android_permissions,
                "android_features": android_features,
                "android_meta_data": android_meta_data,
                "android_providers": android_providers,
                "deep_linking": {
                    "scheme": deep_linking_scheme,
                    "host": deep_linking_host,
                },
                "android_signing": bool(
                    self.options.android_signing_key_store
                    or self.get_pyproject("tool.flet.android.signing.key_store")
                    or os.getenv("FLET_ANDROID_SIGNING_KEY_STORE")
                ),
            },
            "flutter": {"dependencies": list(self.flutter_dependencies.keys())},
            "boot_screen": self._resolve_boot_screen(),
            "pyproject": self.get_pyproject(),
        }

    def _resolve_boot_screen(self):
        """
        Resolve the boot screen configuration from pyproject.toml.

        Merges the global `[tool.flet.boot_screen]` with the platform-specific
        `[tool.flet.<platform>.boot_screen]` (platform wins per key), resolves
        the selected screen `name` (default "flet") and its options table.

        Falls back to the legacy `[tool.flet[.<platform>].app.boot_screen]` /
        `app.startup_screen` (`show`/`message`) settings, mapping them onto the
        built-in "flet" screen with a deprecation warning.

        Returns a dict with `name` and `options_b64` (base64-encoded JSON of the
        options table) for the cookiecutter template.
        """
        config_platform = self.config_platform

        def merged(key):
            result = {}
            merge_dict(
                result, copy.deepcopy(self.get_pyproject(f"tool.flet.{key}") or {})
            )
            merge_dict(
                result,
                copy.deepcopy(
                    self.get_pyproject(f"tool.flet.{config_platform}.{key}") or {}
                ),
            )
            return result

        boot_screen = merged("boot_screen")

        if boot_screen:
            name = boot_screen.get("name", "flet")
            options = boot_screen.get(name) or {}
        else:
            # backward compatibility with the legacy app.boot_screen /
            # app.startup_screen settings
            name = "flet"
            options = {}
            legacy_boot = merged("app.boot_screen")
            legacy_startup = merged("app.startup_screen")
            if legacy_boot or legacy_startup:
                console.log(
                    "[tool.flet.app.boot_screen] and "
                    "[tool.flet.app.startup_screen] are deprecated; use "
                    "[tool.flet.boot_screen] with a named screen instead.",
                    style=warning_style,
                )
                if legacy_boot.get("show"):
                    options["spinner_size"] = 30
                    message = legacy_boot.get("message")
                    if message:
                        options["prepare_message"] = message
                if legacy_startup.get("show"):
                    options["spinner_size"] = 30
                    message = legacy_startup.get("message")
                    if message:
                        options["startup_message"] = message

        return {
            "name": name,
            "options_b64": base64.b64encode(json.dumps(options).encode("utf-8")).decode(
                "ascii"
            ),
        }

    def create_flutter_project(self, second_pass=False):
        """
        Render Flutter bootstrap project from template if template inputs changed.

        Args:
            second_pass: Whether this render happens after extension registration.

        Returns:
            `True` when template output changed and files were regenerated,
            otherwise `False`.
        """

        assert self.options
        assert self.get_pyproject
        assert self.flutter_dir
        assert self.template_data
        assert self.build_dir
        assert self.pubspec_path

        hash = HashStamp(
            self.build_dir / ".hash" / f"template-{'2' if second_pass else '1'}"
        )

        template_url = self.options.template or self.get_pyproject(
            "tool.flet.template.url"
        )

        template_ref = self.options.template_ref or self.get_pyproject(
            "tool.flet.template.ref"
        )
        if not template_ref:
            template_ref = flet.version.flet_version

        is_local_dev = False
        # Identity printed in status / hashed for invalidation; may differ from
        # the path cookiecutter actually reads when caching kicks in below.
        template_source = template_url
        if template_url:
            # User-provided template (git repo or local path) — use checkout
            checkout = template_ref
        else:
            # Check for local dev templates first (running from source checkout)
            local_tpl = Path(__file__).resolve().parents[5] / "templates" / "build"
            if local_tpl.is_dir():
                template_url = str(local_tpl)
                template_source = template_url
                checkout = None
                is_local_dev = True
            else:
                from flet_cli.utils.template_cache import get_cached_template_zip

                template_source = DEFAULT_TEMPLATE_URL.format(version=template_ref)
                template_url = str(
                    get_cached_template_zip(template_source, template_ref)
                )
                checkout = None

        hash.update(template_source)
        hash.update(template_ref)

        template_dir = self.options.template_dir or self.get_pyproject(
            "tool.flet.template.dir"
        )
        hash.update(template_dir)
        hash.update(self.template_data)

        hash_changed = hash.has_changed()

        if hash_changed:
            # if options.clear_cache is set, delete any existing Flutter bootstrap
            # project directory
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
                status = f"[bold blue]Creating app shell from {template_source}"
                if checkout:
                    status += f' with ref "{template_ref}"'
                status += "..."
                self.update_status(status)

            try:
                from cookiecutter.main import cookiecutter

                cookiecutter(
                    template=template_url,
                    checkout=checkout,
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

            # For local development, override flet dependency with path
            repo_root = None
            pubspec = None
            if is_local_dev:
                repo_root = flet.version.find_repo_root(Path(__file__).resolve().parent)
                if repo_root:
                    flet_pkg_path = str(repo_root / "packages" / "flet")
                    pubspec = self.load_yaml(self.pubspec_path)
                    pubspec["dependencies"]["flet"] = {"path": flet_pkg_path}
                    pubspec.setdefault("dependency_overrides", {})["flet"] = {
                        "path": flet_pkg_path
                    }

            # In test mode, inject the integration-test driver (and flutter_test)
            # as dev dependencies. They are intentionally NOT in the template
            # pubspec: that keeps it valid YAML for the release patch tooling and
            # ensures a normal `flet build` never pulls them. flet_integration_test
            # is publish_to:none, so for local dev it resolves to the in-repo
            # package by path, and for an end user it is a git dependency pinned to
            # this flet version's tag.
            if getattr(self, "test_mode", False):
                if pubspec is None:
                    pubspec = self.load_yaml(self.pubspec_path)
                dev_deps = pubspec.setdefault("dev_dependencies", {})
                dev_deps["flutter_test"] = {"sdk": "flutter"}
                if is_local_dev and repo_root:
                    fit_pkg_path = str(repo_root / "packages" / "flet_integration_test")
                    dev_deps["flet_integration_test"] = {"path": fit_pkg_path}
                    pubspec.setdefault("dependency_overrides", {})[
                        "flet_integration_test"
                    ] = {"path": fit_pkg_path}
                else:
                    dev_deps["flet_integration_test"] = {
                        "git": {
                            "url": "https://github.com/flet-dev/flet.git",
                            "ref": f"v{flet.version.flet_version}",
                            "path": "packages/flet_integration_test",
                        }
                    }

            # Only the web (Pyodide) build loads the packaged app as a Flutter
            # asset; on native platforms serious_python places it inside the
            # bundle, and a missing app/app.zip asset would fail the build.
            if self.config_platform == "web":
                if pubspec is None:
                    pubspec = self.load_yaml(self.pubspec_path)
                assets = pubspec.setdefault("flutter", {}).setdefault("assets", [])
                for asset in ["app/app.zip", "app/app.zip.hash"]:
                    if asset not in assets:
                        assets.append(asset)

            if pubspec is not None:
                self.save_yaml(self.pubspec_path, pubspec)

            pyproject_pubspec = self.get_pyproject("tool.flet.flutter.pubspec")

            if pyproject_pubspec:
                pyproject_pubspec = copy.deepcopy(pyproject_pubspec)
                pubspec = self.load_yaml(self.pubspec_path)
                # Replace individual dependency entries from pyproject rather
                # than deep-merging them — a Dart dependency can only have one
                # source, so merging {"path":…} with {"git":…} is invalid.
                for section in (
                    "dependencies",
                    "dependency_overrides",
                    "dev_dependencies",
                ):
                    if section in pyproject_pubspec:
                        pubspec.setdefault(section, {}).update(
                            pyproject_pubspec.pop(section)
                        )
                pubspec = merge_dict(pubspec, pyproject_pubspec)
                self.save_yaml(self.pubspec_path, pubspec)

            # make backup of pubspec.yaml
            shutil.copyfile(self.pubspec_path, f"{self.pubspec_path}.orig")

            if not second_pass:
                console.log(f"Created app shell {self.emojis['checkmark']}")

        hash.commit()

        return hash_changed

    def register_flutter_extensions(self):
        """
        Discover local Flutter extension packages and inject them into dependencies.
        """

        assert self.flutter_packages_dir
        assert self.flutter_packages_temp_dir
        assert isinstance(self.flutter_dependencies, dict)
        assert self.template_data
        assert self.build_dir

        # Replace the permanent flutter-packages copy with this build's set. The
        # temp dir is populated by serious_python's package step and is ABSENT
        # when the app has no Flutter extensions — so always clear the old copy
        # first, otherwise an extension removed since the previous build (e.g.
        # dropping flet-video) would linger here and stay in the built app.
        #
        # Skip this when the package step ran with --skip-site-packages: in that
        # mode serious_python does not repopulate the temp dir, so an absent temp
        # dir means "unchanged" rather than "no extensions". Wiping here would
        # delete the previous build's extensions and never restore them, breaking
        # the Flutter build (unresolved web plugins). A removed extension changes
        # the package requirements, flips the package hash, and takes the full
        # (non-skip) path above instead.
        if not self.site_packages_skipped:
            if self.flutter_packages_dir.exists():
                shutil.rmtree(self.flutter_packages_dir, ignore_errors=True)
            if self.flutter_packages_temp_dir.exists():
                # copy packages from temp to permanent location
                shutil.move(self.flutter_packages_temp_dir, self.flutter_packages_dir)

        if self.flutter_packages_dir.exists():
            self.update_status("[bold blue]Registering Flutter user extensions...")

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
        """
        Merge resolved Flutter extension dependencies into `pubspec.yaml`.
        """

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
        for dep in pubspec["dependencies"]:
            if dep == self.template_data["project_name"]:
                self.cleanup(
                    1,
                    f"Project name cannot have the same name as one of its "
                    f"dependencies: {dep}. Use --project option to specify "
                    "a different project name.",
                )

        self.save_yaml(self.pubspec_path, pubspec)

    def customize_icons(self):
        """
        Resolve platform icon assets, patch pubspec icon config, and generate icons.
        """

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
            pubspec["flutter_launcher_icons"]["adaptive_icon_background"] = (
                adaptive_icon_background
            )

        # check if pubspec changed
        hash.update(Path(pubspec_origin_path).stat().st_mtime)
        hash.update(pubspec["flutter_launcher_icons"])

        # save pubspec.yaml
        if hash.has_changed():
            if copy_ops:
                self.update_status("[bold blue]Customizing app icons...")
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

            self.update_status("[bold blue]Generating app icons...")

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
                if isinstance(icons_result.stdout, str):
                    console.log(icons_result.stdout, style=verbose1_style)
                if isinstance(icons_result.stderr, str):
                    console.log(icons_result.stderr, style=error_style)
                self.cleanup(icons_result.returncode)
            console.log(f"Generated app icons {self.emojis['checkmark']}")

        hash.commit()

    def customize_splash_images(self):
        """
        Resolve splash assets/colors, patch splash config, and generate splash files.
        """

        assert self.package_app_path
        assert self.flutter_dir
        assert self.options
        assert self.get_pyproject
        assert self.pubspec_path
        assert self.build_dir
        assert self.target_platform

        if self.target_platform not in ["web", "ipa", "ios-simulator", "apk", "aab"]:
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
            pubspec["flutter_native_splash"]["android_12"]["color_dark"] = (
                splash_dark_color
            )

        splash_icon_bgcolor = self.get_pyproject(
            f"tool.flet.{self.config_platform}.splash.icon_bgcolor"
        ) or self.get_pyproject("tool.flet.splash.icon_bgcolor")

        if splash_icon_bgcolor:
            pubspec["flutter_native_splash"]["android_12"]["icon_background_color"] = (
                splash_icon_bgcolor
            )

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
                self.update_status("[bold blue]Customizing app splash images...")
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
            self.update_status("[bold blue]Generating splash screens...")
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
                if isinstance(splash_result.stdout, str):
                    console.log(splash_result.stdout, style=verbose1_style)
                if isinstance(splash_result.stderr, str):
                    console.log(splash_result.stderr, style=error_style)
                self.cleanup(splash_result.returncode)
            console.log(f"Generated splash screens {self.emojis['checkmark']}")

        hash.commit()

    def fallback_image(self, pubspec, yaml_path: str, images: list, images_dir: str):
        """
        Assign first available image from candidates to a nested pubspec key path.

        Args:
            pubspec: Parsed pubspec document.
            yaml_path: Dot-separated key path to image setting.
            images: Candidate image file names in fallback order.
            images_dir: Relative image directory prefix.
        """

        d = pubspec
        pp = yaml_path.split(".")
        for p in pp[:-1]:
            d = d[p]
        for image in images:
            if image:
                d[pp[-1]] = f"{images_dir}/{image}"
                return

    def _darwin_spm_active(self) -> bool:
        """Whether to stage serious_python for Swift Package Manager (vs CocoaPods).

        On by default, matching Flutter 3.44+ (SPM enabled by default). Because
        `serious_python_darwin` ships a `Package.swift`, Flutter always builds it
        as an SPM plugin when SPM is enabled — even in a hybrid app where other,
        non-SPM plugins (e.g. `flet-video`/media_kit) build with CocoaPods at the
        same time. So serious_python must stage for SPM to match; it is NOT tied
        to whether the app also pulls in non-SPM plugins. Users force CocoaPods
        with `--no-swift-package-manager` (or `swift_package_manager = false` under
        `[tool.flet]`) only when they've disabled SPM in Flutter itself. Flet does
        not change Flutter's global SPM configuration.
        """
        if self.package_platform not in ("iOS", "Darwin"):
            return False
        return self.get_bool_setting(
            self.options.swift_package_manager, "swift_package_manager", True
        )

    def package_python_app(self):
        """
        Package Python app and dependencies into Flutter-consumable app archive.

        Handles dependency resolution, cleanup/compile flags, cache checks, and
        invokes `serious_python` packaging command.
        """

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

        self.update_status("[bold blue]Packaging Python app...")
        package_args = [
            self.dart_exe,
            "run",
            "--suppress-analytics",
            "serious_python:main",
            "package",
            str(self.package_app_path),
            "--platform",
            self.package_platform,
            "--python-version",
            self.python_release.short,
        ]

        if self.template_data["options"]["target_arch"]:
            # serious_python's --arch is a Dart multi-option: values must be
            # comma-separated or the flag repeated. Space-separated values
            # after the first are silently treated as positional arguments.
            package_args.extend(
                ["--arch", ",".join(self.template_data["options"]["target_arch"])]
            )

        # Only the short version is passed; serious_python derives the full
        # version, python-build date, and dart_bridge version from its own
        # committed snapshot of the manifest.
        package_env = {
            "SERIOUS_PYTHON_VERSION": self.python_release.short,
        }

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
                or self.get_pyproject("tool.flet.dev_packages")
                or []
            )
            if len(dev_packages) > 0:
                for i in range(0, len(toml_dependencies)):
                    package_name = Requirement(toml_dependencies[i]).name
                    if package_name in dev_packages:
                        package_location = dev_packages[package_name]
                        dev_path = Path(package_location)
                        if not dev_path.is_absolute():
                            dev_path = (self.python_app_path / dev_path).resolve()
                        if dev_path.exists():
                            # Use Path.as_uri() so Windows drive paths render as
                            # `file:///D:/a/...` rather than `file://D:\a\...`,
                            # which pip otherwise treats as a UNC path and fails
                            # to resolve.
                            toml_dependencies[i] = (
                                f"{package_name} @ {dev_path.as_uri()}"
                            )
                        else:
                            toml_dependencies[i] = (
                                f"{package_name} @ {package_location}"
                            )
                        dev_packages_configured = True
                if dev_packages_configured:
                    toml_dependencies.append("--no-cache-dir")

            for toml_dep in toml_dependencies:
                package_args.extend(["-r", toml_dep])

        elif requirements_txt.exists():
            if self.verbose > 1:
                with open(requirements_txt, encoding="utf-8") as f:
                    reqs_txt_contents = f.read()
                    console.log(
                        f"Contents of requirements.txt: {reqs_txt_contents}",
                        style=verbose2_style,
                    )
                    hash.update(reqs_txt_contents)
            package_args.extend(["-r", "-r", "-r", str(requirements_txt)])
        else:
            package_args.extend(["-r", f"flet=={flet.version.flet_version}"])

        # site-packages variable
        if self.package_platform != "Emscripten":
            package_env["SERIOUS_PYTHON_SITE_PACKAGES"] = str(
                self.build_dir / "site-packages"
            )
            # app staging dir: serious_python's `package` places the processed
            # app here (no app.zip on native); the platform native build copies
            # it into the bundle (Android zips it as a stored asset).
            package_env["SERIOUS_PYTHON_APP"] = str(self.build_dir / "python-app")

        # Swift Package Manager (darwin): tell serious_python's package command to
        # do the host-side SPM staging (the podspec prepare_command doesn't run
        # under SPM) and write the SP_NATIVE_SET cache-bust key to this file.
        # serious_python defaults to SPM staging, so be explicit either way — set
        # it false for the CocoaPods cases (e.g. an app using flet-video).
        if self.package_platform in ("iOS", "Darwin"):
            spm = self._darwin_spm_active()
            package_env["SERIOUS_PYTHON_DARWIN_SPM"] = "true" if spm else "false"
            if spm:
                package_env["SERIOUS_PYTHON_SPM_KEY_FILE"] = str(
                    self.build_dir / ".serious_python_spm_key"
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

        if self.target_platform == "web":
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

        # android-extract-packages: path-hungry packages shipped extracted to disk
        # instead of inside the zip (serious_python Android native-mmap packaging).
        # A built-in default set covers commonly-broken packages; the user list
        # (CLI / pyproject) is merged on top. Consumed by the serious_python_android
        # Gradle split during `flutter build`, so the env var is set on build_env
        # (see _run_flutter_command), not on the package step.
        self.android_extract_packages: list[str] = []
        if self.package_platform == "Android":
            user_extract_packages = (
                self.options.android_extract_packages
                or self.get_pyproject(
                    f"tool.flet.{self.config_platform}.extract_packages"
                )
                or self.get_pyproject("tool.flet.extract_packages")
                or []
            )
            self.android_extract_packages = list(
                dict.fromkeys(ANDROID_DEFAULT_EXTRACT_PACKAGES + user_extract_packages)
            )

        if self.get_bool_setting(self.options.compile_app, "compile.app", True):
            package_args.append("--compile-app")

        if self.get_bool_setting(
            self.options.compile_packages, "compile.packages", True
        ):
            package_args.append("--compile-packages")

        cleanup_app = self.get_bool_setting(
            self.options.cleanup_app, "cleanup.app", False
        )
        cleanup_packages = self.get_bool_setting(
            self.options.cleanup_packages, "cleanup.packages", True
        )

        if cleanup_app_files := (
            self.options.cleanup_app_files
            or self.get_pyproject(f"tool.flet.{self.config_platform}.cleanup.app_files")
            or self.get_pyproject("tool.flet.cleanup.app_files")
        ):
            if isinstance(cleanup_app_files, str):
                cleanup_app_files = [
                    value.strip() for value in cleanup_app_files.split(",")
                ]
            if isinstance(cleanup_app_files, list):
                package_args.extend(
                    [
                        "--cleanup-app-files",
                        ",".join([v.strip() for v in cleanup_app_files if v.strip()]),
                    ]
                )
                cleanup_app = True

        if cleanup_package_files := (
            self.options.cleanup_package_files
            or self.get_pyproject(
                f"tool.flet.{self.config_platform}.cleanup.package_files"
            )
            or self.get_pyproject("tool.flet.cleanup.package_files")
        ):
            if isinstance(cleanup_package_files, str):
                cleanup_package_files = [
                    value for value in cleanup_package_files.split(",")
                ]
            if isinstance(cleanup_package_files, list):
                package_args.extend(
                    [
                        "--cleanup-package-files",
                        ",".join(
                            [v.strip() for v in cleanup_package_files if v.strip()]
                        ),
                    ]
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
                # serious_python skips copying Flutter packages to the temp dir
                # under --skip-site-packages, so register_flutter_extensions must
                # keep (not wipe) the permanent flutter-packages copy from the
                # previous build.
                self.site_packages_skipped = True
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
            if isinstance(package_result.stdout, str):
                console.log(package_result.stdout, style=verbose1_style)
            if isinstance(package_result.stderr, str):
                console.log(package_result.stderr, style=error_style)
            self.cleanup(package_result.returncode)

        hash.commit()

        # verify the package output: web ships app/app.zip; native platforms
        # stage the unpacked app to build/app for the native build to bundle.
        if self.package_platform == "Emscripten":
            app_zip_path = self.flutter_dir.joinpath("app", "app.zip")
            if not os.path.exists(app_zip_path):
                self.cleanup(1, "Flet app package app/app.zip was not created.")
        else:
            app_staging_dir = self.build_dir / "python-app"
            if not app_staging_dir.exists():
                self.cleanup(
                    1, f"Flet app package was not staged to {app_staging_dir}."
                )

        console.log(f"Packaged Python app {self.emojis['checkmark']}")

        # Drop the matching Pyodide runtime into the Flutter project's web/
        # directory so it ships in `flutter build web` output. Cached
        # per-version under ~/.flet/pyodide/<version>/ so subsequent builds
        # are no-ops.
        if self.package_platform == "Emscripten":
            from flet_cli.utils.pyodide import ensure_pyodide

            self.update_status("[bold blue]Preparing Pyodide runtime...")
            pyodide_dest = self.flutter_dir / "web" / "pyodide"
            ensure_pyodide(self.python_release.pyodide, pyodide_dest)
            console.log(
                f"Pyodide {self.python_release.pyodide} ready "
                f"{self.emojis['checkmark']}"
            )

    def get_bool_setting(self, cli_option, pyproj_setting, default_value):
        """
        Resolve a boolean setting with precedence: CLI option, pyproject, default.

        Args:
            cli_option: Value from CLI argument.
            pyproj_setting: Relative key under `tool.flet.<platform>.` and
                `tool.flet.`.
            default_value: Fallback value when no override is defined.

        Returns:
            Resolved boolean-like setting value.
        """

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

    def add_flutter_command_args(self, args: list[str]):
        """
        Hook for subclasses to append command-specific Flutter arguments.

        Args:
            args: Mutable argument list to extend.
        """

        pass

    def run_flutter(self):
        """
        Execute Flutter command for the current build target.
        """

        self._run_flutter_command()

    def _serious_python_build_env(self) -> dict:
        """
        serious_python environment for the platform NATIVE build (the Gradle /
        CMake / podspec steps run by `flutter build`).

        These tell the native build where the `package` step staged the app and
        site-packages and which embedded Python runtime to bundle. `flet build`
        applies them via `_run_flutter_command`; `flet test` applies the SAME set
        to the `flutter test` it spawns (see test.py `_flutter_path_env`) so both
        bundle an identical app. In particular, without `SERIOUS_PYTHON_APP` the
        Android `packageApp` Gradle task early-returns and a stale `app.zip` (e.g.
        an old-Python `main.pyc`) survives in the APK — `ImportError: bad magic
        number`. Built defensively so it is safe to call before the full build
        pipeline has populated every attribute.
        """

        env: dict = {}
        python_release = getattr(self, "python_release", None)
        if python_release is not None:
            # Only the short version is passed; serious_python derives the rest
            # from its committed manifest snapshot.
            env["SERIOUS_PYTHON_VERSION"] = python_release.short

        build_dir = getattr(self, "build_dir", None)
        package_platform = getattr(self, "package_platform", None)
        if build_dir is not None and package_platform != "Emscripten":
            env["SERIOUS_PYTHON_SITE_PACKAGES"] = str(build_dir / "site-packages")
            # app staging dir: read by the platform native build (CMake / podspec
            # / Android Gradle) at `flutter build` time to place the unpacked app
            # into the bundle.
            env["SERIOUS_PYTHON_APP"] = str(build_dir / "python-app")

        # Swift Package Manager (darwin): export the cache-bust key the package
        # step computed so the plugin's Package.swift re-resolves when the staged
        # native set changes (SwiftPM caches its graph on manifest text + env).
        if (
            build_dir is not None
            and package_platform in ("iOS", "Darwin")
            and self._darwin_spm_active()
        ):
            spm_key_file = build_dir / ".serious_python_spm_key"
            if spm_key_file.exists():
                env["SP_NATIVE_SET"] = spm_key_file.read_text().strip()

        # Path-hungry packages to ship extracted to disk: consumed by the
        # serious_python_android Gradle split during `flutter build`.
        if package_platform == "Android" and getattr(
            self, "android_extract_packages", None
        ):
            env["SERIOUS_PYTHON_ANDROID_EXTRACT_PACKAGES"] = ",".join(
                self.android_extract_packages
            )
        return env

    def _run_flutter_command(self):
        """
        Build final Flutter CLI command, configure environment, and run it.
        """

        assert self.options
        assert self.build_dir
        assert self.get_pyproject
        assert self.template_data
        assert self.target_platform

        # flutter build
        build_args = [self.flutter_exe]
        self.add_flutter_command_args(build_args)
        build_args.extend(
            [
                "--no-version-check",
                "--suppress-analytics",
            ]
        )

        # serious_python env for the native build, shared verbatim with `flet
        # test` (which spawns its own `flutter test`) so both bundle an identical
        # app — see `_serious_python_build_env`.
        build_env = self._serious_python_build_env()

        if self.package_platform == "Emscripten" and not self.template_data["no_wasm"]:
            build_args.append("--wasm")

        android_signing_key_store = (
            self.options.android_signing_key_store
            or self.get_pyproject("tool.flet.android.signing.key_store")
            or os.getenv("FLET_ANDROID_SIGNING_KEY_STORE")
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

        if android_signing_key_store:
            android_signing_key_alias = (
                self.options.android_signing_key_alias
                or self.get_pyproject("tool.flet.android.signing.key_alias")
                or os.getenv("FLET_ANDROID_SIGNING_KEY_ALIAS")
                or "upload"
            )
            build_env["FLET_ANDROID_SIGNING_KEY_ALIAS"] = android_signing_key_alias

        flutter_build_args = (
            self.options.flutter_build_args
            or self.get_pyproject(
                f"tool.flet.{self.config_platform}.flutter.build_args"
            )
            or self.get_pyproject("tool.flet.flutter.build_args")
        )
        if flutter_build_args:
            if isinstance(flutter_build_args, (list, tuple)):
                for arg in flutter_build_args:
                    if isinstance(arg, (list, tuple)):
                        build_args.extend(arg)
                    elif isinstance(arg, str):
                        build_args.append(arg)
            elif isinstance(flutter_build_args, str):
                build_args.append(flutter_build_args)

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
            if isinstance(build_result.stdout, str):
                console.log(build_result.stdout, style=verbose1_style)
            if isinstance(build_result.stderr, str):
                console.log(build_result.stderr, style=error_style)
            self.cleanup(build_result.returncode if build_result.returncode else 1)

    def resolve_output_path(self, build_output: str) -> str:
        """
        Resolve a platform `outputs` glob to an absolute path inside the
        Flutter project, substituting the `{arch}` and name placeholders.

        Args:
            build_output: An entry of `self.platforms[...]["outputs"]`.
        """

        assert self.flutter_dir
        assert self.template_data

        arch = platform.machine().lower()
        if arch in {"x86_64", "amd64"}:
            arch = "x64"
        elif arch in {"arm64", "aarch64"}:
            arch = "arm64"

        return (
            str(self.flutter_dir.joinpath(build_output))
            .replace("{arch}", arch)
            .replace("{artifact_name}", self.template_data["artifact_name"])
            .replace("{project_name}", self.template_data["project_name"])
            .replace("{product_name}", self.template_data["product_name"])
        )

    def copy_build_output(self):
        """
        Copy generated platform artifacts into the requested output directory.
        """

        assert self.template_data
        assert self.options
        assert self.flutter_dir
        assert self.out_dir
        assert self.assets_path
        assert self.target_platform

        self.update_status(
            f"[bold blue]Copying build to [cyan]{self.rel_out_dir}[/cyan] directory...",
        )

        def make_ignore_fn(out_dir, out_glob):
            """
            Create a shutil ignore callback that keeps only one selected output glob.
            """

            def ignore(path, names):
                """
                Filter sibling entries at `out_dir` so only `out_glob` is copied.
                """

                if path == out_dir and out_glob != "*":
                    return [f for f in os.listdir(path) if f != out_glob]
                return []

            return ignore

        for build_output in self.platforms[self.target_platform]["outputs"]:
            build_output_dir = self.resolve_output_path(build_output)

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

            # copy build result to out_dir
            copy_tree(
                build_output_dir,
                str(self.out_dir),
                ignore=make_ignore_fn(build_output_dir, build_output_glob),
            )

        if self.target_platform == "web" and self.assets_path.exists():
            # copy `assets` directory contents to the output directory
            copy_tree(str(self.assets_path), str(self.out_dir))
        elif self.target_platform in {"apk", "aab"}:
            self.rename_android_build_outputs()

        console.log(
            f"Copied build to [cyan]{self.rel_out_dir}[/cyan] "
            f"directory {self.emojis['checkmark']}"
        )

    def rename_android_build_outputs(self):
        """
        Rename copied Android release artifacts so they honor user-configured
        artifact names.

        Flutter outputs APK/AAB release files with an `app` prefix
        (`app-release.*`, `app-<abi>-release.*`), plus optional `.sha1` files.
        This method removes the `-release` segment and replaces only the
        leading `app` token with the resolved Flet artifact name.
        """
        assert self.target_platform
        assert self.out_dir
        assert self.template_data

        artifact_name = str(self.template_data["artifact_name"])
        output_ext = "apk" if self.target_platform == "apk" else "aab"
        release_suffix = f"-release.{output_ext}"
        release_hash_suffix = f"{release_suffix}.sha1"
        final_suffix = f".{output_ext}"
        final_hash_suffix = f"{final_suffix}.sha1"

        for output_file in self.out_dir.iterdir():
            if not output_file.is_file():
                continue

            name = output_file.name
            suffix = None
            final_file_suffix = None
            if name.endswith(release_hash_suffix):
                suffix = release_hash_suffix
                final_file_suffix = final_hash_suffix
            elif name.endswith(release_suffix):
                suffix = release_suffix
                final_file_suffix = final_suffix
            if suffix is None or final_file_suffix is None:
                continue

            prefix = name[: -len(suffix)]
            # Only rewrite Flutter default release outputs that start with `app`.
            if prefix != "app" and not prefix.startswith("app-"):
                continue

            # Keep ABI and hash suffixes, but drop `-release`.
            renamed = f"{artifact_name}{prefix[len('app') :]}{final_file_suffix}"
            if renamed == name:
                continue

            renamed_path = output_file.with_name(renamed)
            if renamed_path.exists():
                console.log(
                    f"Skipping rename of [cyan]{name}[/cyan] because "
                    f"[cyan]{renamed}[/cyan] already exists.",
                    style=warning_style,
                )
                continue

            output_file.rename(renamed_path)
            if self.verbose > 0:
                console.log(
                    f"Renamed build output from [cyan]{name}[/cyan] to "
                    f"[cyan]{renamed}[/cyan].",
                    style=verbose1_style,
                )

    def find_platform_image(
        self,
        src_path: Path,
        dest_path: Path,
        image_name: str,
        copy_ops: list,
        hash: HashStamp,
    ):
        """
        Find the best matching image file for the current target platform.

        When multiple files share the same base name (e.g. `icon.icns`,
        `icon.ico`, `icon.png`), the method filters out formats that are
        incompatible with the build target before selecting the first match.
        For example, `.icns` is skipped on Windows builds because
        `flutter_launcher_icons` cannot decode it.

        Args:
            src_path: Source assets directory.
            dest_path: Destination image directory.
            image_name: Base image name (without extension).
            copy_ops: Mutable copy operation list to append to.
            hash: Hash accumulator used for change detection.

        Returns:
            File name of matched image, or `None` if not found.
        """

        # .icns is macOS-only and .ico is Windows-only; filter out
        # incompatible formats so flutter_launcher_icons gets a decodable file.
        images = list(
            filter(
                lambda p: not (
                    (ext := Path(p).suffix.lower()) == ".icns"
                    and self.target_platform != "macos"
                    or ext == ".ico"
                    and self.target_platform != "windows"
                ),
                glob.glob(str(src_path.joinpath(f"{image_name}.*"))),
            )
        )

        if not images:
            return None

        best = images[0]
        if self.verbose > 0:
            console.log(f'Found "{image_name}" image at {best}', style=verbose1_style)
        copy_ops.append((best, dest_path))
        hash.update(best)
        hash.update(Path(best).stat().st_mtime)
        return Path(best).name

    def run(self, args, cwd, env: Optional[dict] = None, capture_output=True):
        """
        Run subprocess with merged environment and optional verbose logging.

        Args:
            args: Command and arguments to execute.
            cwd: Working directory for the process.
            env: Additional environment variables merged on top of `self.env`.
            capture_output: Whether process output should be captured.

        Returns:
            Process result object returned by `flet_cli.utils.processes.run`.
        """

        if self.verbose > 0:
            console.log(f"Run subprocess: {args}", style=verbose1_style)

        return processes.run(
            args,
            cwd,
            env={**self.env, **env} if env else self.env,
            capture_output=capture_output,
            log=self.log_stdout,
        )

    def load_yaml(self, path):
        """
        Load and parse a YAML document from disk.

        Args:
            path: YAML file path.

        Returns:
            Parsed YAML object.
        """

        with open(str(path), encoding="utf-8") as f:
            return yaml.safe_load(f)

    def save_yaml(self, path, doc):
        """
        Serialize YAML document to disk.

        Args:
            path: Destination YAML file path.
            doc: YAML-serializable document object.
        """

        with open(str(path), "w", encoding="utf-8") as f:
            yaml.dump(doc, f)
