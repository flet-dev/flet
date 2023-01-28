import dataclasses
from dataclasses import field
from typing import Optional

from flet_core.alignment import Alignment


@dataclasses.dataclass
class Scale:
    scale: Optional[float] = field(default=None)
    scale_x: Optional[float] = field(default=None)
    scale_y: Optional[float] = field(default=None)
    alignment: Optional[Alignment] = field(default=None)


@dataclasses.dataclass
class Rotate:
    angle: float
    alignment: Optional[Alignment] = field(default=None)


@dataclasses.dataclass
class Offset:
    x: float
    y: float
