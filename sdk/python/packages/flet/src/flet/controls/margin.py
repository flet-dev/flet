from dataclasses import dataclass
from typing import Optional, Union

from flet.controls.types import Number
from flet.utils import deprecated

__all__ = ["Margin", "MarginValue", "OptionalMarginValue"]


@dataclass
class Margin:
    left: Number
    top: Number
    right: Number
    bottom: Number

    @classmethod
    def all(cls, value: Number) -> "Margin":
        return Margin(left=value, top=value, right=value, bottom=value)

    @classmethod
    def symmetric(cls, *, vertical: Number = 0, horizontal: Number = 0) -> "Margin":
        return Margin(left=horizontal, top=vertical, right=horizontal, bottom=vertical)

    @classmethod
    def only(
        cls, *, left: Number = 0, top: Number = 0, right: Number = 0, bottom: Number = 0
    ) -> "Margin":
        return Margin(left=left, top=top, right=right, bottom=bottom)


@deprecated(
    reason="Use Margin.all() instead",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def all(value: float) -> Margin:
    return Margin(left=value, top=value, right=value, bottom=value)


@deprecated(
    reason="Use Margin.symmetric() instead",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def symmetric(vertical: float = 0, horizontal: float = 0) -> Margin:
    return Margin(left=horizontal, top=vertical, right=horizontal, bottom=vertical)


@deprecated(
    reason="Use Margin.only() instead",
    version="0.70.0",
    delete_version="0.73.0",
    show_parentheses=True,
)
def only(
    left: float = 0, top: float = 0, right: float = 0, bottom: float = 0
) -> Margin:
    return Margin(left=left, top=top, right=right, bottom=bottom)


MarginValue = Union[Number, Margin]
OptionalMarginValue = Optional[MarginValue]
