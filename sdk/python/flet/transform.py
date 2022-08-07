import dataclasses
from dataclasses import field

from flet.alignment import Alignment


@dataclasses.dataclass
class Scale:
    scale: float = field(default=None)
    scale_x: float = field(default=None)
    scale_y: float = field(default=None)
    alignment: Alignment = field(default=None)


@dataclasses.dataclass
class Rotate:
    angle: float
    alignment: Alignment = field(default=None)


@dataclasses.dataclass
class Offset:
    x: float
    y: float
