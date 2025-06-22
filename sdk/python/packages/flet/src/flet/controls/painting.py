import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.blur import BlurValue
from flet.controls.gradients import GradientTileMode
from flet.controls.transform import OffsetValue
from flet.controls.types import (
    BlendMode,
    Number,
    OptionalColorValue,
    OptionalNumber,
    StrokeCap,
    StrokeJoin,
)

__all__ = [
    "Paint",
    "PaintGradient",
    "PaintLinearGradient",
    "PaintRadialGradient",
    "PaintSweepGradient",
    "PaintingStyle",
]


class PaintingStyle(Enum):
    FILL = "fill"
    STROKE = "stroke"


@dataclass(kw_only=True)
class PaintGradient:
    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)


@dataclass
class PaintLinearGradient(PaintGradient):
    """
    More information on Linear gradient
    https://api.flutter.dev/flutter/dart-ui/Gradient/Gradient.linear.html
    """

    begin: Optional[OffsetValue]
    """
    An instance of https://flet.dev/docs/reference/types/offset. The offset at which
    stop 0.0 of the gradient is placed.
    """

    end: Optional[OffsetValue]
    """
    An instance of https://flet.dev/docs/reference/types/offset. The offset at which
    stop 1.0 of the gradient is placed.
    """

    colors: list[str]
    """
    The https://flet.dev/docs/reference/colors the gradient should obtain at each of
    the stops. This list must contain at least two colors.

    If `stops` is provided, this list must have the same length as `stops`.
    """

    color_stops: Optional[list[Number]] = None
    """
    A list of values from `0.0` to `1.0` that denote fractions along the gradient.

    If provided, this list must have the same length as `colors`. If the first value
    is not `0.0`, then a stop with position `0.0` and a color equal to the first color
    in `colors` is implied. If the last value is not `1.0`, then a stop with position
    `1.0` and a color equal to the last color in `colors` is implied.
    """

    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    """
    How this gradient should tile the plane beyond in the region before `begin` and
    after `end`. The value is `GradientTileMode` enum with supported values: `CLAMP`
    (default), `DECAL`, `MIRROR`, `REPEATED`. More info here:
    https://api.flutter.dev/flutter/dart-ui/TileMode.html
    """

    def __post_init__(self):
        self._type = "linear"


@dataclass
class PaintRadialGradient(PaintGradient):
    """
    More information on Radial gradient
    https://api.flutter.dev/flutter/dart-ui/Gradient/Gradient.radial.html
    """

    center: Optional[OffsetValue]
    """
    An instance of https://flet.dev/docs/reference/types/offset class. The center of
    the gradient.
    """

    radius: Number
    """
    The radius of the gradient.
    """

    colors: list[str]
    """
    The https://flet.dev/docs/reference/colors the gradient should obtain at each of
    the stops. This list must contain at least two colors.

    If `stops` is provided, this list must have the same length as `stops`.
    """

    color_stops: Optional[list[float]] = None
    """
    A list of values from `0.0` to `1.0` that denote fractions along the gradient.

    If provided, this list must have the same length as `colors`. If the first value
    is not `0.0`, then a stop with position `0.0` and a color equal to the first color
    in `colors` is implied. If the last value is not `1.0`, then a stop with position
    `1.0` and a color equal to the last color in `colors` is implied.
    """

    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    """
    How this gradient should tile the plane beyond in the region before `begin` and
    after `end`. The value is of type
    https://flet.dev/docs/reference/types/gradienttilemode.
    """

    focal: Optional[OffsetValue] = None
    """
    The focal point of the gradient. If specified, the gradient will appear to be
    focused along the vector from `center` to focal.
    """

    focal_radius: Number = 0.0
    """
    The radius of the focal point of gradient, as a fraction of the shortest side of
    the paint box.

    For example, if a radial gradient is painted on a box that is `100.0` pixels wide
    and `200.0` pixels tall, then a radius of `1.0` will place the `1.0` stop at
    `100.0` pixels from the focal point.
    """

    def __post_init__(self):
        self._type = "radial"


@dataclass
class PaintSweepGradient(PaintGradient):
    """
    More information on Sweep gradient
    https://api.flutter.dev/flutter/dart-ui/Gradient/Gradient.sweep.html
    """

    center: Optional[OffsetValue]
    """
    An instance of https://flet.dev/docs/reference/types/offset class. The center of
    the gradient.
    """

    colors: list[str]
    """
    The https://flet.dev/docs/reference/colors the gradient should obtain at each of
    the stops. This list must contain at least two colors.

    If `stops` is provided, this list must have the same length as `stops`.
    """

    color_stops: Optional[list[Number]] = None
    """
    A list of values from `0.0` to `1.0` that denote fractions along the gradient.

    If provided, this list must have the same length as `colors`. If the first value
    is not `0.0`, then a stop with position `0.0` and a color equal to the first color
    in `colors` is implied. If the last value is not `1.0`, then a stop with position
    `1.0` and a color equal to the last color in `colors` is implied.
    """

    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    """
    How this gradient should tile the plane beyond in the region before `begin` and
    after `end`. The value is of type
    https://flet.dev/docs/reference/types/gradienttilemode.
    """

    start_angle: Number = 0.0
    """
    The angle in https://en.wikipedia.org/wiki/Radian at which stop 0.0 of the
    gradient is placed. Defaults to 0.0.
    """

    end_angle: Number = math.pi * 2
    """
    The angle in radians at which stop 1.0 of the gradient is placed. Defaults to
    math.pi * 2.
    """

    rotation: OptionalNumber = None
    """
    The rotation of the gradient in https://en.wikipedia.org/wiki/Radian, around the
    center-point of its bounding box.
    """

    def __post_init__(self):
        self._type = "sweep"


@dataclass
class Paint:
    """
    A description of the style to use when drawing a shape on the canvas.
    """

    color: OptionalColorValue = None
    """
    The https://flet.dev/docs/reference/colors to use when stroking or filling a shape.
    Defaults to opaque black.
    """

    blend_mode: Optional[BlendMode] = None
    """
    A blend mode to apply when a shape is drawn or a layer is composited.

    Value is of type https://flet.dev/docs/reference/types/blendmode and defaults to
    `BlendMode.SRC_OVER`.
    """

    blur_image: Optional[BlurValue] = None
    """
    Blur image when drawing it on a canvas.

    See https://flet.dev/docs/controls/container#blur for more information.
    """

    anti_alias: Optional[bool] = None
    """
    Whether to apply anti-aliasing to lines and images drawn on the canvas.

    Defaults to `True`.
    """

    gradient: Optional[PaintGradient] = None
    """
    Configures gradient paint. Value is an instance of one of the following classes:

    * https://flet.dev/docs/reference/types/paintlineargradient
    * https://flet.dev/docs/reference/types/paintradialgradient
    * https://flet.dev/docs/reference/types/paintsweepgradient
    """

    stroke_cap: Optional[StrokeCap] = None
    """
    TBD
    """

    stroke_join: Optional[StrokeJoin] = None
    """
    TBD
    """

    stroke_miter_limit: OptionalNumber = None
    """
    TBD
    """

    stroke_width: OptionalNumber = None
    """
    TBD
    """

    stroke_dash_pattern: Optional[list[Number]] = None
    """
    TBD
    """

    style: Optional[PaintingStyle] = None
    """
    TBD
    """
