from typing import Union

from flet.controls.base_control import value
from flet.controls.types import Number

__all__ = [
    "Padding",
    "PaddingValue",
]


@value
class Padding:
    """
    Defines padding for all sides of a rectangle.
    """

    left: Number = 0
    """
    The padding value for the left side of the rectangle.
    """

    top: Number = 0
    """
    The padding value for the top side of the rectangle.
    """

    right: Number = 0
    """
    The padding value for the right side of the rectangle.
    """

    bottom: Number = 0
    """
    The padding value for the bottom side of the rectangle.
    """

    @classmethod
    def all(cls, value: Number) -> "Padding":
        """
        Applies the same padding to all sides.
        """
        return Padding(left=value, top=value, right=value, bottom=value)

    @classmethod
    def symmetric(cls, *, vertical: Number = 0, horizontal: Number = 0) -> "Padding":
        """
        Applies `vertical` padding to top and bottom sides and `horizontal` padding to \
        left and right sides.
        """
        return Padding(left=horizontal, top=vertical, right=horizontal, bottom=vertical)

    @classmethod
    def only(
        cls, *, left: Number = 0, top: Number = 0, right: Number = 0, bottom: Number = 0
    ) -> "Padding":
        """
        Applies padding to the specified sides.
        """
        return Padding(left=left, top=top, right=right, bottom=bottom)

    @classmethod
    def zero(cls) -> "Padding":
        return Padding.only()


PaddingValue = Union[Number, Padding]
"""Type alias for padding values.

Represents padding as either:
- a single numeric value applied to all sides,
- or an explicit :class:`~flet.Padding` configuration.
"""
