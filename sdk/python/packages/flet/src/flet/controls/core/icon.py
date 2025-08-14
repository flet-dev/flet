from typing import Optional

from flet.controls.base_control import control
from flet.controls.box import BoxShadowValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import BlendMode, ColorValue, IconData, Number

__all__ = ["Icon"]


@control("Icon")
class Icon(ConstrainedControl):
    """
    Displays a Material icon.

    Raises:
        AssertionError: If [`fill`][(c).] is less than `0.0` or greater than `1.0`.
        AssertionError: If [`weight`][(c).] is less than or equal to `0.0`.
        AssertionError: If [`optical_size`][(c).] is less than or equal to `0.0`.
    """

    icon: IconData
    """
    The icon to display.

    You can search through the list of all available icons using our
    [Icons browser](https://gallery.flet.dev/icons-browser/) app
    [written in Flet](https://github.com/flet-dev/examples/blob/main/python/apps/icons-browser/main.py).
    """

    color: Optional[ColorValue] = None
    """
    Icon color.
    """

    size: Optional[Number] = None
    """
    The icon's size.

    Icons occupy a square with width and height equal to `size`.

    Defaults to the nearest [`IconTheme.size`][flet.IconTheme.size].

    If this `Icon` is being placed inside an [`IconButton`][flet.IconButton], then use
    [`IconButton.icon_size`][flet.IconButton.icon_size] instead, so that the
    `IconButton` can make the splash area the appropriate size as well.
    The `IconButton` uses an [`IconTheme`][flet.IconTheme] to pass down the
    size to the `Icon`.
    """

    semantics_label: Optional[str] = None
    """
    The semantics label for this icon.

    It is not shown to the in the UI, but is announced in accessibility modes
    (e.g. TalkBack/VoiceOver).
    """

    shadows: Optional[BoxShadowValue] = None
    """
    A list of Shadows that will be painted underneath the icon.

    Multiple shadows are supported to replicate lighting from multiple light sources.

    Shadows must be in the same order for Icon to be considered as equivalent as order
    produces differing transparency.
    """

    fill: Optional[Number] = None
    """
    The fill for drawing the icon.

    Requires the underlying icon font to support the `FILL` FontVariation axis,
    otherwise has no effect. Variable font filenames often indicate the supported axes.
    Must be between `0.0` (unfilled) and `1.0` (filled), inclusive.

    Can be used to convey a state transition for animation or interaction.
    """

    apply_text_scaling: Optional[bool] = None
    """
    Whether to scale the size of this widget using the ambient MediaQuery's TextScaler.

    This is specially useful when you have an icon associated with a text,
    as scaling the text without scaling the icon would result in a confusing interface.
    """

    grade: Optional[Number] = None
    """
    The grade (granular stroke weight) for drawing the icon.

    Requires the underlying icon font to support the `GRAD` FontVariation axis,
    otherwise has no effect. Variable font filenames often indicate the supported axes.
    Can be negative.

    Grade and weight both affect a symbol's stroke weight (thickness),
    but grade has a smaller impact on the size of the symbol.

    Grade is also available in some text fonts. One can match grade levels between
    text and symbols for a harmonious visual effect. For example, if the text font
    has a -25 grade value, the symbols can match it with a suitable value, say -25.
    """

    weight: Optional[Number] = None
    """
    The stroke weight for drawing the icon.

    Requires the underlying icon font to support the `wght` FontVariation axis,
    otherwise has no effect. Variable font filenames often indicate the supported axes.
    Must be greater than `0`.
    """

    optical_size: Optional[Number] = None
    """
    The optical size for drawing the icon.

    Requires the underlying icon font to support the `opsz` FontVariation axis,
    otherwise has no effect. Variable font filenames often indicate the supported axes.
    Must be greater than `0`.

    For an icon to look the same at different sizes, the stroke weight (thickness)
    must change as the icon size scales. Optical size offers a way to automatically
    adjust the stroke weight as icon size changes.
    """

    blend_mode: Optional[BlendMode] = BlendMode.SRC_OVER
    """
    The BlendMode to apply to the foreground of the icon.
    """

    def before_update(self):
        super().before_update()
        assert self.fill is None or (0.0 <= self.fill <= 1.0), (
            f"fill must be between 0.0 and 1.0 inclusive, got {self.fill}"
        )
        assert self.weight is None or (self.weight > 0.0), (
            f"weight must be strictly greater than 0.0, got {self.weight}"
        )
        assert self.optical_size is None or (self.optical_size > 0.0), (
            f"optical_size must be strictly greater than 0.0, got {self.optical_size}"
        )
