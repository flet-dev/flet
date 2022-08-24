import dataclasses
from typing import Optional, Union


@dataclasses.dataclass
class BorderSide:
    width: Union[None, float, int]
    color: Optional[str] = dataclasses.field(default=None)


@dataclasses.dataclass
class Border:
    top: Optional[BorderSide]
    right: Optional[BorderSide]
    bottom: Optional[BorderSide]
    left: Optional[BorderSide]


def all(width: Optional[float] = None, color: Optional[str] = None):
    bs = BorderSide(width, color)
    return Border(left=bs, top=bs, right=bs, bottom=bs)


def symmetric(
    vertical: Optional[BorderSide] = None, horizontal: Optional[BorderSide] = None
):
    return Border(left=horizontal, top=vertical, right=horizontal, bottom=vertical)


def only(
    left: Optional[BorderSide] = None,
    top: Optional[BorderSide] = None,
    right: Optional[BorderSide] = None,
    bottom: Optional[BorderSide] = None,
):
    return Border(left=left, top=top, right=right, bottom=bottom)
