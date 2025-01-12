from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union

from flet.core.alignment import Alignment
from flet.core.border import Border
from flet.core.gradients import Gradient
from flet.core.types import (
    BlendMode,
    BorderRadiusValue,
    ColorValue,
    ImageFit,
    ImageRepeat,
    Number,
    OffsetValue,
    OptionalNumber,
)


@dataclass
class ColorFilter:
    color: Optional[ColorValue] = None
    blend_mode: Optional[BlendMode] = None


class FilterQuality(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ShadowBlurStyle(Enum):
    NORMAL = "normal"
    SOLID = "solid"
    OUTER = "outer"
    INNER = "inner"


@dataclass
class BoxShadow:
    spread_radius: Optional[float] = None
    blur_radius: Optional[float] = None
    color: Optional[ColorValue] = None
    offset: Optional[OffsetValue] = None
    blur_style: ShadowBlurStyle = field(default=ShadowBlurStyle.NORMAL)


class BoxShape(Enum):
    RECTANGLE = "rectangle"
    CIRCLE = "circle"


@dataclass
class DecorationImage:
    src: Optional[str] = None
    src_base64: Optional[str] = None
    color_filter: Optional[ColorFilter] = None
    fit: Optional[ImageFit] = None
    alignment: Optional[Alignment] = None
    repeat: Optional[ImageRepeat] = None
    match_text_direction: Optional[bool] = None
    scale: OptionalNumber = None
    opacity: OptionalNumber = None
    filter_quality: Optional[FilterQuality] = None
    invert_colors: Optional[bool] = None
    anti_alias: Optional[bool] = None


@dataclass
class BoxDecoration:
    bgcolor: Optional[ColorValue] = None
    image: Optional[DecorationImage] = None
    border: Optional[Border] = None
    border_radius: Optional[BorderRadiusValue] = None
    shadow: Union[None, BoxShadow, List[BoxShadow]] = None
    gradient: Optional[Gradient] = None
    shape: Optional[BoxShape] = None
    blend_mode: Optional[BlendMode] = None


@dataclass
class BoxConstraints:
    min_width: Number = 0
    min_height: Number = 0
    max_width: Number = float("inf")
    max_height: Number = float("inf")

    def __post_init__(self):
        assert (
            0 <= self.min_width <= self.max_width <= float("inf")
        ), "min_width and max_width must be between 0 and infinity and min_width must be less than or equal to max_width"
        assert (
            0 <= self.min_height <= self.max_height <= float("inf")
        ), "min_height and max_height must be between 0 and infinity and min_height must be less than or equal to max_height"
