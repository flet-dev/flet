import dataclasses
import math
from dataclasses import field
from typing import List, Union

from flet import alignment
from flet.alignment import Alignment

try:
    from typing import Literal
except:
    from typing_extensions import Literal

TileMode = Literal["clamp", "decal", "mirror", "repeated"]


@dataclasses.dataclass
class Gradient:
    colors: List[str]
    tile_mode: TileMode = field(default="clamp")
    rotation: Union[float, int] = field(default=None)
    stops: List[float] = field(default=None)


@dataclasses.dataclass
class LinearGradient(Gradient):
    begin: Alignment = field(default=alignment.center_left)
    end: Alignment = field(default=alignment.center_right)
    type: str = field(default="linear")


@dataclasses.dataclass
class RadialGradient(Gradient):
    center: Alignment = field(default=alignment.center)
    radius: Union[float, int] = field(default=0.5)
    focal: Alignment = field(default=None)
    focal_radius: Union[float, int] = field(default=0.0)
    type: str = field(default="radial")


@dataclasses.dataclass
class SweepGradient(Gradient):
    center: Alignment = field(default=alignment.center)
    start_angle: Union[float, int] = field(default=0.0)
    end_angle: Union[float, int] = field(default=math.pi * 2)
    type: str = field(default="sweep")
