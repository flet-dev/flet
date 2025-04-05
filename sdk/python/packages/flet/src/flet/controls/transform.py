from dataclasses import dataclass, field
from typing import Optional, Tuple, Union

from flet.controls.alignment import Alignment
from flet.controls.types import Number

__all__ = ["Scale", "Rotate", "Offset", "ScaleValue", "RotateValue", "OffsetValue"]


@dataclass
class Scale:
    scale: Optional[float] = field(default=None)
    scale_x: Optional[float] = field(default=None)
    scale_y: Optional[float] = field(default=None)
    alignment: Optional[Alignment] = field(default=None)


@dataclass
class Rotate:
    angle: float
    alignment: Optional[Alignment] = field(default=None)


@dataclass
class Offset:
    x: float
    y: float


RotateValue = Union[Number, Rotate]
ScaleValue = Union[Number, Scale]
OffsetValue = Union[Offset, Tuple[Number, Number]]
