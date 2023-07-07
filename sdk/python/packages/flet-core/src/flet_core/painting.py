import dataclasses
import math
from enum import Enum
from typing import List, Optional, Tuple, Union

from flet_core.blur import Blur
from flet_core.gradients import GradientTileMode
from flet_core.types import BlendMode, OffsetValue


class StrokeCap(Enum):
    BUTT = "butt"
    ROUND = "round"
    SQUARE = "square"


class StrokeJoin(Enum):
    MITER = "miter"
    ROUND = "round"
    BEVEL = "bevel"


class PaintingStyle(Enum):
    FILL = "fill"
    STROKE = "stroke"


@dataclasses.dataclass
class PaintGradient:
    pass


@dataclasses.dataclass
class PaintLinearGradient(PaintGradient):
    begin: OffsetValue
    end: OffsetValue
    colors: List[str]
    color_stops: Optional[List[float]] = dataclasses.field(default=None)
    tile_mode: GradientTileMode = dataclasses.field(default=GradientTileMode.CLAMP)
    type: str = dataclasses.field(default="linear")


@dataclasses.dataclass
class PaintRadialGradient(PaintGradient):
    center: OffsetValue
    radius: Union[float, int]
    colors: List[str]
    color_stops: Optional[List[float]] = dataclasses.field(default=None)
    tile_mode: GradientTileMode = dataclasses.field(default=GradientTileMode.CLAMP)
    focal: Optional[OffsetValue] = dataclasses.field(default=None)
    focal_radius: Union[float, int] = dataclasses.field(default=0.0)
    type: str = dataclasses.field(default="radial")


@dataclasses.dataclass
class PaintSweepGradient(PaintGradient):
    center: OffsetValue
    colors: List[str]
    color_stops: Optional[List[float]] = dataclasses.field(default=None)
    tile_mode: GradientTileMode = dataclasses.field(default=GradientTileMode.CLAMP)
    start_angle: float = dataclasses.field(default=0.0)
    end_angle: float = dataclasses.field(default=math.pi * 2)
    rotation: Union[None, float, int] = dataclasses.field(default=None)
    type: str = dataclasses.field(default="sweep")


@dataclasses.dataclass
class Paint:
    color: Optional[str] = dataclasses.field(default=None)
    blend_mode: Optional[BlendMode] = dataclasses.field(default=None)
    blur_image: Union[
        None, float, int, Tuple[Union[float, int], Union[float, int]], Blur
    ] = dataclasses.field(default=None)
    anti_alias: Optional[bool] = dataclasses.field(default=None)
    gradient: Optional[PaintGradient] = dataclasses.field(default=None)
    stroke_cap: Optional[StrokeCap] = dataclasses.field(default=None)
    stroke_join: Optional[StrokeJoin] = dataclasses.field(default=None)
    stroke_miter_limit: Optional[float] = dataclasses.field(default=None)
    stroke_width: Optional[float] = dataclasses.field(default=None)
    stroke_dash_pattern: Optional[List[float]] = dataclasses.field(default=None)
    style: Optional[PaintingStyle] = dataclasses.field(default=None)
