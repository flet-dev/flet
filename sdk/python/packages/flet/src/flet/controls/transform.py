from dataclasses import dataclass
from typing import Optional, Tuple, Union

from flet.controls.alignment import Alignment
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
    alignment: Optional[Alignment] = None


@dataclass
class Rotate:
    angle: Number
    alignment: Optional[Alignment] = None


@dataclass
class Offset:
    x: Number
    y: Number


RotateValue = Union[Number, Rotate]
OptionalRotateValue = Optional[RotateValue]
ScaleValue = Union[Number, Scale]
OptionalScaleValue = Optional[ScaleValue]
OffsetValue = Union[Offset, Tuple[Number, Number]]
OptionalOffsetValue = Optional[OffsetValue]
