import argparse
import os
import plistlib
import shutil
import tempfile
from pathlib import Path
from typing import Callable, Optional

from rich.console import Group
from rich.live import Live

from flet_cli.commands.build_base import BaseBuildCommand, console
from flet_cli.commands.flutter_base import verbose1_style
from flet_cli.utils.android import flutter_target_platforms
from flet_cli.utils.ios_sign import (
    find_provisioning_profile,
    installed_provisioning_profiles,
)
from flet_cli.utils.macos_sign import (
    APP_STORE_CERTIFICATE_TYPES,
    APP_STORE_HELPER_ENTITLEMENTS,
    DEVELOPER_ID_CERTIFICATE_TYPES,
    INSTALLER_CERTIFICATE_TYPES,
    MacOSSigningError,
    NotaryCredentials,
    SigningIdentity,
    app_store_entitlements,
    build_pkg,
    identity_team_id,
    notarize_and_staple,
    profile_application_identifier,
    profile_covers_application,
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
            if self.target_platform == "macos":
                self.preflight_macos_signing()
            elif self.target_platform == "ipa":
                self.preflight_ios_signing()
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

    def preflight_ios_signing(self) -> None:
        """
        Validate the configured provisioning profile before any build work.

        Xcode resolves `PROVISIONING_PROFILE_SPECIFIER` only when it
        archives, minutes into the build, and reports a miss without naming
        the profiles it did find. Resolving the same specifier here — by
        name or UUID, as Xcode does — reports the alternatives instead, and
        additionally checks expiry, team match, and bundle-id coverage,
        which Xcode only surfaces later at signing.

        A build with no profile configured is left alone: it is signed with
        `--no-codesign` and produces an `.xcarchive`.

        Exits via `cleanup(1, ...)` when the profile cannot be used.
        """

        assert self.template_data

        specifier = self.template_data.get("ios_provisioning_profile")
        if not specifier:
            # Unsigned build: Flutter is passed --no-codesign and produces an
            # .xcarchive only, which is a supported outcome.
            return

        profiles = installed_provisioning_profiles()
        profile = find_provisioning_profile(specifier, profiles)
        if profile is None:
            usable = [p for p in profiles if not p.expired]
            if usable:
                listing = "\n".join(
                    f"  - {p.name!r} (team {p.team_id}, UUID {p.uuid})" for p in usable
                )
                hint = f"Installed profiles:\n{listing}"
            else:
                hint = (
                    "No unexpired profiles are installed. Download the "
                    "profile from the Apple Developer portal and double-click "
                    "it, or copy it into "
                    "~/Library/MobileDevice/Provisioning Profiles."
                )
            self.cleanup(
                1,
                f"Provisioning profile {specifier!r} is not installed — Xcode "
                f"would fail once the build reaches signing. Configure the "
                f"profile's name or UUID exactly as the portal shows it.\n"
                f"{hint}",
            )
            return

        if profile.expired:
            self.cleanup(
                1,
                f"Provisioning profile {profile.name!r} expired on "
                f"{profile.expires:%Y-%m-%d}. Regenerate it in the Apple "
                f"Developer portal and install the new one.",
            )

        team_id = self.template_data.get("ios_team_id")
        if team_id and profile.team_id and profile.team_id != team_id:
            self.cleanup(
                1,
                f"Provisioning profile {profile.name!r} belongs to team "
                f"{profile.team_id}, but the build is configured for team "
                f"{team_id}. Xcode matches the profile within the team, so "
                f"these must agree.",
            )

        bundle_id = self.template_data.get("bundle_id")
        app_id = profile.application_identifier
        if bundle_id and app_id:
            # application-identifier is "<TEAM>.<bundle id>", explicit or
            # wildcard; compare only the bundle-id part.
            authorized = app_id.split(".", 1)[-1]
            covers = (
                authorized == bundle_id
                if not authorized.endswith("*")
                else bundle_id.startswith(authorized[:-1])
            )
            if not covers:
                self.cleanup(
                    1,
                    f"Provisioning profile {profile.name!r} authorizes "
                    f"{authorized!r}, which does not cover the app's bundle "
                    f"id {bundle_id!r}. Use a profile registered for this "
                    f"App ID.",
                )

    # Valid values of the macOS distribution lane selector. A single enum —
    # instead of per-lane booleans — makes conflicting lanes inexpressible
    # and lets one pyproject hold both lanes' settings, with the CLI
    # flipping between them per build.
    MACOS_DISTRIBUTIONS = ("none", "developer-id", "app-store")

    def resolve_macos_distribution(self) -> str:
        """
        Resolve and validate the macOS distribution lane.

        `choices=` only validates the CLI layer, so the resolved value is
        checked again here — a typo in `pyproject.toml` (e.g. `app_store`)
        must fail loudly, not fall through to a silently ad-hoc build. For
        the same reason, per-lane subtable names under
        `[tool.flet.macos.signing]` are validated: a misnamed subtable
        would otherwise be silently ignored.

        Returns:
            One of `MACOS_DISTRIBUTIONS`; exits via `cleanup(1, ...)` on an
                invalid configured value or a misnamed lane subtable.
        """

        assert self.options
        assert self.get_pyproject

        distribution = (
            self.options.macos_distribution
            or self.get_pyproject("tool.flet.macos.signing.distribution")
            or "none"
        )
        if distribution not in self.MACOS_DISTRIBUTIONS:
            self.cleanup(
                1,
                f"Invalid macOS distribution {distribution!r}. Valid values "
                f"for --macos-distribution / "
                f"`[tool.flet.macos.signing].distribution`: "
                f"{', '.join(self.MACOS_DISTRIBUTIONS)}.",
            )
        lane_names = [d for d in self.MACOS_DISTRIBUTIONS if d != "none"]
        for key, value in (self.get_pyproject("tool.flet.macos.signing") or {}).items():
            if not isinstance(value, dict):
                continue
            if key == "none":
                self.cleanup(
                    1,
                    "`[tool.flet.macos.signing.none]` is not a lane subtable "
                    "— the `none` lane reads no signing settings, so it "
                    "would be silently ignored. Put shared values directly "
                    "on `[tool.flet.macos.signing]`.",
                )
            elif key not in lane_names:
                self.cleanup(
                    1,
                    f"Unknown lane subtable `[tool.flet.macos.signing.{key}]` "
                    f"— it would be silently ignored. Valid lane names: "
                    f"{', '.join(lane_names)}.",
                )
        return distribution

    def macos_signing_setting(
        self,
        cli_value: Optional[str],
        distribution: str,
        key: str,
        env_var: Optional[str] = None,
    ) -> Optional[str]:
        """
        Resolve a signing setting with per-lane awareness.

        Precedence: CLI option > `[tool.flet.macos.signing.<lane>]`
        subtable > flat `[tool.flet.macos.signing]` key > environment
        variable.

        Args:
            cli_value: The already-parsed CLI option value, or None.
            distribution: The resolved lane; `none` has no subtable.
            key: Key name under `[tool.flet.macos.signing]`.
            env_var: Environment variable fallback, if the setting has one.

        Returns:
            The resolved value, or None when the setting is not configured.
        """

        assert self.get_pyproject

        return (
            cli_value
            or (
                self.get_pyproject(f"tool.flet.macos.signing.{distribution}.{key}")
                if distribution != "none"
                else None
            )
            or self.get_pyproject(f"tool.flet.macos.signing.{key}")
            or (os.getenv(env_var) if env_var else None)
        )

    def _macos_store_profile_path(self) -> Path:
        """
        Resolve the configured Mac App Store provisioning profile to a path.

        Relative paths resolve against the project directory. Exits via
        `cleanup(1, ...)` when no profile is configured or the file does
        not exist.
        """

        assert self.options
        assert self.get_pyproject
        assert self.python_app_path

        profile = self.macos_signing_setting(
            cli_value=self.options.macos_provisioning_profile,
            distribution="app-store",
            key="provisioning_profile",
            env_var="FLET_MACOS_PROVISIONING_PROFILE",
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
        return profile_path

    def preflight_macos_signing(self) -> None:
        """
        Validate the signing configuration before any build work.

        Signing runs after the multi-minute Flutter build, so configuration
        mistakes — a typo'd, ambiguous, or expired identity, missing notary
        credentials, a missing provisioning profile or store category —
        would otherwise surface only at the very end. This resolves the
        same settings the signing step will use and fails in seconds
        instead. The signing step re-checks everything (the keychain is
        the authority and can change); this is purely an early exit, and a
        no-op for builds with no signing configured.

        Exits via `cleanup(1, ...)` on any configuration error.
        """

        assert self.options
        assert self.get_pyproject
        assert self.template_data

        distribution = self.resolve_macos_distribution()
        identity = self.macos_signing_setting(
            cli_value=self.options.macos_signing_identity,
            distribution=distribution,
            key="identity",
            env_var="FLET_MACOS_SIGNING_IDENTITY",
        )
        if not identity and distribution == "none":
            return

        if distribution != "none" and (identity or "").strip() == "-":
            self.cleanup(
                1,
                f"The ad-hoc identity ('-') cannot be used with the "
                f"'{distribution}' distribution — ad-hoc signatures cannot "
                f"be notarized or uploaded. Configure a real signing "
                f"identity, or build with --macos-distribution none.",
            )

        try:
            if distribution == "app-store":
                resolve_identity(identity, types=APP_STORE_CERTIFICATE_TYPES)
                resolve_identity(
                    self.macos_signing_setting(
                        cli_value=self.options.macos_installer_identity,
                        distribution=distribution,
                        key="installer_identity",
                        env_var="FLET_MACOS_INSTALLER_IDENTITY",
                    ),
                    policy="basic",
                    types=INSTALLER_CERTIFICATE_TYPES,
                )
            elif distribution == "developer-id":
                resolve_identity(identity, types=DEVELOPER_ID_CERTIFICATE_TYPES)
                self._macos_notary_credentials()
            else:
                resolve_identity(identity)
        except MacOSSigningError as e:
            self.cleanup(1, str(e))

        if distribution == "app-store":
            self._macos_store_profile_path()
            # The authoritative check reads the built app's Info.plist; this
            # one catches the common case — the key not configured at all —
            # before the build.
            if not self.template_data["options"]["info_plist"].get(
                "LSApplicationCategoryType"
            ):
                self.cleanup(
                    1,
                    "App Store submissions require the LSApplicationCategoryType "
                    "Info.plist key. Add it with --info-plist "
                    'LSApplicationCategoryType="public.app-category.<category>" '
                    "or `[tool.flet.macos.info]` in pyproject.toml.",
                )

    def sign_macos_app(self) -> None:
        """
        Code-sign and package the built macOS app bundle for its
        distribution lane.

        Runs after `copy_build_output()` and operates on the final `.app`
        in the output directory, i.e. the artifact users distribute. The
        lane comes from `resolve_macos_distribution()`:

        - `none` (default) — sign only when a signing identity is
          configured; without one, the app keeps the ad-hoc signature
          produced by the Flutter build.
        - `developer-id` — sign with the hardened runtime, notarize, and
          staple for direct distribution.
        - `app-store` — sandboxed store signing plus a signed installer
          `.pkg` (see `_sign_macos_app_store()`).

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

        distribution = self.resolve_macos_distribution()
        identity = self.macos_signing_setting(
            cli_value=self.options.macos_signing_identity,
            distribution=distribution,
            key="identity",
            env_var="FLET_MACOS_SIGNING_IDENTITY",
        )

        # Distribution lanes require an identity anyway, so an unset one
        # auto-discovers (resolve_identity with types, below). A plain
        # build without an identity keeps its ad-hoc signature.
        if not identity and distribution == "none":
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
            # Each lane scopes resolution to the certificate type Apple's
            # services accept for it — which also lets an unset identity
            # auto-discover the only candidate. The plain lane stays
            # unscoped: Apple Development or corporate certificates are
            # legitimate there.
            if distribution == "app-store":
                resolved = resolve_identity(identity, types=APP_STORE_CERTIFICATE_TYPES)
            elif distribution == "developer-id":
                resolved = resolve_identity(
                    identity, types=DEVELOPER_ID_CERTIFICATE_TYPES
                )
            else:
                resolved = resolve_identity(identity)
            if not identity:
                console.log(f"Signing identity: {resolved.name}")
            if distribution == "developer-id" and resolved.is_adhoc:
                self.cleanup(
                    1,
                    "Developer ID distribution requires a Developer ID "
                    'identity; ad-hoc ("-") signed apps cannot be notarized.',
                )

            if distribution == "app-store":
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

            if distribution == "developer-id":
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
        log: Callable[[str], None],
    ) -> None:
        """
        Sign for Mac App Store / TestFlight and build the installer package.

        The store lane differs from Developer ID signing in every dimension
        that matters: the app is signed with an Apple Distribution identity
        *without* the hardened runtime; entitlements come from
        `app_store_entitlements()` (sandbox on, identifiers in, `cs.*`
        exceptions stripped); helper executables and nested helper bundles
        carry the sandbox-inherit pair; a provisioning profile is embedded;
        and the deliverable is a `.pkg` signed with an installer
        certificate, not a notarized `.app`.

        All prerequisites — installer identity, Team ID, provisioning
        profile, and the `LSApplicationCategoryType` Info.plist key App
        Store validation demands — are checked before any signing work, so
        misconfiguration fails in seconds rather than after the
        multi-minute signing pass.

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
        team_id = identity_team_id(identity)
        if not team_id:
            self.cleanup(
                1,
                f'Cannot determine the Team ID from identity "{identity.name}". '
                "App Store entitlements require it.",
            )

        installer_identity = self.macos_signing_setting(
            cli_value=self.options.macos_installer_identity,
            distribution="app-store",
            key="installer_identity",
            env_var="FLET_MACOS_INSTALLER_IDENTITY",
        )
        # Installer certs sign packages, not code — resolved under the
        # `basic` policy, scoped to installer types (the policy also lists
        # application certs), before the signing pass so a typo fails fast.
        # An unset identity auto-discovers the only installer certificate.
        installer = resolve_identity(
            installer_identity, policy="basic", types=INSTALLER_CERTIFICATE_TYPES
        )
        if installer.is_adhoc:
            self.cleanup(
                1,
                "Store packages cannot be signed ad-hoc; use your "
                '"3rd Party Mac Developer Installer" / "Mac Installer '
                'Distribution" certificate.',
            )
        if not installer_identity:
            console.log(f"Installer identity: {installer.name}")

        profile_path = self._macos_store_profile_path()

        # Read the *built* app's bundle id — the authoritative value after
        # all project/org/bundle-id resolution and templating.
        info_path = app_path / "Contents" / "Info.plist"
        try:
            info = plistlib.loads(info_path.read_bytes())
            bundle_id = info["CFBundleIdentifier"]
        except (OSError, plistlib.InvalidFileException, ValueError, KeyError) as e:
            self.cleanup(
                1,
                f"Cannot read CFBundleIdentifier from {info_path}: {e}. "
                "The built app bundle is malformed; re-run the build.",
            )
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
        if profile_app_id is not None and not profile_covers_application(
            profile_app_id, application_identifier
        ):
            self.cleanup(
                1,
                f"The provisioning profile authorizes {profile_app_id!r} but "
                f"the app's identifier is {application_identifier!r}. "
                "TestFlight rejects mismatched builds (ITMS-90889); create a "
                "profile for this bundle id.",
            )

        # MacOSSigningError from here on is handled by sign_macos_app's
        # enclosing try block.
        app_entitlements = app_store_entitlements(
            entitlements, application_identifier, team_id
        )

        with tempfile.TemporaryDirectory() as tmp:
            app_ents_path = Path(tmp) / "app.entitlements"
            app_ents_path.write_bytes(plistlib.dumps(app_entitlements))
            helper_ents_path = Path(tmp) / "helper.entitlements"
            helper_ents_path.write_bytes(plistlib.dumps(APP_STORE_HELPER_ENTITLEMENTS))

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

        profile = self.macos_signing_setting(
            cli_value=self.options.macos_notary_profile,
            distribution="developer-id",
            key="notary_profile",
            env_var="FLET_MACOS_NOTARY_PROFILE",
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
