import math
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from flet.core.blur import BlurValue
from flet.core.gradients import GradientTileMode
from flet.core.types import (
    BlendMode,
    ColorValue,
    OffsetValue,
    StrokeCap,
    Number,
    OptionalNumber,
)


class StrokeJoin(Enum):
    MITER = "miter"
    ROUND = "round"
    BEVEL = "bevel"


class PaintingStyle(Enum):
    FILL = "fill"
    STROKE = "stroke"


@dataclass
class PaintGradient:
    pass


@dataclass
class PaintLinearGradient(PaintGradient):
    begin: Optional[OffsetValue]
    end: Optional[OffsetValue]
    colors: List[str]
    color_stops: Optional[List[Number]] = None
    tile_mode: GradientTileMode = field(default=GradientTileMode.CLAMP)

    def __post_init__(self):
        self.type = "linear"


@dataclass
class PaintRadialGradient(PaintGradient):
    center: Optional[OffsetValue]
    radius: Number
    colors: List[str]
    color_stops: Optional[List[float]] = None
    tile_mode: GradientTileMode = field(default=GradientTileMode.CLAMP)
    focal: Optional[OffsetValue] = None
    focal_radius: Number = field(default=0.0)

    def __post_init__(self):
        self.type = "radial"


@dataclass
class PaintSweepGradient(PaintGradient):
    center: Optional[OffsetValue]
    colors: List[str]
    color_stops: Optional[List[Number]] = None
    tile_mode: GradientTileMode = field(default=GradientTileMode.CLAMP)
    start_angle: Number = field(default=0.0)
    end_angle: Number = field(default=math.pi * 2)
    rotation: OptionalNumber = None

    def __post_init__(self):
        self.type = "sweep"


@dataclass
class Paint:
    color: Optional[ColorValue] = None
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
