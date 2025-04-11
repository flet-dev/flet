import math
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from flet.controls import alignment
from flet.controls.alignment import Alignment

__all__ = [
    "Gradient",
    "LinearGradient",
    "RadialGradient",
    "SweepGradient",
    "GradientTileMode",
]

from flet.controls.types import Number, OptionalNumber


class GradientTileMode(Enum):
    CLAMP = "clamp"
    DECAL = "decal"
    MIRROR = "mirror"
    REPEATED = "repeated"


@dataclass
class Gradient:
    colors: List[str]
    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    rotation: OptionalNumber = None
    stops: Optional[List[Number]] = None
    type: str = ""


@dataclass
class LinearGradient(Gradient):
    begin: Alignment = field(default_factory=lambda: alignment.center_left)
    end: Alignment = field(default_factory=lambda: alignment.center_right)

    def __post_init__(self):
        self.type = "linear"


@dataclass
class RadialGradient(Gradient):
    center: Alignment = field(default_factory=lambda: alignment.center)
    radius: Number = 0.5
    focal: Optional[Alignment] = None
    focal_radius: Number = 0.0

    def __post_init__(self):
        self.type = "radial"


@dataclass
class SweepGradient(Gradient):
    center: Alignment = field(default_factory=lambda: alignment.center)
    start_angle: Number = 0.0
    end_angle: Number = math.pi * 2

    def __post_init__(self):
        self.type = "sweep"
