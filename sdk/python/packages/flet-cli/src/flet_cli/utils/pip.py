import subprocess
import sys

import flet_cli.version


def install_flet_package(name: str):
    subprocess.call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "--disable-pip-version-check",
            f"{name}=={flet_cli.version.version}",
        ]
    )
