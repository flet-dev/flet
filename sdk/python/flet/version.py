import subprocess as sp

from pkg_resources import parse_version

from flet.utils import which

# this value will be replaced by CI
version = ""


def update_version():
    in_repo = sp.run(
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
        return sorted(versions, key=parse_version)[-1][1:]
    return "0.1.60"


if not globals().get("version", None):
    version = update_version()
