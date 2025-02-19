import argparse
import os
import re
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path

from flet.core.types import WebRenderer
from flet.utils import copy_tree, is_within_directory, random_string

from flet_cli.commands.base import BaseCommand
from flet_cli.utils.project_dependencies import (
    get_poetry_dependencies,
    get_project_dependencies,
)
from flet_cli.utils.pyproject_toml import load_pyproject_toml


class Command(BaseCommand):
    """
    Publish Flet app as a standalone web app.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "script",
            type=str,
            nargs="?",
            help="path to a Python script",
            default=".",
        )
        parser.add_argument(
            "--pre",
            dest="pre",
            action="store_true",
            default=False,
            help="allow micropip to install pre-release Python packages",
        )
        parser.add_argument(
            "-a",
            "--assets",
            dest="assets_dir",
            type=str,
            default=None,
            help="path to an assets directory",
        )
        parser.add_argument(
            "--distpath",
            dest="distpath",
            help="where to put the published app (default: ./dist)",
        )
        parser.add_argument(
            "--app-name",
            dest="app_name",
            type=str,
            default=None,
            help="application name",
        )
        parser.add_argument(
            "--app-short-name",
            dest="app_short_name",
            type=str,
            default=None,
            help="application short name",
        )
        parser.add_argument(
            "--app-description",
            dest="app_description",
            type=str,
            default=None,
            help="application description",
        )
        parser.add_argument(
            "--base-url",
            dest="base_url",
            type=str,
            default=None,
            help="base URL for the app",
        )
        parser.add_argument(
            "--web-renderer",
            dest="web_renderer",
            choices=["canvaskit", "html"],
            default="canvaskit",
            help="web renderer to use",
        )
        parser.add_argument(
            "--use-color-emoji",
            dest="use_color_emoji",
            action="store_true",
            default=False,
            help="enables color emojis with CanvasKit renderer",
        )
        parser.add_argument(
            "--route-url-strategy",
            dest="route_url_strategy",
            choices=["path", "hash"],
            default="path",
            help="URL routing strategy",
        )
        parser.add_argument(
            "--pwa-background-color",
            dest="pwa_background_color",
            help="an initial background color for your web application",
            required=False,
        )
        parser.add_argument(
            "--pwa-theme-color",
            dest="pwa_theme_color",
            help="default color for your web application's user interface",
            required=False,
        )

    def handle(self, options: argparse.Namespace) -> None:
        import flet.version
        from flet.utils.pip import ensure_flet_web_package_installed

        ensure_flet_web_package_installed()
        from flet_web import get_package_web_dir, patch_index_html, patch_manifest_json

        # constants
        dist_name = "dist"
        assets_name = "assets"
        app_tar_gz_filename = "app.tar.gz"
        reqs_filename = "requirements.txt"

        # script path
        script_path = Path(options.script)
        if not script_path.is_absolute():
            script_path = Path(os.getcwd()).joinpath(script_path).resolve()

        if not script_path.exists():
            print(f"File or directory not found: {script_path}")
            sys.exit(1)

        if script_path.is_dir():
            script_path = script_path / "main.py"

        script_dir = script_path.parent

        project_dir = Path(script_dir)
        get_pyproject = load_pyproject_toml(project_dir)

        if get_pyproject("tool.flet.app.path"):
            script_dir = script_dir.joinpath(get_pyproject("tool.flet.app.path"))
            script_path = script_dir.joinpath(
                os.path.basename(script_path),
            )

        # delete "dist" directory
        if options.distpath:
            dist_dir = Path(options.distpath)
            if not dist_dir.is_absolute():
                dist_dir = project_dir.joinpath(dist_dir).resolve()
        else:
            dist_dir = project_dir.joinpath(dist_name)

        print(f"Cleaning up {dist_dir}...")
        if dist_dir.exists():
            shutil.rmtree(dist_dir, ignore_errors=True)
        dist_dir.mkdir(parents=True, exist_ok=True)

        # copy "web"
        web_path = get_package_web_dir()
        if not os.path.exists(web_path):
            print(f"Flet module does not contain 'web' directory: {web_path}")
            sys.exit(1)
        copy_tree(web_path, dist_dir)

        # copy assets
        assets_dir = options.assets_dir
        if assets_dir and not Path(assets_dir).is_absolute():
            assets_dir = str(script_path.joinpath(assets_dir).resolve())
        else:
            assets_dir = str(script_dir / assets_name)

        if os.path.exists(assets_dir):
            copy_tree(assets_dir, str(dist_dir))

        deps = []
        requirements_txt = project_dir.joinpath(reqs_filename)

        toml_dependencies = get_poetry_dependencies(
            get_pyproject("tool.poetry.dependencies")
        ) or get_project_dependencies(get_pyproject("project.dependencies"))

        if toml_dependencies:
            deps = toml_dependencies
            print(f"pyproject.toml dependencies: {deps}")
        elif requirements_txt.exists():
            with open(requirements_txt, "r", encoding="utf-8") as f:
                deps = list(
                    filter(
                        lambda dep: not dep.startswith("#"),
                        [line.rstrip() for line in f],
                    )
                )
                print(f"{reqs_filename} dependencies: {deps}")

        if len(deps) == 0:
            deps = [f"flet=={flet.version.version}"]

        temp_reqs_txt = Path(tempfile.gettempdir()).joinpath(random_string(10))
        with open(temp_reqs_txt, "w", encoding="utf-8") as f:
            f.writelines(dep + "\n" for dep in deps)

        # pack all files in script's directory to dist/app.tar.gz
        app_tar_gz_path = os.path.join(dist_dir, app_tar_gz_filename)

        def filter_tar(tarinfo: tarfile.TarInfo):
            full_path = os.path.join(script_dir, tarinfo.name)
            if (
                tarinfo.name.startswith(".")
                or tarinfo.name.startswith("__pycache__")
                or tarinfo.name == reqs_filename
            ):
                return None
            elif assets_dir and is_within_directory(assets_dir, full_path):
                return None
            elif is_within_directory(dist_dir, full_path):
                return None
            # tarinfo.uid = tarinfo.gid = 0
            # tarinfo.uname = tarinfo.gname = "root"
            if tarinfo.name != "":
                print("    Adding", tarinfo.name)
            return tarinfo

        print(f"Packaging application to {app_tar_gz_filename}")
        with tarfile.open(app_tar_gz_path, "w:gz", format=tarfile.GNU_FORMAT) as tar:
            tar.add(script_dir, arcname="/", filter=filter_tar)
            print("    Adding requirements.txt")
            tar.add(temp_reqs_txt, arcname=reqs_filename)

        os.remove(temp_reqs_txt)

        # patch ./dist/index.html
        # - <!-- pyodideCode -->
        # - <!-- flutterWebRenderer -->
        # - %FLET_ROUTE_URL_STRATEGY%
        # - %FLET_WEB_PYODIDE%

        base_url = (
            (options.base_url or get_pyproject("tool.flet.web.base_url") or "/")
            .strip("/")
            .strip()
        )

        app_short_name = (
            options.app_short_name
            or get_pyproject("project.name")
            or get_pyproject("tool.poetry.name")
            or project_dir.name
        )

        app_name = (
            options.app_name or get_pyproject("tool.flet.product") or app_short_name
        )

        app_description = (
            options.app_description
            or get_pyproject("project.description")
            or get_pyproject("tool.poetry.description")
        )

        pwa_background_color = options.pwa_background_color or get_pyproject(
            "tool.flet.web.pwa_background_color"
        )

        pwa_theme_color = options.pwa_theme_color or get_pyproject(
            "tool.flet.web.pwa_theme_color"
        )

        print("Patching index.html")
        patch_index_html(
            index_path=os.path.join(dist_dir, "index.html"),
            base_href=base_url,
            app_name=app_name,
            app_description=app_description,
            pyodide=True,
            pyodide_pre=options.pre,
            pyodide_script_path=str(script_path),
            web_renderer=WebRenderer(
                (
                    options.web_renderer
                    or get_pyproject("tool.flet.web.renderer")
                    or "canvaskit"
                )
            ),
            use_color_emoji=(
                True
                if (
                    options.use_color_emoji
                    or get_pyproject("tool.flet.web.use_color_emoji")
                )
                else False
            ),
            route_url_strategy=str(
                options.route_url_strategy
                or get_pyproject("tool.flet.web.route_url_strategy")
                or "path"
            ),
        )

        print("Patching manifest.json")
        patch_manifest_json(
            manifest_path=os.path.join(dist_dir, "manifest.json"),
            app_name=app_name,
            app_short_name=app_short_name,
            app_description=app_description,
            background_color=pwa_background_color,
            theme_color=pwa_theme_color,
        )
