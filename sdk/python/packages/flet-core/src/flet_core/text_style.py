import dataclasses
from dataclasses import field
from enum import Enum, IntFlag
from typing import List, Optional, Union

from flet_core.control import OptionalNumber
from flet_core.painting import Paint
from flet_core.shadow import BoxShadow
from flet_core.types import FontWeight


class TextDecoration(IntFlag):
    NONE = 0
    UNDERLINE = 1
    OVERLINE = 2
    LINE_THROUGH = 4


class TextDecorationStyle(Enum):
    SOLID = "solid"
    DOUBLE = "double"
    DOTTED = "dotted"
    DASHED = "dashed"
    WAVY = "wavy"


@dataclasses.dataclass
class TextStyle:
    size: Union[None, int, float] = field(default=None)
    weight: Optional[FontWeight] = field(default=None)
    italic: Optional[bool] = field(default=None)
    decoration: Optional[TextDecoration] = field(default=None)
    decoration_color: Optional[str] = field(default=None)
    decoration_thickness: OptionalNumber = field(default=None)
    decoration_style: Optional[TextDecorationStyle] = field(default=None)
    font_family: Optional[str] = field(default=None)
    color: Optional[str] = field(default=None)
    bgcolor: Optional[str] = field(default=None)
    shadow: Union[None, BoxShadow, List[BoxShadow]] = field(default=None)
    foreground: Optional[Paint] = field(default=None)
