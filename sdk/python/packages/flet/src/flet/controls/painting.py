import math
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

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
    type: str = ""


@dataclass
class PaintLinearGradient(PaintGradient):
    begin: Optional[OffsetValue]
    end: Optional[OffsetValue]
    colors: List[str]
    color_stops: Optional[List[Number]] = None
    tile_mode: GradientTileMode = GradientTileMode.CLAMP

    def __post_init__(self):
        self.type = "linear"


@dataclass
class PaintRadialGradient(PaintGradient):
    center: Optional[OffsetValue]
    radius: Number
    colors: List[str]
    color_stops: Optional[List[float]] = None
    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    focal: Optional[OffsetValue] = None
    focal_radius: Number = 0.0

    def __post_init__(self):
        self.type = "radial"


@dataclass
class PaintSweepGradient(PaintGradient):
    center: Optional[OffsetValue]
    colors: List[str]
    color_stops: Optional[List[Number]] = None
    tile_mode: GradientTileMode = GradientTileMode.CLAMP
    start_angle: Number = 0.0
    end_angle: Number = math.pi * 2
    rotation: OptionalNumber = None

    def __post_init__(self):
        self.type = "sweep"


@dataclass
class Paint:
    color: OptionalColorValue = None
    blend_mode: Optional[BlendMode] = None
    blur_image: Optional[BlurValue] = None
    anti_alias: Optional[bool] = None
    gradient: Optional[PaintGradient] = None
    stroke_cap: Optional[StrokeCap] = None
    stroke_join: Optional[StrokeJoin] = None
    stroke_miter_limit: OptionalNumber = None
    stroke_width: OptionalNumber = None
    stroke_dash_pattern: Optional[List[Number]] = None
    style: Optional[PaintingStyle] = None
