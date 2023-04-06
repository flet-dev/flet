import dataclasses
from dataclasses import field
from enum import Enum
from typing import Optional

from flet_core.types import OffsetValue


class ShadowBlurStyle(Enum):
    NORMAL = "normal"
    SOLID = "solid"
    OUTER = "outer"
    INNER = "inner"


@dataclasses.dataclass
class BoxShadow:
    spread_radius: Optional[float] = field(default=None)
    blur_radius: Optional[float] = field(default=None)
    color: Optional[str] = field(default=None)
    offset: OffsetValue = field(default=None)
    blur_style: ShadowBlurStyle = field(default=ShadowBlurStyle.NORMAL)
