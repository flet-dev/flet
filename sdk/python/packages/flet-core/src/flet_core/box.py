from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Union

from flet_core.alignment import Alignment
from flet_core.border import Border
from flet_core.gradients import Gradient
from flet_core.types import (
    OffsetValue,
    BorderRadiusValue,
    BlendMode,
    ImageFit,
    OptionalNumber,
    ImageRepeat,
)


@dataclass
class ColorFilter:
    color: Optional[str] = field(default=None)
    blend_mode: Optional[BlendMode] = field(default=None)


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
    spread_radius: Optional[float] = field(default=None)
    blur_radius: Optional[float] = field(default=None)
    color: Optional[str] = field(default=None)
    offset: OffsetValue = field(default=None)
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
    bgcolor: Optional[str] = None
    image: Optional[DecorationImage] = None
    border: Optional[Border] = None
    border_radius: BorderRadiusValue = None
    shadow: Union[None, BoxShadow, List[BoxShadow]] = None
    gradient: Optional[Gradient] = None
    shape: Optional[BoxShape] = None
    blend_mode: Optional[BlendMode] = None
