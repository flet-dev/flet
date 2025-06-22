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
    """
    Defines what happens at the edge of a gradient.
    More information about GradientTileMode [here](https://api.flutter.dev/flutter/dart-ui/TileMode.html).
    """
    
    CLAMP = "clamp"
    """
    Samples beyond the edge are clamped to the nearest color in the defined inner area.
    More information on CLAMP GradientTileMode [here](https://api.flutter.dev/flutter/dart-ui/TileMode.html#clamp).
    """

    DECAL = "decal"
    """
    Samples beyond the edge are treated as transparent black.
    More information on DECAL GradientTileMode [here](https://api.flutter.dev/flutter/dart-ui/TileMode.html#decal).
    """
    
    MIRROR = "mirror"
    """
    Samples beyond the edge are mirrored back and forth across the defined area.
    More information on MIRROR GradientTileMode [here](https://api.flutter.dev/flutter/dart-ui/TileMode.html#mirror).
    """
    
    REPEATED = "repeated"
    """
    Samples beyond the edge are repeated from the far end of the defined area.
    More information on REPEATED GradientTileMode [here](https://api.flutter.dev/flutter/dart-ui/TileMode.html#repeated).
    """


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

    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)


@dataclass
class LinearGradient(Gradient):
    """
    Creates a linear gradient from `begin` to `end`.
    
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
        self._type = "linear"


@dataclass
class RadialGradient(Gradient):
    """
    Creates a radial gradient centered at center that ends at radius distance from the 
    center.
    
    More information on Radial gradient [here](https://api.flutter.dev/flutter/painting/
    RadialGradient-class.html)).
    """

    center: Alignment = field(default_factory=lambda: Alignment.center())
    """
    An instance of [Alignment](https://flet.dev/docs/reference/types/alignment) class.
    The center of the gradient, as an offset into the (-1.0, -1.0) x (1.0, 1.0) square
    describing the gradient which will be mapped onto the paint box. For example, an
    alignment of (0.0, 0.0) will place the radial gradient in the center of the box.
    """

    radius: Number = 0.5
    """
    The radius of the gradient, as a fraction of the shortest side of the paint box.
    For example, if a radial gradient is painted on a box that is 100.0 pixels wide and
    200.0 pixels tall, then a radius of 1.0 will place the 1.0 stop at 100.0 pixels from
    the `center`.
    """

    focal: Optional[Alignment] = None
    """
    The focal point of the gradient. If specified, the gradient will appear to be
    focused along the vector from `center` to focal.
    """

    focal_radius: Number = 0.0
    """
    The radius of the focal point of gradient, as a fraction of the shortest side of the
    paint box. For example, if a radial gradient is painted on a box that is 100.0
    pixels wide and 200.0 pixels tall, then a radius of 1.0 will place the 1.0 stop at
    100.0 pixels from the focal point.
    """

    def __post_init__(self):
        self._type = "radial"


@dataclass
class SweepGradient(Gradient):
    """
    Creates a sweep gradient centered at center that starts at `start_angle` and ends 
    at `end_angle`.
    
    More information on Sweep gradient [here](https://api.flutter.dev/flutter/painting/
    SweepGradient-class.html).
    """

    center: Alignment = field(default_factory=lambda: Alignment.center())
    """
    The center of the gradient, as an offset into the (-1.0, -1.0) x (1.0, 1.0) square
    describing the gradient which will be mapped onto the paint box. For example, an
    alignment of (0.0, 0.0) will place the sweep gradient in the center of the box.
    """

    start_angle: Number = 0.0
    """
    The angle in [radians](https://en.wikipedia.org/wiki/Radian) at which stop 0.0 of
    the gradient is placed. Defaults to 0.0.
    """

    end_angle: Number = math.pi * 2
    """
    The angle in [radians](https://en.wikipedia.org/wiki/Radian) at which stop 1.0 of
    the gradient is placed. Defaults to math.pi * 2.
    """

    def __post_init__(self):
        self._type = "sweep"

