# this file will be replaced by CI

import subprocess as sp
from pkg_resources import parse_version

from flet.utils import which


def update_version():
    in_repo = which("git") and sp.run(
        ["git", "status"],
        capture_output=True,
        text=True,
    ).stdout.startswith("On branch ")

    if in_repo:
        # NOTE: this may break if there is a tag name starting with
        #         "v" that isn't a version number
        tags = sp.run(
            ["git", "tag"],
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        versions = filter(lambda t: t.startswith("v"), tags)
        version = sorted(versions, key=parse_version)[-1][1:]

    else:
        version = "0.1.60"  # default to old version
    return version


if not globals().get("version", None):
    version = update_version()
