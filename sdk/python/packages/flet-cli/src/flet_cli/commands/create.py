import argparse
import os
from pathlib import Path

import flet.version
from flet.utils import slugify
from flet_cli.commands.base import BaseCommand
from packaging import version
from rich.console import Console
from rich.style import Style

error_style = Style(color="red1", bold=True)
console = Console(log_path=False)


class Command(BaseCommand):
    """
    Create a new Flet app from a template.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "output_directory",
            type=str,
            default=".",
            nargs="?",
            help="project output directory",
        )
        parser.add_argument(
            "--project-name",
            dest="project_name",
            help="project name for the new Flet app",
            required=False,
        )
        parser.add_argument(
            "--description",
            dest="description",
            help="the description to use for the new Flet project",
            required=False,
        )
        parser.add_argument(
            "--template",
            dest="template",
            choices=["app", "extension"],
            default="app",
            help="template to use for new Flet project",
            required=False,
        )
        parser.add_argument(
            "--template-ref",
            dest="template_ref",
            type=str,
            help="the branch, tag or commit ID to checkout after cloning the repository with Flet app templates",
        )

    def handle(self, options: argparse.Namespace) -> None:
        from cookiecutter.main import cookiecutter

        self.verbose = options.verbose

        template_data = {
            "template_name": options.template,
            "flet_version": flet.version.version,
            "sep": os.sep,
        }

        template_ref = options.template_ref
        if not template_ref and flet.version.version:
            template_ref = version.Version(flet.version.version).base_version

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
                f"gh:flet-dev/flet-app-templates",
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
            for root, dirs, files in os.walk(out_dir):
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
