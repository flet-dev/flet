from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union

from flet.controls.alignment import Alignment
from flet.controls.border import Border
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.gradients import Gradient
from flet.controls.transform import OffsetValue
from flet.controls.types import (
    BlendMode,
    ImageFit,
    ImageRepeat,
    Number,
    OptionalColorValue,
    OptionalNumber,
)

__all__ = [
    "BoxDecoration",
    "BoxShadow",
    "DecorationImage",
    "ColorFilter",
    "FilterQuality",
    "ShadowBlurStyle",
    "BoxShape",
    "BoxConstraints",
    "ShadowValue",
    "OptionalShadowValue",
    "OptionalBoxDecoration",
    "OptionalBoxShadow",
    "OptionalDecorationImage",
    "OptionalColorFilter",
    "OptionalFilterQuality",
    "OptionalShadowBlurStyle",
    "OptionalBoxShape",
    "OptionalBoxConstraints",
]


@dataclass
class ColorFilter:
    color: OptionalColorValue = None
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
    spread_radius: OptionalNumber = None
    blur_radius: OptionalNumber = None
    color: OptionalColorValue = None
    offset: Optional[OffsetValue] = None
    blur_style: ShadowBlurStyle = ShadowBlurStyle.NORMAL


ShadowValue = Union[BoxShadow, List[BoxShadow]]
OptionalShadowValue = Union[BoxShadow, List[BoxShadow]]


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
    bgcolor: OptionalColorValue = None
    image: Optional[DecorationImage] = None
    border: Optional[Border] = None
    border_radius: OptionalBorderRadiusValue = None
    shadow: Optional[ShadowValue] = None
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


# typing
OptionalBoxDecoration = Optional[BoxDecoration]
OptionalBoxShadow = Optional[BoxShadow]
OptionalDecorationImage = Optional[DecorationImage]
OptionalColorFilter = Optional[ColorFilter]
OptionalFilterQuality = Optional[FilterQuality]
OptionalShadowBlurStyle = Optional[ShadowBlurStyle]
OptionalBoxShape = Optional[BoxShape]
OptionalBoxConstraints = Optional[BoxConstraints]
