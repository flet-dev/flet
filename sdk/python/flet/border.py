import dataclasses
from typing import Union


@dataclasses.dataclass
class BorderSide:
    width: Union[None, float, int]
    color: str = dataclasses.field(default=None)


@dataclasses.dataclass
class Border:
    top: BorderSide
    right: BorderSide
    bottom: BorderSide
    left: BorderSide


def all(width: float = None, color: str = None):
    bs = BorderSide(width, color)
    return Border(left=bs, top=bs, right=bs, bottom=bs)


def symmetric(vertical: BorderSide = None, horizontal: BorderSide = None):
    return Border(left=horizontal, top=vertical, right=horizontal, bottom=vertical)


def only(
    left: BorderSide = None,
    top: BorderSide = None,
    right: BorderSide = None,
    bottom: BorderSide = None,
):
    return Border(left=left, top=top, right=right, bottom=bottom)
