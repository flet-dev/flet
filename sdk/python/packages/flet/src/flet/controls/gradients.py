import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

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
    """
    A shader that renders a color gradient.

    There are several types of gradients: `LinearGradient`, `RadialGradient` and 
    `SweepGradient`.
    """

    colors: list[str]
    """
    The [colors](https://flet.dev/docs/reference/colors) the gradient should obtain at 
    each of the stops. This list must contain at least two colors.

    If `stops` is provided, this list must have the same length as `stops`.
    """

    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    """
    How this gradient should tile the plane beyond in the region before `begin` and 
    after `end`. The value is of type
    [GradientTileMode](https://flet.dev/docs/reference/types/gradienttilemode).
    """

    rotation: OptionalNumber = None
    """
    The rotation of the gradient in
    [radians](https://en.wikipedia.org/wiki/Radian), around the center-point of its
    bounding box.
    """

    stops: Optional[list[Number]] = None
    """
    A list of values from `0.0` to `1.0` that denote fractions along the gradient.

    If provided, this list must have the same length as `colors`. If the first value is
    not `0.0`, then a stop with position `0.0` and a color equal to the first color in
    `colors` is implied. If the last value is not `1.0`, then a stop with position `1.0`
    and a color equal to the last color in `colors` is implied.
    """

    type: str = ""


@dataclass
class LinearGradient(Gradient):
    """
    More information on Linear gradient [here](https://api.flutter.dev/flutter/painting/LinearGradient-class.html).
    """

    begin: Alignment = field(default_factory=lambda: Alignment.center_left())
    """
    An instance of [Alignment](https://flet.dev/docs/reference/types/alignment). The
    offset at which stop `0.0` of the gradient is placed.
    """

    end: Alignment = field(default_factory=lambda: Alignment.center_right())
    """
    An instance of [Alignment](https://flet.dev/docs/reference/types/alignment). The
    offset at which stop `1.0` of the gradient is placed.
    """

    def __post_init__(self):
        self.type = "linear"



@dataclass
class RadialGradient(Gradient):
    center: Alignment = field(default_factory=lambda: Alignment.center())
    radius: Number = 0.5
    focal: Optional[Alignment] = None
    focal_radius: Number = 0.0

    def __post_init__(self):
        self.type = "radial"


@dataclass
class SweepGradient(Gradient):
    center: Alignment = field(default_factory=lambda: Alignment.center())
    start_angle: Number = 0.0
    end_angle: Number = math.pi * 2

    def __post_init__(self):
        self.type = "sweep"
