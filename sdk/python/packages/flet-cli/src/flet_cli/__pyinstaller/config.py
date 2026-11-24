client_files = None
"""
Files of the client archive `flet pack` bundles, set before it runs
PyInstaller. `None` in a plain `pyinstaller` run, where the hook archives the
client itself.
"""

verbose = 0
"""
Number of `-v` flags `flet pack` runs with.
"""


def log_progress(*args) -> None:
    """
    Print a progress message of `flet pack`, shown with `-v` only.
    """

    if verbose > 0:
        print(*args)
