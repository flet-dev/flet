from dataclasses import dataclass
from typing import Optional, Union

from flet.controls.types import Number

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


MarginValue = Union[Number, Margin]
OptionalMarginValue = Optional[MarginValue]
