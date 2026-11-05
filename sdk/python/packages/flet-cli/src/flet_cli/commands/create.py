import argparse
import os
import platform
import shutil
from pathlib import Path

from rich.console import Console
from rich.markup import escape
from rich.style import Style

import flet.version
from flet.utils import slugify
from flet_cli.commands.base import BaseCommand
from flet_cli.utils.cli import quote_for_shell
from flet_cli.utils.examples import (
    ExampleNotFoundError,
    copy_local_example,
    download_example,
    normalize_example_id,
    set_project_metadata,
    strip_tooling_only_tables,
)

error_style = Style(color="red1", bold=True)
console = Console(log_path=False)

DEFAULT_APP_TEMPLATE_URL = (
    "https://github.com/flet-dev/flet/releases/download/"
    "v{version}/flet-app-templates.zip"
)


class Command(BaseCommand):
    """
    Create a new Flet project using a predefined template.
    It sets up the initial directory structure, metadata,
    and required files to help you get started quickly.

    Detailed guide with usage examples: https://flet.dev/docs/getting-started/create-flet-app
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Register command-line options for creating a project from templates.

        Args:
            parser: Argument parser configured by the command runner.
        """

        parser.add_argument(
            "output_directory",
            type=str,
            default=None,
            nargs="?",
            help="Directory where the new Flet project will be created. "
            "If omitted, the project is created in the current directory, or, "
            "with `--example`, in a new directory named after the example",
        )
        parser.add_argument(
            "--project-name",
            dest="project_name",
            required=False,
            help="Name of the new Flet project. "
            "This will be used in metadata files such as `pyproject.toml`",
        )
        parser.add_argument(
            "--description",
            dest="description",
            required=False,
            help="Short description of the new Flet project. "
            "This will appear in generated metadata",
        )
        parser.add_argument(
            "--template",
            dest="template",
            type=str.lower,
            choices=["app", "extension"],
            default="app",
            required=False,
            help="The template to use (or type of project to create) "
            "for new Flet project",
        )
        parser.add_argument(
            "--template-ref",
            dest="template_ref",
            type=str,
            help="Git reference (branch, tag, or commit ID) of the Flet template "
            "repository (flet-dev/flet-app-templates) to use. Useful when using a "
            "custom or development version of templates",
        )
        parser.add_argument(
            "--example",
            dest="example",
            type=str,
            help="Create the project from a Flet example instead of a template. "
            "Takes the example's path in the examples directory of the Flet "
            "repository, e.g. `controls/material/button/basic`. Examples in the "
            "Flet docs show this command for their project",
        )
        parser.add_argument(
            "--example-ref",
            dest="example_ref",
            type=str,
            help="Git reference (branch, tag, or commit ID) of the Flet repository "
            "(flet-dev/flet) to fetch `--example` from. Defaults to the tag of the "
            "installed Flet version",
        )

    def handle(self, options: argparse.Namespace) -> None:
        """
        Render and generate a new project using the selected cookiecutter template.

        Args:
            options: Parsed command-line options.
        """

        self.verbose = options.verbose

        if options.example is not None:
            self._create_from_example(options)
            return

        from cookiecutter.main import cookiecutter

        system_name = platform.system().lower()
        platform_name = {
            "windows": "windows",
            "darwin": "darwin",
            "linux": "linux",
        }.get(system_name, system_name)

        template_data = {
            "template_name": options.template,
            "flet_version": flet.version.flet_version,
            "sep": os.sep,
            "platform": platform_name,
        }

        template_ref = options.template_ref
        if not template_ref:
            template_ref = flet.version.flet_version

        # Resolve template source: local dev, or zip from GitHub release
        local_tpl = Path(__file__).resolve().parents[5] / "templates" / "app"
        if local_tpl.is_dir():
            template_url = str(local_tpl)
            checkout = None
        else:
            template_url = DEFAULT_APP_TEMPLATE_URL.format(version=template_ref)
            checkout = None

        output_directory = options.output_directory or "."
        out_dir = Path(output_directory).resolve()
        template_data["out_dir"] = out_dir.name

        project_name = slugify(
            options.project_name if options.project_name else out_dir.name
        )
        template_data["project_name"] = project_name

        if options.description is not None:
            template_data["description"] = options.description

        # print("Template data:", template_data)
        try:
            cookiecutter(
                template_url,
                checkout=checkout,
                directory=options.template,
                output_dir=str(out_dir.parent),
                no_input=True,
                overwrite_if_exists=True,
                extra_context=template_data,
            )
        except Exception as e:
            console.print(
                f"Error creating the project from a template: {e}", style=error_style
            )
            exit(1)

        console.print(
            "The app has been created.\n", style=Style(color="green", bold=True)
        )

        self._print_next_steps(out_dir, output_directory, with_tests=True)

    def _create_from_example(self, options: argparse.Namespace) -> None:
        """
        Copy a Flet example project into the output directory.

        The example comes from the local Flet repository checkout when this
        package runs from one, otherwise from GitHub at `--example-ref`, which
        defaults to the tag of the installed Flet version.

        Args:
            options: Parsed command-line options.
        """

        try:
            example = normalize_example_id(options.example)
        except ExampleNotFoundError as e:
            console.print(f"Error: {e}", style=error_style)
            exit(1)

        output_directory = options.output_directory or example.rsplit("/", 1)[-1]
        out_dir = Path(output_directory).resolve()
        if out_dir.exists() and any(out_dir.iterdir()):
            console.print(
                f"Error: {escape(str(out_dir))} already exists and is not empty.",
                style=error_style,
            )
            exit(1)

        local_examples = Path(__file__).resolve().parents[5] / "examples"
        use_local = local_examples.is_dir() and not options.example_ref
        ref = options.example_ref or f"v{flet.version.flet_version}"
        created_out_dir = not out_dir.exists()
        try:
            if use_local:
                source = (local_examples / example).resolve()
                if not source.is_relative_to(local_examples.resolve()):
                    raise ExampleNotFoundError(f"Invalid example: {example!r}")
                copy_local_example(source, out_dir)
            else:
                with console.status(f"Downloading example {escape(example)}..."):
                    download_example(example, ref, out_dir)

            pyproject_path = out_dir / "pyproject.toml"
            pyproject = strip_tooling_only_tables(
                pyproject_path.read_text(encoding="utf-8")
            )
            renamed = set_project_metadata(
                pyproject,
                name=slugify(options.project_name or out_dir.name),
                description=options.description,
            )
            pyproject_path.write_text(renamed or pyproject, encoding="utf-8")
        except Exception as e:
            # The output directory was missing or empty, so everything in it is ours.
            if created_out_dir:
                shutil.rmtree(out_dir, ignore_errors=True)
            elif out_dir.is_dir():
                for child in out_dir.iterdir():
                    if child.is_dir() and not child.is_symlink():
                        shutil.rmtree(child, ignore_errors=True)
                    else:
                        child.unlink(missing_ok=True)
            if isinstance(e, ExampleNotFoundError):
                console.print(f"Error: {escape(str(e))}", style=error_style)
                if not use_local and not options.example_ref:
                    console.print(
                        "Examples are fetched for the installed Flet version. To "
                        "get the latest examples, add `--example-ref main`."
                    )
            else:
                console.print(
                    f"Error creating the project from an example: {escape(str(e))}",
                    style=error_style,
                )
            exit(1)

        if renamed is None:
            console.print(
                "Warning: couldn't set the project name in pyproject.toml; "
                "edit [project].name there by hand.",
                style=Style(color="yellow"),
            )

        console.print(
            "The app has been created.\n", style=Style(color="green", bold=True)
        )
        self._print_next_steps(out_dir, output_directory, with_tests=False)

    def _print_next_steps(
        self, out_dir: Path, output_directory: str, with_tests: bool
    ) -> None:
        """
        Print the created files when verbose, then the commands to run next.

        Args:
            out_dir: Resolved directory of the new project.
            output_directory: Output directory as the user gave it.
            with_tests: Whether the project has integration tests to run.
        """

        if self.verbose > 0:
            console.print(f"[cyan]Files created at[/cyan] {out_dir}:\n")
            for root, _, files in os.walk(out_dir):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), out_dir)
                    console.print(rel_path)
            console.print("")

        # print next steps
        app_dir = (
            os.path.relpath(out_dir, os.getcwd()) if output_directory != "." else ""
        )
        if app_dir:
            # The `cd` is meant to be pasted, so quote the path for the shell, then
            # escape rich markup so a directory named `[beta]` survives rendering.
            console.print(f"cd {escape(quote_for_shell(app_dir))}\n")

        console.print("[cyan]Run the app:[/cyan]\n")
        console.print("flet run\n")

        if with_tests:
            # print testing step
            console.print("[cyan]Run the integration tests:[/cyan]\n")
            console.print("flet test\n")
