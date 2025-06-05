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
    # type: str = ""
    type: str = field(default="", init=False, repr=False)


@dataclass
class PaintLinearGradient(PaintGradient):
    begin: Optional[OffsetValue]
    end: Optional[OffsetValue]
    colors: list[str]
    color_stops: Optional[list[Number]] = None
    tile_mode: GradientTileMode = GradientTileMode.CLAMP

    def __post_init__(self):
        self.type = "linear"


@dataclass
class PaintRadialGradient(PaintGradient):
    center: Optional[OffsetValue]
    radius: Number
    colors: list[str]
    color_stops: Optional[list[float]] = None
    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    focal: Optional[OffsetValue] = None
    focal_radius: Number = 0.0

    def __post_init__(self):
        self.type = "radial"


@dataclass
class PaintSweepGradient(PaintGradient):
    center: Optional[OffsetValue]
    colors: list[str]
    color_stops: Optional[list[Number]] = None
    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    start_angle: Number = 0.0
    end_angle: Number = math.pi * 2
    rotation: OptionalNumber = None

    def __post_init__(self):
        self.type = "sweep"


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
