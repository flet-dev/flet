import argparse
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
from distutils.dir_util import copy_tree
from pathlib import Path

from flet.cli.commands.base import BaseCommand
from flet.utils import get_package_web_dir, is_within_directory
from flet_core.utils import random_string


class Command(BaseCommand):
    """
    Publish Flet app as a standalone web app
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("script", type=str, help="path to a Python script")
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

    def handle(self, options: argparse.Namespace) -> None:
        # constants
        dist_name = "dist"
        app_tar_gz_filename = "app.tar.gz"
        reqs_filename = "requirements.txt"

        # script path
        script_path = options.script
        if not os.path.isabs(script_path):
            script_path = str(Path(os.getcwd()).joinpath(script_path).resolve())

        if not Path(script_path).exists():
            print(f"File not found: {script_path}")
            sys.exit(1)

        script_dir = os.path.dirname(script_path)

        # delete "dist" directory
        dist_dir = options.distpath
        if dist_dir:
            if not os.path.isabs(dist_dir):
                dist_dir = str(Path(os.getcwd()).joinpath(dist_dir).resolve())
        else:
            dist_dir = os.path.join(script_dir, dist_name)

        print(f"Cleaning up {dist_dir}...")
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir, ignore_errors=True)
        Path(dist_dir).mkdir(parents=True, exist_ok=True)

        # copy "web"
        web_path = get_package_web_dir()
        if not os.path.exists(web_path):
            print("Flet module does not contain 'web' directory.")
            sys.exit(1)
        copy_tree(web_path, dist_dir)

        # copy assets
        assets_dir = options.assets_dir
        if assets_dir and not Path(assets_dir).is_absolute():
            assets_dir = str(
                Path(os.path.dirname(script_path)).joinpath(assets_dir).resolve()
            )
        if assets_dir:
            if not os.path.exists(assets_dir):
                print("Assets dir not found:", assets_dir)
                sys.exit(1)
            copy_tree(assets_dir, dist_dir)

        # create "./dist/requirements.txt" if not exist
        # add flet-pyodide=={version} to dist/requirements.txt
        reqs_path = os.path.join(script_dir, reqs_filename)

        # add required dependencies
        deps = []
        if os.path.exists(reqs_path):
            with open(reqs_path, "r") as f:
                deps = [line.rstrip() for line in f]

        deps = list(
            filter(lambda dep: not re.search("(^flet$)|(^flet[^a-z0-9-]+)", dep), deps)
        )

        pyodide_dep_found = False
        for dep in deps:
            if re.search("(^flet-pyodide$)|(^flet-pyodide[^a-z0-9-]+)", dep):
                pyodide_dep_found = True
                break
        if not pyodide_dep_found:
            deps.append("flet-pyodide")

        temp_reqs_txt = Path(tempfile.gettempdir()).joinpath(random_string(10))
        with open(temp_reqs_txt, "w") as f:
            f.writelines(dep + "\n" for dep in deps)

        # pack all files in script's directory to dist/app.tar.gz
        app_tar_gz_path = os.path.join(dist_dir, app_tar_gz_filename)

        def filter_tar(tarinfo: tarfile.TarInfo):
            full_path = os.path.join(script_dir, tarinfo.name)
            if (
                tarinfo.name.startswith(".")
                or tarinfo.name.startswith("__pycache__")
                or tarinfo.name == "requirements.txt"
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
            tar.add(temp_reqs_txt, arcname="requirements.txt")

        os.remove(temp_reqs_txt)

        # patch ./dist/index.html
        # - <!-- pyodideCode -->
        # - <!-- flutterWebRenderer -->
        # - %FLET_ROUTE_URL_STRATEGY%
        # - %FLET_WEB_PYODIDE%

        print("Patching index.html")
        index_path = os.path.join(dist_dir, "index.html")
        with open(index_path, "r") as f:
            index = f.read()

        pre = "true" if options.pre else "false"
        module_name = Path(script_path).stem
        pyodideCode = f"""
        <script>
            var micropipIncludePre = {pre};
            var pythonModuleName = "{module_name}";
        </script>
        <script src="python.js"></script>
        """
        index = index.replace("%FLET_WEB_PYODIDE%", "true")
        index = index.replace("<!-- pyodideCode -->", pyodideCode)
        index = index.replace(
            "<!-- webRenderer -->",
            f'<script>webRenderer="{options.web_renderer}";</script>',
        )
        index = index.replace(
            "<!-- useColorEmoji -->",
            f"<script>useColorEmoji={str(options.use_color_emoji).lower()};</script>",
        )
        index = index.replace("%FLET_ROUTE_URL_STRATEGY%", options.route_url_strategy)

        if options.base_url:
            base_url = options.base_url.strip("/").strip()
            index = index.replace(
                '<base href="/">',
                '<base href="{}">'.format(
                    "/" if base_url == "" else "/{}/".format(base_url)
                ),
            )
        if options.app_name:
            index = re.sub(
                r"\<meta name=\"apple-mobile-web-app-title\" content=\"(.+)\">",
                r'<meta name="apple-mobile-web-app-title" content="{}">'.format(
                    options.app_name
                ),
                index,
            )
        if options.app_description:
            index = re.sub(
                r"\<meta name=\"description\" content=\"(.+)\">",
                r'<meta name="description" content="{}">'.format(
                    options.app_description
                ),
                index,
            )

        with open(index_path, "w") as f:
            f.write(index)

        # patch manifest.json
        print("Patching manifest.json")
        manifest_path = os.path.join(dist_dir, "manifest.json")
        with open(manifest_path, "r") as f:
            manifest = json.loads(f.read())

        if options.app_name:
            manifest["name"] = options.app_name
            manifest["short_name"] = options.app_name

        if options.app_short_name:
            manifest["short_name"] = options.app_short_name

        if options.app_description:
            manifest["description"] = options.app_description

        with open(manifest_path, "w") as f:
            f.write(json.dumps(manifest, indent=2))
