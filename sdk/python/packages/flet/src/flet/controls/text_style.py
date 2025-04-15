from dataclasses import dataclass
from enum import Enum, IntFlag
from typing import Optional

from flet.controls.box import ShadowValue
from flet.controls.painting import Paint
from flet.controls.types import FontWeight, OptionalColorValue, OptionalNumber

__all__ = [
    "TextOverflow",
    "TextBaseline",
    "TextThemeStyle",
    "TextDecoration",
    "TextDecorationStyle",
    "TextStyle",
    "StrutStyle",
    "OptionalTextStyle",
    "OptionalStrutStyle",
    "OptionalTextOverflow",
    "OptionalTextBaseline",
    "OptionalTextThemeStyle",
    "OptionalTextDecoration",
    "OptionalTextDecorationStyle",
]


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
    size: OptionalNumber = None
    height: OptionalNumber = None
    weight: Optional[FontWeight] = None
    italic: Optional[bool] = None
    decoration: Optional[TextDecoration] = None
    decoration_color: OptionalColorValue = None
    decoration_thickness: OptionalNumber = None
    decoration_style: "OptionalTextDecorationStyle" = None
    font_family: Optional[str] = None
    color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    shadow: Optional[ShadowValue] = None
    foreground: Optional[Paint] = None
    letter_spacing: OptionalNumber = None
    word_spacing: OptionalNumber = None
    overflow: Optional[TextOverflow] = None
    baseline: Optional[TextBaseline] = None


@dataclass
class StrutStyle:
    size: OptionalNumber = None
    height: OptionalNumber = None
    weight: Optional[FontWeight] = None
    italic: Optional[bool] = None
    font_family: Optional[str] = None
    leading: OptionalNumber = None
    force_strut_height: Optional[bool] = None


# Typing
OptionalTextStyle = Optional[TextStyle]
OptionalStrutStyle = Optional[StrutStyle]
OptionalTextOverflow = Optional[TextOverflow]
OptionalTextBaseline = Optional[TextBaseline]
OptionalTextThemeStyle = Optional[TextThemeStyle]
OptionalTextDecoration = Optional[TextDecoration]
OptionalTextDecorationStyle = Optional[TextDecorationStyle]
