from dataclasses import dataclass
from typing import Union

from flet.controls.types import Number
from flet.utils import deprecated

__all__ = [
    "Padding",
    "PaddingValue",
    "all",
    "only",
    "symmetric",
]


@dataclass
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
        Applies `vertical` padding to top and bottom sides and `horizontal` padding to
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


@deprecated(
    reason="Use Padding.all() instead",
    version="0.80.0",
    delete_version="0.83.0",
    show_parentheses=True,
)
def all(value: float) -> Padding:
    return Padding(left=value, top=value, right=value, bottom=value)


@deprecated(
    reason="Use Padding.symmetric() instead",
    version="0.80.0",
    delete_version="0.83.0",
    show_parentheses=True,
)
def symmetric(vertical: float = 0, horizontal: float = 0) -> Padding:
    return Padding(left=horizontal, top=vertical, right=horizontal, bottom=vertical)


@deprecated(
    reason="Use Padding.only() instead",
    version="0.80.0",
    delete_version="0.83.0",
    show_parentheses=True,
)
def only(
    left: float = 0, top: float = 0, right: float = 0, bottom: float = 0
) -> Padding:
    return Padding(left=left, top=top, right=right, bottom=bottom)


PaddingValue = Union[Number, Padding]
