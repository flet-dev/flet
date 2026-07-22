import argparse
import os
import plistlib
import shutil
import tempfile
from pathlib import Path

from rich.console import Group
from rich.live import Live

from flet_cli.commands.build_base import BaseBuildCommand, console
from flet_cli.commands.flutter_base import verbose1_style
from flet_cli.utils.android import flutter_target_platforms
from flet_cli.utils.macos_sign import (
    MacOSSigningError,
    NotaryCredentials,
    SigningIdentity,
    build_pkg,
    identity_team_id,
    notarize_and_staple,
    profile_application_identifier,
    resolve_identity,
    sign_app,
    verify_app_store_app,
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

        Runs after `copy_build_output()` and operates on the final `.app`
        in the output directory, i.e. the artifact users distribute.

        No-op unless a signing identity is configured; without one, the app keeps the
        default ad-hoc signature produced by the Flutter build. Notarization is
        additionally gated and requires a real (non-ad-hoc) identity plus notary
        credentials.

        The app-bundle signature re-applies the entitlements from the
        template-generated `Release.entitlements` — re-signing replaces the
        signature Xcode embedded them in, so they must be supplied again.

        Exits via `cleanup(1, ...)` with an actionable message on any
        configuration or signing failure.
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
        app_store = (
            self.options.macos_app_store
            if self.options.macos_app_store is not None
            else bool(self.get_pyproject("tool.flet.macos.signing.app_store"))
        )

        if app_store and notarize:
            self.cleanup(
                1,
                "App Store builds are not notarized — Apple reviews and "
                "re-signs store builds itself. Remove --macos-notarize / "
                "`[tool.flet.macos.signing].notarize`.",
            )

        if not identity:
            if notarize:
                self.cleanup(
                    1,
                    "Notarization requires a code-signing identity. Pass "
                    "--macos-signing-identity or set "
                    "`[tool.flet.macos.signing].identity` in pyproject.toml.",
                )
            if app_store:
                self.cleanup(
                    1,
                    "App Store signing requires an Apple Distribution "
                    "identity. Pass --macos-signing-identity or set "
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

        # Release.entitlements is the single merged source of entitlements.
        # Signing without it would produce a hardened-runtime app missing the
        # allow-jit/allow-unsigned-executable-memory exceptions Python needs, producing
        # an app that signs fine and crashes at launch.
        entitlements = self.flutter_dir / "macos" / "Runner" / "Release.entitlements"
        if not entitlements.is_file():
            self.cleanup(
                1,
                f"Entitlements file not found: {entitlements}. The Flutter "
                "build directory is incomplete; re-run the build.",
            )

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

            if app_store:
                self._sign_macos_app_store(app_path, resolved, entitlements, log)
                return

            signed_count = sign_app(
                app_path,
                resolved,
                entitlements=entitlements,
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

    def _sign_macos_app_store(
        self,
        app_path: Path,
        identity: SigningIdentity,
        entitlements: Path,
        log,
    ):
        """
        Sign for Mac App Store / TestFlight and build the installer package.

        The store lane differs from Developer ID signing in every dimension
        that matters: the app is signed with an Apple Distribution identity
        *without* the hardened runtime; entitlements are the template's with
        all `com.apple.security.cs.*` hardened-runtime exceptions stripped,
        App Sandbox forced on, and the `application-identifier` /
        `team-identifier` pair injected; helper executables carry exactly
        the sandbox-inherit pair; a provisioning profile is embedded; and
        the deliverable is a `.pkg` signed with an installer certificate,
        not a notarized `.app`.

        All prerequisites — installer identity, Team ID, provisioning
        profile, and the `LSApplicationCategoryType` Info.plist key App
        Store validation demands — are checked before any signing work, so
        misconfiguration fails asap.

        Exits via `cleanup(1, ...)` on any failure.
        """

        assert self.options
        assert self.get_pyproject
        assert self.out_dir
        assert self.python_app_path

        # Fail-fast prerequisite resolution, cheapest checks first.
        if identity.is_adhoc:
            self.cleanup(
                1,
                'App Store builds cannot be signed ad-hoc ("-"); use your '
                "Apple Distribution certificate.",
            )
        if "Developer ID" in identity.name:
            console.log(
                f"[yellow]Warning: signing an App Store build with "
                f'"{identity.name}" — App Store Connect only accepts Apple '
                "Distribution (or 3rd Party Mac Developer Application) "
                "certificates.[/yellow]"
            )
        team_id = identity_team_id(identity)
        if not team_id:
            self.cleanup(
                1,
                f'Cannot determine the Team ID from identity "{identity.name}". '
                "App Store entitlements require it.",
            )

        installer_identity = (
            self.options.macos_installer_identity
            or self.get_pyproject("tool.flet.macos.signing.installer_identity")
            or os.getenv("FLET_MACOS_INSTALLER_IDENTITY")
        )
        if not installer_identity:
            self.cleanup(
                1,
                "App Store builds need an installer certificate to sign the "
                ".pkg. Pass --macos-installer-identity or set "
                "`[tool.flet.macos.signing].installer_identity` "
                '(e.g. "3rd Party Mac Developer Installer: ... (TEAMID)").',
            )
        # Installer certs sign packages, not code — resolved under the
        # `basic` policy, and before the signing pass so a typo fails fast.
        installer = resolve_identity(installer_identity, policy="basic")

        profile = (
            self.options.macos_provisioning_profile
            or self.get_pyproject("tool.flet.macos.signing.provisioning_profile")
            or os.getenv("FLET_MACOS_PROVISIONING_PROFILE")
        )
        if not profile:
            self.cleanup(
                1,
                "App Store builds need a Mac App Store provisioning profile. "
                "Pass --macos-provisioning-profile or set "
                "`[tool.flet.macos.signing].provisioning_profile`.",
            )
        profile_path = Path(profile)
        if not profile_path.is_absolute():
            profile_path = (self.python_app_path / profile_path).resolve()
        if not profile_path.is_file():
            self.cleanup(1, f"Provisioning profile not found: {profile_path}")

        # Read the *built* app's bundle id — the authoritative value after
        # all project/org/bundle-id resolution and templating.
        info_path = app_path / "Contents" / "Info.plist"
        info = plistlib.loads(info_path.read_bytes())
        bundle_id = info["CFBundleIdentifier"]
        application_identifier = f"{team_id}.{bundle_id}"

        # App Store validation hard-requires a category (empirically: 409
        # "The Info.plist must contain a LSApplicationCategoryType key").
        if not info.get("LSApplicationCategoryType"):
            self.cleanup(
                1,
                "App Store submissions require the LSApplicationCategoryType "
                "Info.plist key. Add it with --info-plist "
                'LSApplicationCategoryType="public.app-category.<category>" '
                "or `[tool.flet.macos.info]` in pyproject.toml.",
            )
        if "ITSAppUsesNonExemptEncryption" not in info:
            console.log(
                "[yellow]Warning: ITSAppUsesNonExemptEncryption is not set in "
                "Info.plist — App Store Connect will ask the export-compliance "
                "question manually for every build. Set it with --info-plist "
                "ITSAppUsesNonExemptEncryption=False if your app only uses "
                "standard encryption.[/yellow]"
            )

        profile_app_id = profile_application_identifier(profile_path)
        if profile_app_id is not None and profile_app_id not in (
            application_identifier,
            f"{team_id}.*",
        ):
            self.cleanup(
                1,
                f"The provisioning profile authorizes {profile_app_id!r} but "
                f"the app's identifier is {application_identifier!r}. "
                "TestFlight rejects mismatched builds (ITMS-90889); create a "
                "profile for this bundle id.",
            )

        # Store entitlements: the template's, minus every hardened-runtime
        # exception (meaningless without the hardened runtime, and scrutinized
        # by App Review), with the sandbox and identifiers forced in.
        with open(entitlements, "rb") as f:
            app_entitlements = {
                k: v
                for k, v in plistlib.load(f).items()
                if not k.startswith("com.apple.security.cs.")
            }
        app_entitlements["com.apple.security.app-sandbox"] = True
        app_entitlements["com.apple.application-identifier"] = application_identifier
        app_entitlements["com.apple.developer.team-identifier"] = team_id
        helper_entitlements = {
            "com.apple.security.app-sandbox": True,
            "com.apple.security.inherit": True,
        }

        with tempfile.TemporaryDirectory() as tmp:
            app_ents_path = Path(tmp) / "app.entitlements"
            app_ents_path.write_bytes(plistlib.dumps(app_entitlements))
            helper_ents_path = Path(tmp) / "helper.entitlements"
            helper_ents_path.write_bytes(plistlib.dumps(helper_entitlements))

            signed_count = sign_app(
                app_path,
                identity,
                entitlements=app_ents_path,
                helper_entitlements=helper_ents_path,
                provisioning_profile=profile_path,
                hardened_runtime=False,
                log=log,
            )
        verify_app_store_app(app_path, application_identifier)
        console.log(
            f"Signed [cyan]{app_path.name}[/cyan] for the App Store "
            f"({signed_count} binaries, identity: {identity.description}) "
            f"{self.emojis['checkmark']}"
        )

        self.update_status(f"[bold blue]Packaging [cyan]{app_path.stem}.pkg[/cyan]...")
        pkg = build_pkg(
            app_path,
            installer,
            self.out_dir / f"{app_path.stem}.pkg",
            log=log,
        )
        console.log(
            f"Packaged [cyan]{pkg.name}[/cyan] for App Store Connect "
            f"(installer identity: {installer.name}) {self.emojis['checkmark']}"
        )

    def _macos_notary_credentials(self) -> NotaryCredentials:
        """
        Resolve Apple notary service credentials.

        A keychain profile is looked up first and if not set, then the
        `APPLE_API_KEY`/`APPLE_API_KEY_ID`/`APPLE_API_ISSUER` App Store Connect
        API key variables (all three required) are looked up next.
        A configured profile deliberately outranks the `APPLE_API_*` variables, which
        other tooling (Fastlane, CI images) may have exported ambiently, possibly for
        a different Apple team.

        Returns:
            Credentials for `notarytool`; exits via `cleanup(1, ...)` with
                setup instructions when nothing is configured.
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
