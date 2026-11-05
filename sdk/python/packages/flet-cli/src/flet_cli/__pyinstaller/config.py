temp_bin_dir = None

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
