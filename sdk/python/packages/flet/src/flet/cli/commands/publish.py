import argparse
import logging
import os
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path

import flet.__pyinstaller.config as hook_config
import flet.version
from flet.cli.commands.base import BaseCommand
from flet.utils import is_macos, is_windows, is_within_directory, safe_tar_extractall
from flet_core.utils import random_string


class Command(BaseCommand):
    """
    Publish Flet app as a standalone web app
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("script", type=str, help="path to a Python script")
        parser.add_argument(
            "-a",
            "--assets",
            dest="assets_dir",
            type=str,
            default=None,
            help="path to an assets directory",
        )
        parser.add_argument(
            "--web-renderer",
            dest="web_renderer",
            choices=["canvaskit", "html"],
            default="canvaskit",
            help="web renderer to use",
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
        flet_web_filename = "flet-web.tar.gz"
        app_tar_gz_filename = "app.tar.gz"
        reqs_filename = "requirements.txt"

        # script path
        script_path = options.script
        if not os.path.isabs(options.script):
            script_path = str(Path(os.getcwd()).joinpath(options.script).resolve())

        if not Path(script_path).exists():
            print(f"File not found: {script_path}")
            exit(1)

        script_dir = os.path.dirname(script_path)

        # delete "dist" directory
        dist_dir = os.path.join(script_dir, dist_name)
        print(f"Cleaning up {dist_dir}...")
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir, ignore_errors=True)
        Path(dist_dir).mkdir(parents=True, exist_ok=True)

        # download flet-web.tar.gz
        print(f"Downloading Flet Web to {dist_dir}")
        temp_arch = self.__download_flet_web(flet_web_filename)

        # unpack to dist
        with tarfile.open(temp_arch, "r:gz") as tar_arch:
            safe_tar_extractall(tar_arch, dist_dir)

        # copy assets
        assets_dir = options.assets_dir
        if assets_dir and not Path(assets_dir).is_absolute():
            assets_dir = str(
                Path(os.path.dirname(script_path)).joinpath(assets_dir).resolve()
            )
        if assets_dir:
            shutil.copytree(assets_dir, dist_dir, dirs_exist_ok=True)

        # create "./dist/requirements.txt" if not exist
        # add flet-pyodide=={version} to dist/requirements.txt
        reqs_path = os.path.join(script_dir, reqs_filename)

        # add required dependencies
        deps = []
        if os.path.exists(reqs_path):
            with open(reqs_path, "r") as f:
                deps = [line.rstrip() for line in f]

        pyodide_dep_found = False
        for dep in deps:
            if dep.startswith("flet-pyodide"):
                pyodide_dep_found = True
                break
        if not pyodide_dep_found:
            deps.append(f"flet-pyodide>={flet.version.version}")
            with open(reqs_path, "w") as f:
                f.writelines(deps)

        # pack all files in script's directory to dist/app.tar.gz
        app_tar_gz_path = os.path.join(dist_dir, app_tar_gz_filename)

        def filter_tar(tarinfo: tarfile.TarInfo):
            full_path = os.path.join(script_dir, tarinfo.name)
            if tarinfo.name.startswith("."):
                return None
            elif assets_dir and is_within_directory(assets_dir, full_path):
                return None
            elif is_within_directory(dist_dir, full_path):
                return None
            # tarinfo.uid = tarinfo.gid = 0
            # tarinfo.uname = tarinfo.gname = "root"
            print("Adding", tarinfo.name)
            return tarinfo

        print(f"Packaging application to {app_tar_gz_filename}")
        with tarfile.open(app_tar_gz_path, "w:gz") as tar:
            tar.add(script_dir, arcname="/", filter=filter_tar)

        # patch ./dist/index.html
        # - <!-- pyodideCode -->
        # - <!-- flutterWebRenderer -->
        # - %FLET_ROUTE_URL_STRATEGY%
        # - %FLET_WEB_PYODIDE%

        print(flet.version.version)

    def __download_flet_web(self, file_name):
        ver = flet.version.version
        temp_arch = str(Path(tempfile.gettempdir()).joinpath(f"{ver}-{file_name}"))
        logging.info(f"Downloading Flet Web v{ver} to {temp_arch}")
        flet_url = (
            # f"https://github.com/flet-dev/flet/releases/download/v{ver}/{file_name}"
            "https://ci.appveyor.com/api/buildjobs/5k01xli75kelopba/artifacts/flet-web.tar.gz"
        )
        urllib.request.urlretrieve(flet_url, temp_arch)
        return temp_arch
