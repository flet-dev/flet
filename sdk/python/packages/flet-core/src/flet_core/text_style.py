from dataclasses import dataclass, field
from enum import Enum, IntFlag
from typing import List, Optional, Union

from flet_core.box import BoxShadow
from flet_core.painting import Paint
from flet_core.types import FontWeight, OptionalNumber


class TextOverflow(Enum):
    CLIP = "clip"
    ELLIPSIS = "ellipsis"
    FADE = "fade"
    VISIBLE = "visible"


class TextBaseline(Enum):
    ALPHABETIC = "alphabetic"
    IDEOGRAPHIC = "ideographic"


class TextThemeStyle(Enum):
    DISPLAY_LARGE = "displayLarge"
    DISPLAY_MEDIUM = "displayMedium"
    DISPLAY_SMALL = "displaySmall"
    HEADLINE_LARGE = "headlineLarge"
    HEADLINE_MEDIUM = "headlineMedium"
    HEADLINE_SMALL = "headlineSmall"
    TITLE_LARGE = "titleLarge"
    TITLE_MEDIUM = "titleMedium"
    TITLE_SMALL = "titleSmall"
    LABEL_LARGE = "labelLarge"
    LABEL_MEDIUM = "labelMedium"
    LABEL_SMALL = "labelSmall"
    BODY_LARGE = "bodyLarge"
    BODY_MEDIUM = "bodyMedium"
    BODY_SMALL = "bodySmall"


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


@dataclass
class TextStyle:
    size: OptionalNumber = field(default=None)
    height: OptionalNumber = field(default=None)
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
    letter_spacing: OptionalNumber = field(default=None)
    word_spacing: OptionalNumber = field(default=None)
    overflow: Optional[TextOverflow] = field(default=None)
    baseline: Optional[TextBaseline] = field(default=None)
