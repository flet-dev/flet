import dataclasses
import math
from dataclasses import field
from enum import Enum
from typing import List, Optional, Union

from flet_core import alignment
from flet_core.alignment import Alignment

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class GradientTileMode(Enum):
    CLAMP = "clamp"
    DECAL = "decal"
    MIRROR = "mirror"
    REPEATED = "repeated"


@dataclasses.dataclass
class Gradient:
    colors: List[str]
    tile_mode: GradientTileMode = field(default=GradientTileMode.CLAMP)
    rotation: Union[None, float, int] = field(default=None)
    stops: Optional[List[float]] = field(default=None)


@dataclasses.dataclass
class LinearGradient(Gradient):
    begin: Alignment = field(default_factory=lambda: alignment.center_left)
    end: Alignment = field(default_factory=lambda: alignment.center_right)
    type: str = field(default="linear")


@dataclasses.dataclass
class RadialGradient(Gradient):
    center: Alignment = field(default_factory=lambda: alignment.center)
    radius: Union[float, int] = field(default=0.5)
    focal: Optional[Alignment] = field(default=None)
    focal_radius: Union[float, int] = field(default=0.0)
    type: str = field(default="radial")


@dataclasses.dataclass
class SweepGradient(Gradient):
    center: Alignment = field(default_factory=lambda: alignment.center)
    start_angle: Union[float, int] = field(default=0.0)
    end_angle: Union[float, int] = field(default=math.pi * 2)
    type: str = field(default="sweep")
