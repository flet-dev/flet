import argparse
import os
from pathlib import Path

from packaging import version
from rich.console import Console
from rich.style import Style

import flet.version
from flet.utils import slugify
from flet_cli.commands.base import BaseCommand

error_style = Style(color="red1", bold=True)
console = Console(log_path=False)


class Command(BaseCommand):
    """
    Create a new Flet project using a predefined template.
    It sets up the initial directory structure, metadata,
    and required files to help you get started quickly.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "output_directory",
            type=str,
            default=".",
            nargs="?",
            help="Directory where the new Flet project will be created. "
            "If omitted, the project is created in the current directory",
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

    def handle(self, options: argparse.Namespace) -> None:
        from cookiecutter.main import cookiecutter

        self.verbose = options.verbose

        template_data = {
            "template_name": options.template,
            "flet_version": flet.version.flet_version,
            "sep": os.sep,
        }

        template_ref = options.template_ref
        if not template_ref:
            template_ref = version.Version(flet.version.flet_version).base_version

        out_dir = Path(options.output_directory).resolve()
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
                "gh:flet-dev/flet-app-templates",
                checkout=template_ref,
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

        if self.verbose > 0:
            console.print(f"[cyan]Files created at[/cyan] {out_dir}:\n")
            for root, _, files in os.walk(out_dir):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), out_dir)
                    console.print(rel_path)
            console.print("")

        # print next steps
        console.print("[cyan]Run the app:[/cyan]\n")
        app_dir = (
            os.path.relpath(out_dir, os.getcwd())
            if options.output_directory != "."
            else ""
        )
        console.print(f"flet run {app_dir}\n")
