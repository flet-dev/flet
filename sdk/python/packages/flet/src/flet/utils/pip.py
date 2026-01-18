import subprocess
import sys

import flet.version
from flet.utils import is_linux


def install_flet_package(name: str):
    print(f"Installing {name} {flet.version.flet_version} package...", end="")
    retcode = subprocess.call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "--disable-pip-version-check",
            f"{name}=={flet.version.flet_version}",
        ]
    )
    if retcode == 0:
        print("OK")
    else:
        print(
            f'Unable to upgrade "{name}" package to version '
            f"{flet.version.flet_version}. Please use "
            f"\"pip install 'flet[all]=={flet.version.flet_version}' --upgrade\" "
            f"command to upgrade Flet."
        )
        exit(1)


def ensure_flet_desktop_package_installed():
    try:
        import flet_desktop.version

        if (
            flet_desktop.version.version
            and flet_desktop.version.version != flet.version.flet_version
        ):
            raise RuntimeError("flet-desktop version mismatch")
    except Exception:
        package_name = "flet-desktop-light" if is_linux() else "flet-desktop"
        install_flet_package(package_name)


def ensure_flet_web_package_installed():
    try:
        import flet_web.version

        if (
            flet_web.version.version
            and flet_web.version.version != flet.version.flet_version
        ):
            raise RuntimeError("flet-web version mismatch")
    except Exception:
        install_flet_package("flet-web")


def ensure_flet_cli_package_installed():
    try:
        import flet_cli.version

        if (
            flet_cli.version.version
            and flet_cli.version.version != flet.version.flet_version
        ):
            raise RuntimeError("flet-cli version mismatch")
    except Exception:
        install_flet_package("flet-cli")
