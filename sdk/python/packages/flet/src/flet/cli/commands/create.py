import argparse
import os
from pathlib import Path

import flet.version
from flet.cli.commands.base import BaseCommand
from flet_core.utils import slugify
from packaging import version
from rich import print


class Command(BaseCommand):
    """
    Create a new Flet app from a template.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "output_directory",
            type=str,
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
            choices=["minimal", "counter"],
            default="minimal",
            help="template to use for new Flet project",
            required=False,
        )

    def handle(self, options: argparse.Namespace) -> None:
        from cookiecutter.main import cookiecutter

        self.verbose = options.verbose

        template_data = {"template_name": options.template}

        template_ref = None
        if flet.version.version:
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
        cookiecutter(
            f"gh:flet-dev/flet-app-templates",
            checkout=template_ref,
            directory=options.template,
            output_dir=str(out_dir.parent),
            no_input=True,
            overwrite_if_exists=True,
            extra_context=template_data,
        )

        print("[spring_green3]Done![/spring_green3]\n")

        if self.verbose > 0:
            print(f"[cyan]Files created at[/cyan] {out_dir}:\n")
            for root, dirs, files in os.walk(out_dir):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), out_dir)
                    print(rel_path)
            print("")

        # print next steps
        print("[cyan]Run the app:[/cyan]\n")
        app_dir = (
            os.path.relpath(out_dir, os.getcwd())
            if options.output_directory != "."
            else ""
        )
        print(f"flet run {app_dir}\n")
