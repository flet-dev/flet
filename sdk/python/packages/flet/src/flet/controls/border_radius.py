import dataclasses
from typing import Optional, Union

from flet.controls.types import Number
from flet.utils import deprecated

__all__ = [
    "BorderRadius",
    "BorderRadiusValue",
    "OptionalBorderRadiusValue",
    "all",
    "horizontal",
    "vertical",
    "only",
]


@dataclasses.dataclass
class BorderRadius:
    top_left: Number
    """
    Radius of the top left border corner.
    """
    
    top_right: Number
    """
    Radius of the top right border corner.
    """

    bottom_left: Number
    """
    Radius of the bottom left border corner.
    """
    
    bottom_right: Number
    """
    Radius of the bottom right border corner.
    """

    @classmethod
    def all(cls, value: Number) -> "BorderRadius":
        """
        Sets the same border radius of `value` for all 4 corners of the rectangle.
        """
        return BorderRadius(
            top_left=value, top_right=value, bottom_left=value, bottom_right=value
        )

    @classmethod
    def horizontal(cls, *, left: Number = 0, right: Number = 0) -> "BorderRadius":
        """
        Sets the border radius horizontally for the left and right corners of the 
        rectangle.

        Both `left` and `right` default to `0`.
        """
        return BorderRadius(
            top_left=left, top_right=right, bottom_left=left, bottom_right=right
        )

    @classmethod
    def vertical(cls, *, top: Number = 0, bottom: Number = 0) -> "BorderRadius":
        """
        Sets the border radius vertically for the top and bottom corners of the 
        rectangle.

        Both `top` and `bottom` default to `0`.
        """
        return BorderRadius(
            top_left=top, top_right=top, bottom_left=bottom, bottom_right=bottom
        )

    @classmethod
    def only(
        cls,
        *,
        top_left: Number = 0,
        top_right: Number = 0,
        bottom_left: Number = 0,
        bottom_right: Number = 0,
    ) -> "BorderRadius":
        """
        Sets different border radius for each corner of the rectangle.
        """
        return BorderRadius(
            top_left=top_left,
            top_right=top_right,
            bottom_left=bottom_left,
            bottom_right=bottom_right,
        )


@deprecated(
    reason="Use BorderRadius.all() instead",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def all(value: float) -> BorderRadius:
    return BorderRadius(
        top_left=value, top_right=value, bottom_left=value, bottom_right=value
    )


@deprecated(
    reason="Use BorderRadius.horizontal() instead",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def horizontal(left: float = 0, right: float = 0) -> BorderRadius:
    return BorderRadius(
        top_left=left, top_right=right, bottom_left=left, bottom_right=right
    )


@deprecated(
    reason="Use BorderRadius.vertical() instead",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def vertical(top: float = 0, bottom: float = 0) -> BorderRadius:
    return BorderRadius(
        top_left=top, top_right=top, bottom_left=bottom, bottom_right=bottom
    )


@deprecated(
    reason="Use BorderRadius.only() instead",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def only(
        top_left: float = 0,
        top_right: float = 0,
        bottom_left: float = 0,
        bottom_right: float = 0,
) -> BorderRadius:
    return BorderRadius(
        top_left=top_left,
        top_right=top_right,
        bottom_left=bottom_left,
        bottom_right=bottom_right,
    )


BorderRadiusValue = Union[Number, BorderRadius]
OptionalBorderRadiusValue = Optional[BorderRadiusValue]
