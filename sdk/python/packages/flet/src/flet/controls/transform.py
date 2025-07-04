from dataclasses import dataclass
from typing import Optional, Union

from flet.controls.alignment import Alignment
from flet.controls.types import Number

__all__ = [
    "Scale",
    "Rotate",
    "Offset",
    "ScaleValue",
    "RotateValue",
    "OffsetValue",
]


@dataclass
class Scale:
    scale: Optional[Number] = None
    scale_x: Optional[Number] = None
    scale_y: Optional[Number] = None
    alignment: Optional[Alignment] = None


@dataclass
class Rotate:
    angle: Number
    alignment: Optional[Alignment] = None


@dataclass
class Offset:
    x: Number = 0
    y: Number = 0


# typing
RotateValue = Union[Number, Rotate]
ScaleValue = Union[Number, Scale]
OffsetValue = Union[Offset, tuple[Number, Number]]
