import argparse
import os
import shutil
from pathlib import Path

from rich.console import Group
from rich.live import Live

from flet_cli.commands.build_base import BaseBuildCommand, console
from flet_cli.commands.flutter_base import verbose1_style
from flet_cli.utils.android import flutter_target_platforms
from flet_cli.utils.macos_sign import (
    MacOSSigningError,
    NotaryCredentials,
    notarize_and_staple,
    resolve_identity,
    sign_app,
)


class Command(BaseBuildCommand):
    """
    Build a Flet Python app into a platform-specific executable or
    installable bundle. It supports building for desktop (macOS, Linux, Windows), web,
    Android (APK/AAB), and iOS (IPA and simulator .app), with a wide range of
    customization options for metadata, assets, splash screens, and signing.

    Detailed usage guide: https://flet.dev/docs/publish
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Register build-specific CLI arguments.

        Args:
            parser: Argument parser configured by the command runner.
        """

        parser.add_argument(
            "target_platform",
            type=str.lower,
            choices=[
                "macos",
                "linux",
                "windows",
                "web",
                "apk",
                "aab",
                "ipa",
                "ios-simulator",
            ],
            help="The target platform or type of package to build",
        )
        parser.add_argument(
            "-o",
            "--output",
            dest="output_dir",
            required=False,
            help="Output directory for the final executable/bundle "
            "(default: <python_app_path>/build/<target_platform>)",
        )
        super().add_arguments(parser)

    def handle(self, options: argparse.Namespace) -> None:
        """
        Execute the full build pipeline for the selected target platform.

        Args:
            options: Parsed command-line options.
        """

        super().handle(options)
        assert self.target_platform
        self.status = console.status(
            f"[bold blue]Initializing {self.target_platform} build...",
            spinner="bouncingBall",
        )
        with Live(Group(self.status, self.progress), console=console) as self.live:
            self.initialize_command()
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
            self.run_flutter()
            self.copy_build_output()
            if self.target_platform == "macos":
                self.sign_macos_app()

            self.cleanup(
                0,
                message=(
                    f"Successfully built your [cyan]"
                    f"{self.platforms[self.target_platform]['status_text']}"
                    f"[/cyan]! {self.emojis['success']} "
                    f"Find it in [cyan]{self.rel_out_dir}[/cyan] directory. "
                    f"{self.emojis['directory']}"
                    + (
                        "\nRun [cyan]flet serve[/cyan] command to "
                        "start a web server with your app. "
                        if self.target_platform == "web"
                        else ""
                    )
                ),
            )

    def add_flutter_command_args(self, args: list[str]):
        """
        Append `flutter build` arguments derived from CLI options and project config.

        Args:
            args: Mutable command argument list to extend.
        """

        assert self.options
        assert self.build_dir
        assert self.get_pyproject
        assert self.template_data
        assert self.target_platform

        args.extend(
            ["build", self.platforms[self.target_platform]["flutter_build_command"]]
        )

        if self.target_platform == "apk" and self.template_data["split_per_abi"]:
            args.append("--split-per-abi")

        if (
            self.target_platform in ("apk", "aab")
            and self.template_data["options"]["target_arch"]
        ):
            args.extend(
                [
                    "--target-platform",
                    ",".join(
                        flutter_target_platforms(
                            self.template_data["options"]["target_arch"]
                        )
                    ),
                ]
            )

        if self.target_platform in ["ipa"]:
            if self.template_data["ios_provisioning_profile"]:
                args.extend(
                    [
                        "--export-options-plist",
                        "ios/exportOptions.plist",
                    ]
                )
            else:
                args.append("--no-codesign")
        elif self.target_platform == "ios-simulator":
            args.append("--simulator")

        build_number = self.options.build_number or self.get_pyproject(
            "tool.flet.build_number"
        )
        if build_number:
            args.extend(["--build-number", str(build_number)])

        build_version = (
            self.options.build_version
            or self.get_pyproject("project.version")
            or self.get_pyproject("tool.poetry.version")
        )
        if build_version:
            args.extend(["--build-name", build_version])

        for arg in (
            self.get_pyproject(f"tool.flet.{self.config_platform}.flutter.build_args")
            or self.get_pyproject("tool.flet.flutter.build_args")
            or []
        ):
            args.append(arg)

    def run_flutter(self):
        """
        Run Flutter build command and log completion status.
        """

        assert self.platforms
        assert self.target_platform

        self.update_status(
            f"[bold blue]Building [cyan]"
            f"{self.platforms[self.target_platform]['status_text']}[/cyan]..."
        )

        # Clear the build output directories of artifacts from previous runs. Flutter
        # only ever adds files to them, and copy_build_output harvests them wholesale —
        # so without this, a previous build with different options (e.g. --arch,
        # --split-per-abi, or a renamed product) would leak its artifacts into the
        # user's output directory.
        assert self.flutter_dir
        flutter_dir = self.flutter_dir.resolve()
        for output in self.platforms[self.target_platform]["outputs"]:
            output_dir = Path(
                os.path.dirname(self.resolve_output_path(output))
            ).resolve()
            # only delete directories that are strictly inside the generated Flutter
            # project (and never the project directory itself).
            if output_dir != flutter_dir and output_dir.is_relative_to(flutter_dir):
                shutil.rmtree(output_dir, ignore_errors=True)

        self._run_flutter_command()

        console.log(
            f"Built [cyan]{self.platforms[self.target_platform]['status_text']}"
            f"[/cyan] {self.emojis['checkmark']}",
        )

    def sign_macos_app(self):
        """
        Code-sign — and optionally notarize — the built macOS app bundle.

        No-op unless a signing identity is configured via
        `--macos-signing-identity`, `[tool.flet.macos.signing]` in
        pyproject.toml, or the `FLET_MACOS_SIGNING_IDENTITY` environment
        variable; the app then keeps the default ad-hoc signature produced
        by the Flutter build.
        """

        assert self.options
        assert self.get_pyproject
        assert self.out_dir
        assert self.flutter_dir

        identity = (
            self.options.macos_signing_identity
            or self.get_pyproject("tool.flet.macos.signing.identity")
            or os.getenv("FLET_MACOS_SIGNING_IDENTITY")
        )
        notarize = (
            self.options.macos_notarize
            if self.options.macos_notarize is not None
            else bool(self.get_pyproject("tool.flet.macos.signing.notarize"))
        )

        if not identity:
            if notarize:
                self.cleanup(
                    1,
                    "Notarization requires a code-signing identity. Pass "
                    "--macos-signing-identity or set "
                    "`[tool.flet.macos.signing].identity` in pyproject.toml.",
                )
            return

        apps = sorted(self.out_dir.glob("*.app"))
        if len(apps) != 1:
            self.cleanup(
                1,
                f"Expected exactly one .app bundle in {self.rel_out_dir}, "
                f"found {len(apps)}.",
            )
        app_path = apps[0]

        # The Xcode-generated entitlements file already contains the merged
        # defaults + [tool.flet.macos.entitlement] + --macos-entitlements
        # values; re-signing replaces the signature, so they must be
        # re-applied to the app bundle here.
        entitlements = self.flutter_dir / "macos" / "Runner" / "Release.entitlements"

        def log(message: str):
            if self.verbose > 0:
                console.log(message, style=verbose1_style)

        self.update_status(f"[bold blue]Signing [cyan]{app_path.name}[/cyan]...")
        try:
            resolved = resolve_identity(identity)
            if notarize and resolved.is_adhoc:
                self.cleanup(
                    1,
                    "Notarization requires a Developer ID identity; "
                    'ad-hoc ("-") signed apps cannot be notarized.',
                )
            signed_count = sign_app(
                app_path,
                resolved,
                entitlements=entitlements if entitlements.is_file() else None,
                log=log,
            )
            console.log(
                f"Signed [cyan]{app_path.name}[/cyan] ({signed_count} binaries, "
                f"identity: {resolved.description}) {self.emojis['checkmark']}"
            )

            if notarize:
                credentials = self._macos_notary_credentials()
                self.update_status(
                    f"[bold blue]Notarizing [cyan]{app_path.name}[/cyan] "
                    "(this can take a few minutes)...",
                )
                notarize_and_staple(app_path, credentials, log=log)
                console.log(
                    f"Notarized and stapled [cyan]{app_path.name}[/cyan] "
                    f"{self.emojis['checkmark']}"
                )
        except MacOSSigningError as e:
            self.cleanup(1, str(e))

    def _macos_notary_credentials(self) -> NotaryCredentials:
        """
        Resolve Apple notary service credentials: CLI over pyproject.toml over
        environment, with the flet-specific profile variable ranking above
        ambient App Store Connect API key variables that other tooling may
        have exported.
        """

        assert self.options
        assert self.get_pyproject

        profile = (
            self.options.macos_notary_profile
            or self.get_pyproject("tool.flet.macos.signing.notary_profile")
            or os.getenv("FLET_MACOS_NOTARY_PROFILE")
        )
        if profile:
            return NotaryCredentials(keychain_profile=profile)

        api_key = os.getenv("APPLE_API_KEY")
        api_key_id = os.getenv("APPLE_API_KEY_ID")
        api_issuer = os.getenv("APPLE_API_ISSUER")
        if api_key and api_key_id and api_issuer:
            return NotaryCredentials(
                api_key=api_key, api_key_id=api_key_id, api_issuer=api_issuer
            )

        self.cleanup(
            1,
            "Notary service credentials are missing. Either store an "
            "App Store Connect API key or Apple ID app-specific password "
            "with `xcrun notarytool store-credentials <profile>` and pass "
            "--macos-notary-profile <profile>, or set the APPLE_API_KEY, "
            "APPLE_API_KEY_ID and APPLE_API_ISSUER environment variables.",
        )
