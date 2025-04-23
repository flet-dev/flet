from dataclasses import dataclass
from typing import Optional, Union

__all__ = [
    "Padding",
    "PaddingValue",
    "OptionalPaddingValue",
]

from flet.controls.types import Number


@dataclass
class Padding:
    left: Number
    top: Number
    right: Number
    bottom: Number

    @classmethod
    def all(cls, value: Number) -> "Padding":
        return Padding(left=value, top=value, right=value, bottom=value)

    @classmethod
    def symmetric(cls, *, vertical: Number = 0, horizontal: Number = 0) -> "Padding":
        return Padding(left=horizontal, top=vertical, right=horizontal, bottom=vertical)

    @classmethod
    def only(
        cls, *, left: Number = 0, top: Number = 0, right: Number = 0, bottom: Number = 0
    ) -> "Padding":
        return Padding(left=left, top=top, right=right, bottom=bottom)


PaddingValue = Union[Number, Padding]
OptionalPaddingValue = Optional[PaddingValue]
