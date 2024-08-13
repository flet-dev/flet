from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union

from flet_core.types import OptionalNumber


class BorderSideStrokeAlign(Enum):
    INSIDE = -1.0
    CENTER = 0.0
    OUTSIDE = 1.0


@dataclass
class BorderSide:
    width: OptionalNumber
    color: Optional[str] = field(default=None)
    stroke_align: Union[BorderSideStrokeAlign, OptionalNumber] = field(default=None)


@dataclass
class Border:
    top: Optional[BorderSide] = field(default=None)
    right: Optional[BorderSide] = field(default=None)
    bottom: Optional[BorderSide] = field(default=None)
    left: Optional[BorderSide] = field(default=None)


def all(width: Optional[float] = None, color: Optional[str] = None) -> Border:
    bs = BorderSide(width, color)
    return Border(left=bs, top=bs, right=bs, bottom=bs)


def symmetric(
    vertical: Optional[BorderSide] = None, horizontal: Optional[BorderSide] = None
) -> Border:
    return Border(left=horizontal, top=vertical, right=horizontal, bottom=vertical)


def only(
    left: Optional[BorderSide] = None,
    top: Optional[BorderSide] = None,
    right: Optional[BorderSide] = None,
    bottom: Optional[BorderSide] = None,
) -> Border:
    return Border(left=left, top=top, right=right, bottom=bottom)
