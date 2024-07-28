from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Union

from flet_core.border import Border
from flet_core.gradients import Gradient
from flet_core.types import OffsetValue, BorderRadiusValue, BlendMode


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
class BoxDecoration:
    color: Optional[str] = None
    image: Optional[str] = None
    border: Optional[Border] = None
    border_radius: BorderRadiusValue = None
    box_shadow: Union[None, BoxShadow, List[BoxShadow]] = None
    gradient: Optional[Gradient] = None
    shape: Optional[BoxShape] = None
    blend_mode: Optional[BlendMode] = None
