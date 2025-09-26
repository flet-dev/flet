from dataclasses import dataclass
from enum import Enum, IntFlag
from typing import Optional

from flet.controls.box import BoxShadowValue
from flet.controls.painting import Paint
from flet.controls.types import ColorValue, FontWeight, Number

__all__ = [
    "StrutStyle",
    "TextBaseline",
    "TextDecoration",
    "TextDecorationStyle",
    "TextOverflow",
    "TextStyle",
    "TextThemeStyle",
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
    A linear decoration to draw near the text.
    """

    @classmethod
    def combine(cls, decorations: list["TextDecoration"]) -> "TextDecoration":
        """
        Creates a decoration that paints the union of all the given decorations.
        """
        result = cls.NONE
        for d in decorations:
            result |= d
        return result

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
    The style in which to draw a text decoration.
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
    A style describing how to format and paint text.
    """

    size: Optional[Number] = None
    """
    The size of glyphs (in logical pixels) to use when painting the text.

    Defaults to `14`.
    """

    height: Optional[Number] = None
    """
    The height of this text span, as a multiple of the font size.

    See detailed explanation
    [here](https://api.flutter.dev/flutter/painting/TextStyle/height.html).
    """

    weight: Optional[FontWeight] = None
    """
    The typeface thickness to use when painting the text (e.g., bold).

    Defaults to [`FontWeight.NORMAL`][flet.].
    """

    italic: bool = False
    """
    Whether to use italic typeface.
    """

    decoration: Optional[TextDecoration] = None
    """
    The decorations to paint near the text (e.g., an underline).
    """

    decoration_color: Optional[ColorValue] = None
    """
    The color in which to paint the text decorations.
    """

    decoration_thickness: Optional[Number] = None
    """
    The thickness of the decoration stroke as a multiplier of the thickness defined by
    the font.
    """

    decoration_style: Optional[TextDecorationStyle] = None
    """
    The style in which to paint the text decorations (e.g., dashed).

    Defaults to `TextDecorationStyle.SOLID`.
    """

    font_family: Optional[str] = None
    """
    See https://flet.dev/docs/controls/text#font_family.
    """

    color: Optional[ColorValue] = None
    """
    Text foreground https://flet.dev/docs/reference/colors.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Text background https://flet.dev/docs/reference/colors.
    """

    shadow: Optional[BoxShadowValue] = None
    """
    TBD
    """

    foreground: Optional[Paint] = None
    """
    The paint drawn as a foreground for the text.
    """

    letter_spacing: Optional[Number] = None
    """
    The amount of space (in logical pixels) to add between each letter. A negative
    value can be used to bring the letters closer.
    """

    word_spacing: Optional[Number] = None
    """
    The amount of space (in logical pixels) to add at each sequence of white-space
    (i.e. between each word). A negative value can be used to bring the words closer.
    """

    overflow: Optional[TextOverflow] = None
    """
    How visual text overflow should be handled.
    """

    baseline: Optional[TextBaseline] = None
    """
    The common baseline that should be aligned between this text span and its parent
    text span, or, for the root text spans, with the line box.
    """

    def copy(
        self,
        *,
        size: Optional[Number] = None,
        height: Optional[Number] = None,
        weight: Optional[FontWeight] = None,
        italic: Optional[bool] = None,
        decoration: Optional[TextDecoration] = None,
        decoration_color: Optional[ColorValue] = None,
        decoration_thickness: Optional[Number] = None,
        decoration_style: Optional[TextDecorationStyle] = None,
        font_family: Optional[str] = None,
        color: Optional[ColorValue] = None,
        bgcolor: Optional[ColorValue] = None,
        shadow: Optional[BoxShadowValue] = None,
        foreground: Optional[Paint] = None,
        letter_spacing: Optional[Number] = None,
        word_spacing: Optional[Number] = None,
        overflow: Optional[TextOverflow] = None,
        baseline: Optional[TextBaseline] = None,
    ):
        return TextStyle(
            size=size if size is not None else self.size,
            height=height if height is not None else self.height,
            weight=weight if weight is not None else self.weight,
            italic=italic if italic is not None else self.italic,
            decoration=decoration if decoration is not None else self.decoration,
            decoration_color=decoration_color
            if decoration_color is not None
            else self.decoration_color,
            decoration_thickness=decoration_thickness
            if decoration_thickness is not None
            else self.decoration_thickness,
            decoration_style=decoration_style
            if decoration_style is not None
            else self.decoration_style,
            font_family=font_family if font_family is not None else self.font_family,
            color=color if color is not None else self.color,
            bgcolor=bgcolor if bgcolor is not None else self.bgcolor,
            shadow=shadow if shadow is not None else self.shadow,
            foreground=foreground if foreground is not None else self.foreground,
            letter_spacing=letter_spacing
            if letter_spacing is not None
            else self.letter_spacing,
            word_spacing=word_spacing
            if word_spacing is not None
            else self.word_spacing,
            overflow=overflow if overflow is not None else self.overflow,
            baseline=baseline if baseline is not None else self.baseline,
        )


@dataclass
class StrutStyle:
    """
    TBD
    """

    size: Optional[Number] = None
    """
    The size of text (in logical pixels) to use when getting metrics from the font.

    Defaults to `14`.
    """

    height: Optional[Number] = None
    """
    The minimum height of the strut, as a multiple of `size`.

    See detailed explanation here:
    https://api.flutter.dev/flutter/painting/StrutStyle/height.html
    """

    weight: Optional[FontWeight] = None
    """
    The typeface thickness to use when calculating the strut.

    Defaults to `FontWeight.W_400`.
    """

    italic: bool = False
    """
    Whether to use italic typeface.
    """

    font_family: Optional[str] = None
    """
    See https://flet.dev/docs/controls/text#font_family.
    """

    leading: Optional[Number] = None
    """
    The amount of additional space to place between lines when rendering text.

    Defaults to using the font-specified leading value.
    """

    force_strut_height: Optional[bool] = None
    """
    Whether the strut height should be forced.

    Defaults to `False`.
    """

    def copy(
        self,
        *,
        size: Optional[Number] = None,
        height: Optional[Number] = None,
        weight: Optional[FontWeight] = None,
        italic: Optional[bool] = None,
        font_family: Optional[str] = None,
        leading: Optional[Number] = None,
        force_strut_height: Optional[bool] = None,
    ) -> "StrutStyle":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return StrutStyle(
            size=size if size is not None else self.size,
            height=height if height is not None else self.height,
            weight=weight if weight is not None else self.weight,
            italic=italic if italic is not None else self.italic,
            font_family=font_family if font_family is not None else self.font_family,
            leading=leading if leading is not None else self.leading,
            force_strut_height=force_strut_height
            if force_strut_height is not None
            else self.force_strut_height,
        )
