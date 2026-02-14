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
    """
    How overflowing text should be handled.
    """

    CLIP = "clip"
    """
    Clip the overflowing text to fix its container.
    """

    ELLIPSIS = "ellipsis"
    """
    Use an ellipsis to indicate that the text has overflowed.
    """

    FADE = "fade"
    """
    Fade the overflowing text to transparent.
    """

    VISIBLE = "visible"
    """
    Render overflowing text outside of its container.
    """


class TextBaseline(Enum):
    """A horizontal line used for aligning text."""

    ALPHABETIC = "alphabetic"
    """
    The horizontal line used to align the bottom of glyphs for alphabetic characters.
    """

    IDEOGRAPHIC = "ideographic"
    """
    The horizontal line used to align ideographic characters.
    """


class TextThemeStyle(Enum):
    """
    Predefined Material text style roles from the active theme.

    Use these values with properties such as [`Text.theme_style`][flet.]
    to reference semantic typography slots (display, headline, title, body, label)
    instead of hard-coding font metrics in each control.
    """

    DISPLAY_LARGE = "displayLarge"
    """
    Largest display style.

    Intended for very prominent, short text on large surfaces, such as hero headlines.
    """

    DISPLAY_MEDIUM = "displayMedium"
    """
    Medium display style.

    Intended for high-impact short text when [`DISPLAY_LARGE`][(c).] is too dominant.
    """

    DISPLAY_SMALL = "displaySmall"
    """
    Smallest display style.

    Intended for concise, emphasized text that still needs display-level prominence.
    """

    HEADLINE_LARGE = "headlineLarge"
    """
    Largest headline style.

    Headline styles are below display styles and suit short, high-emphasis headings.
    """

    HEADLINE_MEDIUM = "headlineMedium"
    """
    Medium headline style.

    Suitable for section headers and prominent in-content headings.
    """

    HEADLINE_SMALL = "headlineSmall"
    """
    Smallest headline style.

    Suitable for compact headline usage on dense layouts.
    """

    TITLE_LARGE = "titleLarge"
    """
    Largest title style.

    Titles are typically used for medium-emphasis, short text such as card titles.
    """

    TITLE_MEDIUM = "titleMedium"
    """
    Medium title style.

    Suitable for secondary titles and emphasized labels in structured content.
    """

    TITLE_SMALL = "titleSmall"
    """
    Smallest title style.

    Suitable for compact title text where space is limited.
    """

    LABEL_LARGE = "labelLarge"
    """
    Largest label style.

    Commonly used for component text, such as button labels and prominent captions.
    """

    LABEL_MEDIUM = "labelMedium"
    """
    Medium label style.

    Suitable for compact UI labels in controls and supporting interface text.
    """

    LABEL_SMALL = "labelSmall"
    """
    Smallest label style.

    Suitable for dense, low-footprint labels and small supporting annotations.
    """

    BODY_LARGE = "bodyLarge"
    """
    Largest body style.

    Body styles are intended for longer passages and primary reading content.
    """

    BODY_MEDIUM = "bodyMedium"
    """
    Medium body style.

    Common default style for standard paragraph text in Material-themed UIs.
    """

    BODY_SMALL = "bodySmall"
    """
    Smallest body style.

    Suitable for secondary body text, footnotes, and compact long-form content.
    """


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
    The thickness of the decoration stroke as a multiplier of the thickness defined by \
    the font.
    """

    decoration_style: Optional[TextDecorationStyle] = None
    """
    The style in which to paint the text decorations (e.g., dashed).

    Defaults to `TextDecorationStyle.SOLID`.
    """

    font_family: Optional[str] = None
    """
    See https://docs.flet.dev/controls/text#font_family.
    """

    color: Optional[ColorValue] = None
    """
    Text foreground https://docs.flet.dev/types/colors.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Text background https://docs.flet.dev/types/colors.
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
    The amount of space (in logical pixels) to add between each letter. A negative \
    value can be used to bring the letters closer.
    """

    word_spacing: Optional[Number] = None
    """
    The amount of space (in logical pixels) to add at each sequence of white-space \
    (i.e. between each word). A negative value can be used to bring the words closer.
    """

    overflow: Optional[TextOverflow] = None
    """
    How visual text overflow should be handled.
    """

    baseline: Optional[TextBaseline] = None
    """
    The common baseline that should be aligned between this text span and its parent \
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
        """
        Returns a copy of this object with the specified properties overridden.
        """
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
    The minimum height of the strut, as a multiple of [`size`][(c).].

    See detailed explanation here:
    https://api.flutter.dev/flutter/painting/StrutStyle/height.html
    """

    weight: Optional[FontWeight] = None
    """
    The typeface thickness to use when calculating the strut.

    Defaults to [`FontWeight.W_400`][flet.].
    """

    italic: bool = False
    """
    Whether to use italic typeface.
    """

    font_family: Optional[str] = None
    """
    See [`Text.font_family`][flet.].
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
