from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flet.core.types import ColorValue, OptionalNumber


class BorderSideStrokeAlign(float, Enum):
    INSIDE = -1.0
    CENTER = 0.0
    OUTSIDE = 1.0


@dataclass
class BorderSide:
    width: OptionalNumber
    color: Optional[ColorValue] = None
    stroke_align: Union[BorderSideStrokeAlign, OptionalNumber] = None


@dataclass
class Border:
    top: Optional[BorderSide] = None
    right: Optional[BorderSide] = None
    bottom: Optional[BorderSide] = None
    left: Optional[BorderSide] = None


def all(width: Optional[float] = None, color: Optional[ColorValue] = None) -> Border:
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
