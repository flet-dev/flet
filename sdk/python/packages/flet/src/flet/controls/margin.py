from typing import Union

from flet.controls.base_control import value
from flet.controls.types import Number

__all__ = ["Margin", "MarginValue"]


@value
class Margin:
    """
    `Margin` class has the properties to set margins for all sides of the rectangle.
    """

    left: Number = 0
    """
    The margin applied to the left.
    """

    top: Number = 0
    """
    The margin applied to the top.
    """

    right: Number = 0
    """
    The margin applied to the right.
    """

    bottom: Number = 0
    """
    The margin applied to the bottom.
    """

    @classmethod
    def all(cls, value: Number) -> "Margin":
        """
        Applies the same margin to all sides.
        """
        return Margin(left=value, top=value, right=value, bottom=value)

    @classmethod
    def symmetric(cls, *, vertical: Number = 0, horizontal: Number = 0) -> "Margin":
        """
        Applies `vertical` margin to top and bottom sides and `horizontal` margin to \
        left and right sides.
        """
        return Margin(left=horizontal, top=vertical, right=horizontal, bottom=vertical)

    @classmethod
    def only(
        cls, *, left: Number = 0, top: Number = 0, right: Number = 0, bottom: Number = 0
    ) -> "Margin":
        """
        Applies margin to the specified sides.
        """
        return Margin(left=left, top=top, right=right, bottom=bottom)


MarginValue = Union[Number, Margin]
"""Type alias for margin values.

Represents margin as either:
- a single numeric value applied to all sides,
- or an explicit :class:`~flet.Margin` configuration.
"""
