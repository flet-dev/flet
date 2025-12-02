import argparse

from rich.console import Group
from rich.live import Live

from flet_cli.commands.build_base import BaseBuildCommand, console


class Command(BaseBuildCommand):
    """
    Build a Flet Python app into a platform-specific executable or
    installable bundle. It supports building for desktop (macOS, Linux, Windows), web,
    Android (APK/AAB), and iOS (IPA), with a wide range of customization options for
    metadata, assets, splash screens, and signing.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        super().__init__(parser)

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "target_platform",
            type=str.lower,
            choices=["macos", "linux", "windows", "web", "apk", "aab", "ipa"],
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
        assert self.options
        assert self.build_dir
        assert self.get_pyproject
        assert self.template_data
        assert self.target_platform

        args.extend(
            ["build", self.platforms[self.target_platform]["flutter_build_command"]]
        )

        if self.target_platform in "apk" and self.template_data["split_per_abi"]:
            args.append("--split-per-abi")

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
        assert self.platforms
        assert self.target_platform

        self.update_status(
            f"[bold blue]Building [cyan]"
            f"{self.platforms[self.target_platform]['status_text']}[/cyan]..."
        )

        self._run_flutter_command()

        console.log(
            f"Built [cyan]{self.platforms[self.target_platform]['status_text']}"
            f"[/cyan] {self.emojis['checkmark']}",
        )
