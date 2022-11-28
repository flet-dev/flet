"""Provide the current Flet version."""


import os
import subprocess as sp
from pathlib import Path

import flet
from flet.utils import which


# this value will be replaced by CI
version = ""


def update_version():
    """Return the current version or default."""
    working = Path().absolute()
    os.chdir(Path(flet.__file__).absolute().parent)
    in_repo = which("git") and sp.run(
        ["git", "status"],
        capture_output=True,
        text=True,
    ).stdout.startswith("On branch ")

    if in_repo:
        # NOTE: this may break if there is a tag name starting with
        #         "v" that isn't a version number
        class RepositoryError(OSError):
            pass

        git_p = sp.run(
            ["git", "describe", "--abbrev=0"],
            capture_output=True,
            text=True,
        )
        err = git_p.stderr.strip()

        if "cannot describe anything" in err:
            msg = "You may be using a repo cloned from a fork. "
            msg += "If so please clone the original Flet repo"
            raise RepositoryError(msg)

        if err:
            msg = "Unknown error while fetching the version: {err}"
            raise RepositoryError(msg)
        version = git_p.stdout.strip()[1:]

    else:
        version = "0.1.60"
    os.chdir(working)
    return version


if not version:
    version = update_version()
