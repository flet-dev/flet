from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flet.controls.colors import Colors
from flet.controls.types import ColorValue, Number, OptionalColorValue, OptionalNumber

__all__ = [
    "Border",
    "BorderSide",
    "BorderSideStrokeAlign",
    "OptionalBorder",
    "OptionalBorderSide",
    "OptionalBorderSideStrokeAlign",
    "BorderSideStrokeAlignValue",
    "OptionalBorderSideStrokeAlignValue",
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
        vertical: "OptionalBorderSide" = None,
        horizontal: "OptionalBorderSide" = None,
    ) -> "Border":
        return Border(left=horizontal, top=vertical, right=horizontal, bottom=vertical)

    @classmethod
    def only(
        cls,
        left: "OptionalBorderSide" = None,
        top: "OptionalBorderSide" = None,
        right: "OptionalBorderSide" = None,
        bottom: "OptionalBorderSide" = None,
    ) -> "Border":
        return Border(left=left, top=top, right=right, bottom=bottom)


# Typings
OptionalBorder = Optional[Border]
OptionalBorderSide = Optional[BorderSide]
OptionalBorderSideStrokeAlign = Optional[BorderSideStrokeAlign]
BorderSideStrokeAlignValue = Union[BorderSideStrokeAlign, Number]
OptionalBorderSideStrokeAlignValue = Optional[BorderSideStrokeAlignValue]
