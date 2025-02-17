import asyncio
import logging
import os
import signal
import stat
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import flet_desktop
import flet_desktop.version
from flet.utils import (
    get_arch,
    is_linux,
    is_macos,
    is_windows,
    random_string,
    safe_tar_extractall,
)

logger = logging.getLogger(flet_desktop.__name__)


def get_package_bin_dir():
    return str(Path(__file__).parent.joinpath("app"))


def open_flet_view(page_url, assets_dir, hidden):
    args, flet_env, pid_file = __locate_and_unpack_flet_view(
        page_url, assets_dir, hidden
    )
    return subprocess.Popen(args, env=flet_env), pid_file


async def open_flet_view_async(page_url, assets_dir, hidden):
    args, flet_env, pid_file = __locate_and_unpack_flet_view(
        page_url, assets_dir, hidden
    )
    return (
        await asyncio.create_subprocess_exec(args[0], *args[1:], env=flet_env),
        pid_file,
    )


def close_flet_view(pid_file):
    if pid_file is not None and os.path.exists(pid_file):
        try:
            with open(pid_file, encoding="utf-8") as f:
                fvp_pid = int(f.read())
            logger.debug(f"Flet View process {fvp_pid}")
            os.kill(fvp_pid, signal.SIGKILL)
        except Exception:
            pass
        finally:
            os.remove(pid_file)


