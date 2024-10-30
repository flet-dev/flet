import subprocess
import sys

import flet.version


def install_flet_package(name: str):
    retcode = subprocess.call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "--disable-pip-version-check",
            f"{name}=={flet.version.version}",
        ]
    )
    if retcode != 0:
        print(
            f'Unable to upgrade "{name}" package to version {flet.version.version}. Please use "pip install \'flet[all]\' --upgrade" command to upgrade Flet.'
        )
        exit(1)
