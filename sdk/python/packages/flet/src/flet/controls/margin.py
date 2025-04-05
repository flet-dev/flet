from dataclasses import dataclass
from typing import Optional, Union

__all__ = ["Margin", "all", "symmetric", "only", "MarginValue", "OptionalMarginValue"]

from flet.controls.types import Number


@dataclass
class Margin:
    left: Number
    top: Number
    right: Number
    bottom: Number


def all(value: Number) -> Margin:
    return Margin(left=value, top=value, right=value, bottom=value)


def symmetric(vertical: Number = 0, horizontal: Number = 0) -> Margin:
    return Margin(left=horizontal, top=vertical, right=horizontal, bottom=vertical)


def only(
    left: Number = 0, top: Number = 0, right: Number = 0, bottom: Number = 0
) -> Margin:
    return Margin(left=left, top=top, right=right, bottom=bottom)


MarginValue = Union[Number, Margin]
OptionalMarginValue = Optional[MarginValue]
