from dataclasses import dataclass, field
from typing import Optional

from flet.core.alignment import Alignment

__all__ = ["Scale", "Rotate", "Offset"]


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


# RotateValue = Union[Number, Rotate]
# ScaleValue = Union[Number, Scale]
# OffsetValue = Union[Offset, Tuple[Number, Number]]
