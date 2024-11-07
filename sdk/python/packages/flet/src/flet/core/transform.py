from dataclasses import dataclass, field
from typing import Optional

from flet.core.alignment import Alignment


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
