from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flet.controls.colors import Colors
from flet.controls.types import ColorValue, Number, OptionalColorValue, OptionalNumber
from flet.utils import deprecated

__all__ = [
    "Border",
    "BorderSide",
    "BorderSideStrokeAlign",
    "OptionalBorder",
    "OptionalBorderSide",
    "OptionalBorderSideStrokeAlign",
    "BorderSideStrokeAlignValue",
    "OptionalBorderSideStrokeAlignValue",
    "all",
    "symmetric",
    "only",
]


class BorderSideStrokeAlign(float, Enum):
    INSIDE = -1.0
    CENTER = 0.0
    OUTSIDE = 1.0


@dataclass
class BorderSide:
    width: Number = 1.0
    color: ColorValue = Colors.BLACK
    stroke_align: "BorderSideStrokeAlignValue" = BorderSideStrokeAlign.INSIDE


@dataclass
class Border:
    top: "OptionalBorderSide" = None
    right: "OptionalBorderSide" = None
    bottom: "OptionalBorderSide" = None
    left: "OptionalBorderSide" = None

    @classmethod
    def all(
        cls, width: OptionalNumber = None, color: OptionalColorValue = None
    ) -> "Border":
        bs = BorderSide(width, color)
        return Border(left=bs, top=bs, right=bs, bottom=bs)

    @classmethod
    def symmetric(
        cls,
        *,
        vertical: "OptionalBorderSide" = None,
        horizontal: "OptionalBorderSide" = None,
    ) -> "Border":
        return Border(left=horizontal, top=vertical, right=horizontal, bottom=vertical)

    @classmethod
    def only(
        cls,
        *,
        left: "OptionalBorderSide" = None,
        top: "OptionalBorderSide" = None,
        right: "OptionalBorderSide" = None,
        bottom: "OptionalBorderSide" = None,
    ) -> "Border":
        return Border(left=left, top=top, right=right, bottom=bottom)


@deprecated(
    reason="Use Border.all() instead.",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def all(width: Optional[float] = None, color: Optional[ColorValue] = None) -> Border:
    bs = BorderSide(width, color)
    return Border(left=bs, top=bs, right=bs, bottom=bs)


@deprecated(
    reason="Use Border.symmetric() instead.",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def symmetric(
    vertical: Optional[BorderSide] = None, horizontal: Optional[BorderSide] = None
) -> Border:
    return Border(left=horizontal, top=vertical, right=horizontal, bottom=vertical)


@deprecated(
    reason="Use Border.only() instead.",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def only(
    left: Optional[BorderSide] = None,
    top: Optional[BorderSide] = None,
    right: Optional[BorderSide] = None,
    bottom: Optional[BorderSide] = None,
) -> Border:
    return Border(left=left, top=top, right=right, bottom=bottom)


# Typings
OptionalBorder = Optional[Border]
OptionalBorderSide = Optional[BorderSide]
OptionalBorderSideStrokeAlign = Optional[BorderSideStrokeAlign]
BorderSideStrokeAlignValue = Union[BorderSideStrokeAlign, Number]
OptionalBorderSideStrokeAlignValue = Optional[BorderSideStrokeAlignValue]
