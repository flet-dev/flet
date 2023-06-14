from pathlib import Path

from flet_core.utils import Vector, slugify


def get_package_root_dir():
    return str(Path(__file__).parent.parent)
