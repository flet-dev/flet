import argparse
from pathlib import Path

from colorama import Fore, Style
from flet.cli.commands.base import BaseCommand
from flet_core.utils import slugify


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
        from copier.main import Worker

        template_data = {"template_name": options.template}

        out_dir = Path(options.output_directory)
        project_name = options.project_name
        if project_name is None:
            project_slug = slugify(out_dir.name)
            if project_slug is not None and project_slug != "":
                project_name = project_slug

        if project_name is not None:
            template_data["project_name"] = project_name

        if options.description is not None:
            template_data["description"] = options.description

        # print("Template data:", template_data)
        with Worker(
            src_path="https://github.com/flet-dev/templates.git",
            dst_path=out_dir,
            vcs_ref="HEAD",
            data=template_data,
            defaults=True,
        ) as worker:
            worker.run_copy()
            print(Fore.LIGHTGREEN_EX + "Done. Now run:")
            print(Style.RESET_ALL)
            if options.output_directory != ".":
                print(Fore.CYAN + "cd", end=" ")
                print(Fore.WHITE + project_name, end="\n")
            print(Fore.CYAN + "flet run")
            print(Style.RESET_ALL)
