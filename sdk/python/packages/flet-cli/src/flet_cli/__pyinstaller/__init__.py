import os


def get_hook_dirs():
    """
    Return directories containing PyInstaller hook modules for `flet-cli`.
    """

    return [os.path.dirname(__file__)]
