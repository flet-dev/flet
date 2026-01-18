import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment

__all__ = [
    "Gradient",
    "GradientTileMode",
    "LinearGradient",
    "RadialGradient",
    "SweepGradient",
]

from flet.controls.types import Number


class GradientTileMode(Enum):
    """
    Defines what happens at the edge of a gradient.
    More information about GradientTileMode [here](https://api.flutter.dev/flutter/dart-ui/TileMode.html).
    """

    CLAMP = "clamp"
    """
    Samples beyond the edge are clamped to the nearest color in the defined inner area.
    More information [here](https://api.flutter.dev/flutter/dart-ui/TileMode.html#clamp).
    """

    DECAL = "decal"
    """
    Samples beyond the edge are treated as transparent black.
    More information [here](https://api.flutter.dev/flutter/dart-ui/TileMode.html#decal).
    """

    MIRROR = "mirror"
    """
    Samples beyond the edge are mirrored back and forth across the defined area.
    More information [here](https://api.flutter.dev/flutter/dart-ui/TileMode.html#mirror).
    """

    REPEATED = "repeated"
    """
    Samples beyond the edge are repeated from the far end of the defined area.
    More information [here](https://api.flutter.dev/flutter/dart-ui/TileMode.html#repeated).
    """


@dataclass
class Gradient:
    """
    A shader that renders a color gradient.

    There are several types of gradients:

    - `LinearGradient`
    - `RadialGradient`
    - `SweepGradient`
    """

    colors: list[str]
    """
    The colors the gradient should obtain at
    each of the stops. This list must contain at least two colors.

    If [`stops`][(c).] is provided, this list must have the same length as it.
    """

    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    """
    How this gradient should tile the plane beyond in the region before `begin` and
    after `end`.
    """

    rotation: Optional[Number] = None
    """
    The rotation of the gradient in [radians](https://en.wikipedia.org/wiki/Radian),
    around the center-point of its bounding box.
    """

    stops: Optional[list[Number]] = None
    """
    A list of values from `0.0` to `1.0` that denote fractions along the gradient.

    If provided, this list must have the same length as [`colors`][(c).].
    If the first value is not `0.0`, then a stop with position `0.0` and a
    color equal to the first color in [`colors`][(c).] is implied.
    If the last value is not `1.0`, then a stop with position `1.0`
    and a color equal to the last color in [`colors`][(c).] is implied.
    """

    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)


@dataclass
class LinearGradient(Gradient):
    """
    Creates a linear gradient from `begin` to `end`.

    More information on
    [here](https://api.flutter.dev/flutter/painting/LinearGradient-class.html).
    """

    begin: Alignment = field(default_factory=lambda: Alignment.CENTER_LEFT)
    """
    The offset at which stop `0.0` of the gradient is placed.
    """

    end: Alignment = field(default_factory=lambda: Alignment.CENTER_RIGHT)
    """
    The offset at which stop `1.0` of the gradient is placed.
    """

    def __post_init__(self):
        self._type = "linear"


@dataclass
class RadialGradient(Gradient):
    """
    Creates a radial gradient centered at center that ends at radius distance from the
    center.

    More information
    [here](https://api.flutter.dev/flutter/painting/RadialGradient-class.html).
    """

    center: Alignment = field(default_factory=lambda: Alignment.CENTER)
    """
    The center of the gradient, as an offset into the `(-1.0, -1.0)` x `(1.0, 1.0)`
    square describing the gradient which will be mapped onto the paint box.
    For example, an alignment of `(0.0, 0.0)` will place the radial
    gradient in the center of the box.
    """

    radius: Number = 0.5
    """
    The radius of the gradient, as a fraction of the shortest side of the paint box.
    For example, if a radial gradient is painted on a box that is `100.0` pixels wide
    and `200.0` pixels tall, then a radius of `1.0` will place the `1.0` stop at
    `100.0` pixels from the [`center`][(c).].
    """

    focal: Optional[Alignment] = None
    """
    The focal point of the gradient. If specified, the gradient will appear to be
    focused along the vector from [`center`][(c).] to focal.
    """

    focal_radius: Number = 0.0
    """
    The radius of the focal point of gradient, as a fraction of the shortest side of the
    paint box. For example, if a radial gradient is painted on a box that is `100.0`
    pixels wide and `200.0` pixels tall, then a radius of `1.0` will place the `1.0`
    stop at `100.0` pixels from the focal point.
    """

    def __post_init__(self):
        self._type = "radial"


@dataclass
class SweepGradient(Gradient):
    """
    Creates a sweep gradient centered at center that starts at `start_angle` and ends
    at `end_angle`.

    More information
    [here](https://api.flutter.dev/flutter/painting/SweepGradient-class.html).
    """

    center: Alignment = field(default_factory=lambda: Alignment.CENTER)
    """
    The center of the gradient, as an offset into the `(-1.0, -1.0)` x `(1.0, 1.0)`
    square describing the gradient which will be mapped onto the paint box.

    For example, an [`Alignment.CENTER`][flet.] will place the sweep gradient
    in the center of the box.
    """

    start_angle: Number = 0.0
    """
    The angle in [radians](https://en.wikipedia.org/wiki/Radian) at which stop `0.0` of
    the gradient is placed.
    """

    end_angle: Number = math.pi * 2
    """
    The angle in [radians](https://en.wikipedia.org/wiki/Radian) at which stop `1.0` of
    the gradient is placed.
    """

    def __post_init__(self):
        self._type = "sweep"
