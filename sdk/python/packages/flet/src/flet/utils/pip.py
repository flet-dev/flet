import os
import subprocess
import sys
from importlib.util import find_spec

import flet.version
from flet.utils import is_linux


def _install_with_pip(package_spec: str) -> int:
    """
    Installs a package using `pip`.

    Args:
        package_spec: Package requirement specifier to install (for example,
            `flet-web==0.27.0`).

    Returns:
        The `pip` process return code. Returns `1` when `pip` cannot be imported.
    """
    if find_spec("pip") is None:
        return 1
    return subprocess.call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "--disable-pip-version-check",
            package_spec,
        ]
    )


def _install_with_uv(package_spec: str) -> int:
    """
    Installs a package using `uv pip install`.

    Args:
        package_spec: Package requirement specifier to install (for example,
            `flet-web==0.27.0`).

    Returns:
        The `uv` process return code. Returns `1` when `uv` is not installed.
    """
    try:
        return subprocess.call(["uv", "pip", "install", package_spec])
    except FileNotFoundError:
        return 1


def install_flet_package(name: str):
    """
    Installs a Flet package pinned to the current Flet SDK version.

    Installation strategy:
    - If `UV` environment variable is set, try `uv` first and then fall back to `pip`.
    - Otherwise, try `pip` first and then fall back to `uv`.

    Args:
        name: Package name to install.

    Raises:
        SystemExit: If package installation fails with both installers.
    """
    package_spec = f"{name}=={flet.version.flet_version}"
    print(f"Installing {name} {flet.version.flet_version} package...", end="")
    if os.environ.get("UV"):
        retcode = _install_with_uv(package_spec)
        if retcode != 0:
            retcode = _install_with_pip(package_spec)
    else:
        retcode = _install_with_pip(package_spec)
        if retcode != 0:
            retcode = _install_with_uv(package_spec)
    if retcode == 0:
        print("OK")
    else:
        print(
            f'Unable to install "{name}" package. Please run '
            f'"pip install {package_spec} --upgrade" '
            f'or "uv pip install {package_spec} --upgrade" '
            f"command."
        )
        exit(1)


def ensure_flet_desktop_package_installed():
    """
    Ensures a compatible desktop runtime package is installed.

    If `flet-desktop` (or `flet-desktop-light` on Linux) is missing or its version
    differs from the current Flet SDK version, this function installs the expected
    package via [`install_flet_package()`][(m).install_flet_package].
    """
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
    """
    Ensures a compatible `flet-web` package is installed.

    If `flet-web` is missing or its version differs from the current Flet SDK
    version, this function installs it via
    [`install_flet_package()`][(m).install_flet_package].
    """
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
    """
    Ensures a compatible `flet-cli` package is installed.

    If `flet-cli` is missing or its version differs from the current Flet SDK
    version, this function installs it via
    [`install_flet_package()`][(m).install_flet_package].
    """
    try:
        import flet_cli.version

        if (
            flet_cli.version.version
            and flet_cli.version.version != flet.version.flet_version
        ):
            raise RuntimeError("flet-cli version mismatch")
    except Exception:
        install_flet_package("flet-cli")
