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
    """
    TBD
    """

    NONE = 0
    """
    Do not draw a decoration.
    """

    UNDERLINE = 1
    """
    Draw a line underneath each line of text.
    """

    OVERLINE = 2
    """
    Draw a line above each line of text.
    """

    LINE_THROUGH = 4
    """
    Draw a line through each line of text.
    """


class TextDecorationStyle(Enum):
    """
    TBD
    """

    SOLID = "solid"
    """
    Draw a solid line.
    """

    DOUBLE = "double"
    """
    Draw two lines.
    """

    DOTTED = "dotted"
    """
    Draw a dotted line.
    """

    DASHED = "dashed"
    """
    Draw a dashed line.
    """

    WAVY = "wavy"
    """
    Draw a sinusoidal line.
    """


@dataclass
class TextStyle:
    """
    A style describing how to format and paint text. It has the following properties:
    """

    size: OptionalNumber = None
    """
    The size of glyphs (in logical pixels) to use when painting the text.

    Defaults to `14`.
    """

    height: OptionalNumber = None
    """
    The height of this text span, as a multiple of the font size.

    See detailed explanation here:
    https://api.flutter.dev/flutter/painting/TextStyle/height.html
    """

    weight: Optional[FontWeight] = None
    """
    Value is of type https://flet.dev/docs/reference/types/fontweight and defaults to
    `FontWeight.NORMAL`.
    """

    italic: Optional[bool] = None
    """
    `True` to use italic typeface.
    """

    decoration: Optional[TextDecoration] = None
    """
    The decorations to paint near the text (e.g., an underline).

    Value is of type https://flet.dev/docs/reference/types/textdecoration.
    """

    decoration_color: OptionalColorValue = None
    """
    The https://flet.dev/docs/reference/colors in which to paint the text decorations.
    """

    decoration_thickness: OptionalNumber = None
    """
    The thickness of the decoration stroke as a multiplier of the thickness defined by
    the font.
    """

    decoration_style: "OptionalTextDecorationStyle" = None
    """
    The style in which to paint the text decorations (e.g., dashed).

    Value is of type https://flet.dev/docs/reference/types/textdecorationstyle and
    defaults to `TextDecorationStyle.SOLID`.
    """

    font_family: Optional[str] = None
    """
    See https://flet.dev/docs/controls/text#font_family.
    """

    color: OptionalColorValue = None
    """
    Text foreground https://flet.dev/docs/reference/colors.
    """

    bgcolor: OptionalColorValue = None
    """
    Text background https://flet.dev/docs/reference/colors.
    """

    shadow: Optional[ShadowValue] = None
    """
    The value of this property is a single instance or a list of
    https://flet.dev/docs/reference/types/boxshadow class instances.
    """

    foreground: Optional[Paint] = None
    """
    The paint drawn as a foreground for the text.

    Value is of type https://flet.dev/docs/reference/types/paint.
    """

    letter_spacing: OptionalNumber = None
    """
    The amount of space (in logical pixels) to add between each letter. A negative
    value can be used to bring the letters closer.
    """

    word_spacing: OptionalNumber = None
    """
    The amount of space (in logical pixels) to add at each sequence of white-space
    (i.e. between each word). A negative value can be used to bring the words closer.
    """

    overflow: Optional[TextOverflow] = None
    """
    How visual text overflow should be handled.

    Value is of type https://flet.dev/docs/reference/types/textoverflow.
    """

    baseline: Optional[TextBaseline] = None
    """
    The common baseline that should be aligned between this text span and its parent
    text span, or, for the root text spans, with the line box.

    Value is of type https://flet.dev/docs/reference/types/textbaseline.
    """


@dataclass
class StrutStyle:
    """
    TBD
    """

    size: OptionalNumber = None
    """
    The size of text (in logical pixels) to use when getting metrics from the font.

    Defaults to `14`.
    """

    height: OptionalNumber = None
    """
    The minimum height of the strut, as a multiple of `size`.

    See detailed explanation here:
    https://api.flutter.dev/flutter/painting/StrutStyle/height.html
    """

    weight: Optional[FontWeight] = None
    """
    The typeface thickness to use when calculating the strut.

    Value is of type https://flet.dev/docs/reference/types/fontweight and defaults to
    `FontWeight.W_400`.
    """

    italic: Optional[bool] = None
    """
    `True` to use italic typeface.

    Defaults to `False`.
    """

    font_family: Optional[str] = None
    """
    See https://flet.dev/docs/controls/text#font_family.
    """

    leading: OptionalNumber = None
    """
    The amount of additional space to place between lines when rendering text.

    Defaults to using the font-specified leading value.
    """

    force_strut_height: Optional[bool] = None
    """
    Whether the strut height should be forced.

    Defaults to `False`.
    """


# Typing
OptionalTextStyle = Optional[TextStyle]
OptionalStrutStyle = Optional[StrutStyle]
OptionalTextOverflow = Optional[TextOverflow]
OptionalTextBaseline = Optional[TextBaseline]
OptionalTextThemeStyle = Optional[TextThemeStyle]
OptionalTextDecoration = Optional[TextDecoration]
OptionalTextDecorationStyle = Optional[TextDecorationStyle]
