import dataclasses
import math
from dataclasses import field
from typing import List, Optional, Union

from flet.core import alignment
from flet.core.alignment import Alignment
from flet.core.enumerations import ExtendedEnum
from flet.core.types import ColorValue


class GradientTileMode(ExtendedEnum):
    CLAMP = "clamp"
    DECAL = "decal"
    MIRROR = "mirror"
    REPEATED = "repeated"


@dataclasses.dataclass
class Gradient:
    colors: List[ColorValue]
    tile_mode: Optional[GradientTileMode] = GradientTileMode.CLAMP
    rotation: Union[None, float, int] = None
    stops: Optional[List[float]] = None


@dataclasses.dataclass
class LinearGradient(Gradient):
    begin: Alignment = field(default_factory=lambda: alignment.center_left)
    end: Alignment = field(default_factory=lambda: alignment.center_right)

    def __post_init__(self):
        self.type = "linear"


@dataclasses.dataclass
class RadialGradient(Gradient):
    center: Alignment = field(default_factory=lambda: alignment.center)
    radius: Union[float, int] = field(default=0.5)
    focal: Optional[Alignment] = field(default=None)
    focal_radius: Union[float, int] = field(default=0.0)

    def __post_init__(self):
        self.type = "radial"


@dataclasses.dataclass
class SweepGradient(Gradient):
    center: Alignment = field(default_factory=lambda: alignment.center)
    start_angle: Union[float, int] = field(default=0.0)
    end_angle: Union[float, int] = field(default=math.pi * 2)

    def __post_init__(self):
        self.type = "sweep"
