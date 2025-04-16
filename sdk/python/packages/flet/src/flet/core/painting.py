import math
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple, Union

from flet.core.blur import Blur
from flet.core.gradients import GradientTileMode
from flet.core.types import BlendMode, ColorValue, OffsetValue, StrokeCap


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
    color_stops: Optional[List[float]] = None
    tile_mode: GradientTileMode = field(default=GradientTileMode.CLAMP)
    type: str = field(default="linear")


@dataclass
class PaintRadialGradient(PaintGradient):
    center: Optional[OffsetValue]
    radius: Union[float, int]
    colors: List[str]
    color_stops: Optional[List[float]] = None
    tile_mode: GradientTileMode = field(default=GradientTileMode.CLAMP)
    focal: Optional[OffsetValue] = None
    focal_radius: Union[float, int] = field(default=0.0)
    type: str = field(default="radial")


@dataclass
class PaintSweepGradient(PaintGradient):
    center: Optional[OffsetValue]
    colors: List[str]
    color_stops: Optional[List[float]] = None
    tile_mode: GradientTileMode = field(default=GradientTileMode.CLAMP)
    start_angle: float = field(default=0.0)
    end_angle: float = field(default=math.pi * 2)
    rotation: Union[None, float, int] = None
    type: str = field(default="sweep")


@dataclass
class Paint:
    color: Optional[ColorValue] = None
    blend_mode: Optional[BlendMode] = None
    blur_image: Union[
        None, float, int, Tuple[Union[float, int], Union[float, int]], Blur
    ] = None
    anti_alias: Optional[bool] = None
    gradient: Optional[PaintGradient] = None
    stroke_cap: Optional[StrokeCap] = None
    stroke_join: Optional[StrokeJoin] = None
    stroke_miter_limit: Optional[float] = None
    stroke_width: Optional[float] = None
    stroke_dash_pattern: Optional[List[float]] = None
    style: Optional[PaintingStyle] = None
