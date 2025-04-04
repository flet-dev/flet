from dataclasses import dataclass
from typing import Optional, Union

__all__ = [
    "Padding",
    "all",
    "symmetric",
    "only",
    "PaddingValue",
    "OptionalPaddingValue",
]

from flet.core.types import Number


@dataclass
class Padding:
    left: Number
    top: Number
    right: Number
    bottom: Number


def all(value: Number) -> Padding:
    return Padding(left=value, top=value, right=value, bottom=value)


def symmetric(vertical: Number = 0, horizontal: Number = 0) -> Padding:
    return Padding(left=horizontal, top=vertical, right=horizontal, bottom=vertical)


def only(
    left: Number = 0, top: Number = 0, right: Number = 0, bottom: Number = 0
) -> Padding:
    return Padding(left=left, top=top, right=right, bottom=bottom)


PaddingValue = Union[Number, Padding]
OptionalPaddingValue = Optional[PaddingValue]
