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
    """
    A border comprised of four sides: top, right, bottom, left.

    Each side of the border is described by an instance of [`BorderSide`](https://flet.dev/docs/reference/types/borderside) 
    class.

    Usage example:
    ```python
    container_1.border = ft.Border.all(10, ft.Colors.PINK_600)
    container_1.border = ft.Border.only(bottom=ft.BorderSide(1, "black"))
    ```
    """

    top: "OptionalBorderSide" = None
    """
    Top side of the border.
    """
    
    right: "OptionalBorderSide" = None
    """
    Right side of the border.
    """

    bottom: "OptionalBorderSide" = None
    """
    Bottom side of the border.
    """
    
    left: "OptionalBorderSide" = None
    """
    Left side of the border.
    """

    @classmethod
    def all(
        cls, width: OptionalNumber = None, color: OptionalColorValue = None
    ) -> "Border":
        """
        Sets the same border for all 4 sides of the rectangle.
        """
        bs = BorderSide(width or 1.0, color or Colors.BLACK)
        return Border(left=bs, top=bs, right=bs, bottom=bs)

    @classmethod
    def symmetric(
        cls,
        *,
        vertical: "OptionalBorderSide" = None,
        horizontal: "OptionalBorderSide" = None,
    ) -> "Border":
        """
        Sets `vertical` border for top and bottom sides and `horizontal` for the left 
        and right sides of the rectangle.
        """
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
        """
        Sets different borders for each side of the rectangle.
        """
        return Border(left=left, top=top, right=right, bottom=bottom)


@deprecated(
    reason="Use Border.all() instead.",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def all(width: Optional[float] = None, color: Optional[ColorValue] = None) -> Border:
    bs = BorderSide(width or 1.0, color or Colors.BLACK)
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
"""
OptionalBorder type description
"""
OptionalBorderSide = Optional[BorderSide]
OptionalBorderSideStrokeAlign = Optional[BorderSideStrokeAlign]
BorderSideStrokeAlignValue = Union[BorderSideStrokeAlign, Number]
OptionalBorderSideStrokeAlignValue = Optional[BorderSideStrokeAlignValue]
