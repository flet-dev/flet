import subprocess
import sys

import flet.version


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
        install_flet_package("flet-desktop")


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
