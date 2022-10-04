# this file will be replaced by CI

import subprocess as sp


def update_version():
    in_repo = sp.run(
        ["git", "status"],
        capture_output=True,
        text=True
    ).stdout.startswith("On branch ")

    if in_repo:
        # NOTE: this may break if there is a tag name starting with
        #         "v" that isn't a version number
        version = sp.run(
            ["git tag |grep '^v' |sort -V |tail -n 1 |sed 's/v//g'"],
            capture_output=True,
            shell=True,
            text=True
        ).stdout.strip()

    else:
        version = "0.1.60"  # default to old version
    return version


if not globals().get("version", None):
    version = update_version()
