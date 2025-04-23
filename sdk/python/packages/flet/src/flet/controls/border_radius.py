import dataclasses
from typing import Optional, Union

__all__ = [
    "BorderRadius",
    "BorderRadiusValue",
    "OptionalBorderRadiusValue",
]

from flet.controls.types import Number


@dataclasses.dataclass
class BorderRadius:
    top_left: Number
    top_right: Number
    bottom_left: Number
    bottom_right: Number

    @classmethod
    def all(cls, value: Number) -> "BorderRadius":
        return BorderRadius(
            top_left=value, top_right=value, bottom_left=value, bottom_right=value
        )

    @classmethod
    def horizontal(cls, *, left: Number = 0, right: Number = 0) -> "BorderRadius":
        return BorderRadius(
            top_left=left, top_right=right, bottom_left=left, bottom_right=right
        )

    @classmethod
    def vertical(cls, *, top: Number = 0, bottom: Number = 0) -> "BorderRadius":
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
        return BorderRadius(
            top_left=top_left,
            top_right=top_right,
            bottom_left=bottom_left,
            bottom_right=bottom_right,
        )


BorderRadiusValue = Union[Number, BorderRadius]
OptionalBorderRadiusValue = Optional[BorderRadiusValue]