def __locate_and_unpack_flet_view(page_url, assets_dir, hidden):
    logger.info("Starting Flet View app...")

    args = []

    # pid file - Flet client writes its process ID to this file
    pid_file = str(Path(tempfile.gettempdir()).joinpath(random_string(20)))

    if is_windows():
        flet_path = None
        # try loading Flet client built with the latest run of `flet build`
        build_windows = os.path.join(os.getcwd(), "build", "windows")
        if os.path.exists(build_windows):
            for f in os.listdir(build_windows):
                if f.endswith(".exe"):
                    flet_path = os.path.join(build_windows, f)

        if not flet_path:
            flet_exe = "flet.exe"
            temp_flet_dir = Path.home().joinpath(
                ".flet", "bin", f"flet-{flet_desktop.version.version}"
            )

            # check if flet_view.exe exists in "bin" directory (user mode)
            flet_path = os.path.join(get_package_bin_dir(), "flet", flet_exe)
            logger.info(f"Looking for Flet executable at: {flet_path}")
            if os.path.exists(flet_path):
                logger.info(f"Flet View found in: {flet_path}")
            else:
                # check if flet.exe is in FLET_VIEW_PATH (flet developer mode)
                flet_path = os.environ.get("FLET_VIEW_PATH")
                if flet_path and os.path.exists(flet_path):
                    logger.info(f"Flet View found in PATH: {flet_path}")
                    flet_path = os.path.join(flet_path, flet_exe)
                else:
                    if not temp_flet_dir.exists():
                        zip_file = __download_flet_client("flet-windows.zip")

                        logger.info(
                            f"Extracting flet.exe from archive to {temp_flet_dir}"
                        )
                        temp_flet_dir.mkdir(parents=True, exist_ok=True)
                        with zipfile.ZipFile(zip_file, "r") as zip_arch:
                            zip_arch.extractall(str(temp_flet_dir))
                    flet_path = str(temp_flet_dir.joinpath("flet", flet_exe))
        args = [flet_path, page_url, pid_file]
    elif is_macos():
        app_path = None
        # try loading Flet client built with the latest run of `flet build`
        build_macos = os.path.join(os.getcwd(), "build", "macos")
        if os.path.exists(build_macos):
            for f in os.listdir(build_macos):
                if f.endswith(".app"):
                    app_path = os.path.join(build_macos, f)

        if not app_path:
            # build version-specific path to Flet.app
            temp_flet_dir = Path.home().joinpath(
                ".flet", "bin", f"flet-{flet_desktop.version.version}"
            )

            # check if flet.exe is in FLET_VIEW_PATH (flet developer mode)
            flet_path = os.environ.get("FLET_VIEW_PATH")
            if flet_path:
                logger.info(f"Flet.app is set via FLET_VIEW_PATH: {flet_path}")
                temp_flet_dir = Path(flet_path)
            else:
                # check if flet_view.app exists in a temp directory
                if not temp_flet_dir.exists():
                    # check if flet.tar.gz exists
                    gz_filename = "flet-macos.tar.gz"
                    tar_file = os.path.join(get_package_bin_dir(), gz_filename)
                    logger.info(f"Looking for Flet.app archive at: {tar_file}")
                    if not os.path.exists(tar_file):
                        tar_file = __download_flet_client(gz_filename)

                    logger.info(f"Extracting Flet.app from archive to {temp_flet_dir}")
                    temp_flet_dir.mkdir(parents=True, exist_ok=True)
                    with tarfile.open(str(tar_file), "r:gz") as tar_arch:
                        safe_tar_extractall(tar_arch, str(temp_flet_dir))
                else:
                    logger.info(f"Flet View found in: {temp_flet_dir}")

            app_name = None
            for f in os.listdir(temp_flet_dir):
                if f.endswith(".app"):
                    app_name = f
            assert (
                app_name is not None
            ), f"Application bundle not found in {temp_flet_dir}"
            app_path = temp_flet_dir.joinpath(app_name)
        args = ["open", str(app_path), "-n", "-W", "--args", page_url, pid_file]
    elif is_linux():
        app_path = None
        # try loading Flet client built with the latest run of `flet build`
        build_linux = os.path.join(os.getcwd(), "build", "linux")
        if os.path.exists(build_linux):
            for f in os.listdir(build_linux):
                ef = os.path.join(build_linux, f)
                if os.path.isfile(ef) and stat.S_IXUSR & os.stat(ef)[stat.ST_MODE]:
                    app_path = ef

        if not app_path:
            # build version-specific path to flet folder
            temp_flet_dir = Path.home().joinpath(
                ".flet", "bin", f"flet-{flet_desktop.version.version}"
            )

            # check if flet.exe is in FLET_VIEW_PATH (flet developer mode)
            flet_path = os.environ.get("FLET_VIEW_PATH")
            if flet_path:
                logger.info(f"Flet View is set via FLET_VIEW_PATH: {flet_path}")
                temp_flet_dir = Path(flet_path)
                app_path = temp_flet_dir.joinpath("flet")
            else:
                # check if flet_view.app exists in a temp directory
                if not temp_flet_dir.exists():
                    # check if flet.tar.gz exists
                    gz_filename = f"flet-linux-{get_arch()}.tar.gz"
                    tar_file = os.path.join(get_package_bin_dir(), gz_filename)
                    logger.info(f"Looking for Flet bundle archive at: {tar_file}")
                    if not os.path.exists(tar_file):
                        tar_file = __download_flet_client(gz_filename)

                    logger.info(f"Extracting Flet from archive to {temp_flet_dir}")
                    temp_flet_dir.mkdir(parents=True, exist_ok=True)
                    with tarfile.open(str(tar_file), "r:gz") as tar_arch:
                        safe_tar_extractall(tar_arch, str(temp_flet_dir))
                else:
                    logger.info(f"Flet View found in: {temp_flet_dir}")

                app_path = temp_flet_dir.joinpath("flet", "flet")
        args = [str(app_path), page_url, pid_file]

    flet_env = {**os.environ}

    if assets_dir:
        args.append(assets_dir)

    if hidden:
        flet_env["FLET_HIDE_WINDOW_ON_START"] = "true"

    return args, flet_env, pid_file


def __download_flet_client(file_name):
    ver = flet_desktop.version.version
    if not ver:
        import flet.version
        from flet.version import update_version

        ver = flet.version.version or update_version()
    temp_arch = Path(tempfile.gettempdir()).joinpath(file_name)
    flet_url = f"https://github.com/flet-dev/flet/releases/download/v{ver}/{file_name}"
    logger.info(f"Downloading Flet v{ver} from {flet_url} to {temp_arch}")
    urllib.request.urlretrieve(flet_url, temp_arch)
    return str(temp_arch)
