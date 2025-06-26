from dataclasses import dataclass
from typing import Optional, Tuple, Union

from flet.controls.alignment import OptionalAlignment
from flet.controls.types import Number, OptionalNumber

__all__ = [
    "Scale",
    "Rotate",
    "Offset",
    "ScaleValue",
    "RotateValue",
    "OffsetValue",
    "OptionalScaleValue",
    "OptionalRotateValue",
    "OptionalOffsetValue",
]


@dataclass
class Scale:
    scale: OptionalNumber = None
    scale_x: OptionalNumber = None
    scale_y: OptionalNumber = None
    alignment: OptionalAlignment = None


@dataclass
class Rotate:
    angle: Number
    alignment: OptionalAlignment = None


@dataclass
class Offset:
    x: Number
    y: Number

    @classmethod
    def zero(cls):
        return Offset(0, 0)


# typing
RotateValue = Union[Number, Rotate]
OptionalRotateValue = Optional[RotateValue]
ScaleValue = Union[Number, Scale]
OptionalScaleValue = Optional[ScaleValue]
OffsetValue = Union[Offset, Tuple[Number, Number]]
OptionalOffsetValue = Optional[OffsetValue]
