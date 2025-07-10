from typing import Optional

from flet.controls.base_control import control
from flet.controls.box import BoxShadowValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import BlendMode, ColorValue, IconValue, Number

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

    name: IconValue
    """
    The name of the icon.

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
    [`IconButton.icon_size`][flet.IconButton.icon_size] instead, so that the `IconButton` can make the splash
    area the appropriate size as well. The `IconButton` uses an [`IconTheme`][flet.IconTheme] to
    pass down the size to the `Icon`.
    """

    semantics_label: Optional[str] = None
    """
    The semantics label for this icon.

    It is not shown to the in the UI, but is announced in accessibility modes
    (e.g. TalkBack/VoiceOver).
    """

    shadows: Optional[BoxShadowValue] = None
    """
    TBD
    """

    fill: Optional[Number] = None
    """
    TBD
    """

    apply_text_scaling: Optional[bool] = None
    """
    TBD
    """

    grade: Optional[Number] = None
    """
    TBD
    """

    weight: Optional[Number] = None
    """
    TBD
    """

    optical_size: Optional[Number] = None
    """
    TBD
    """

    blend_mode: Optional[BlendMode] = None
    """
    TBD
    """

    def before_update(self):
        super().before_update()
        assert self.fill is None or (
            0.0 <= self.fill <= 1.0
        ), f"fill must be between 0.0 and 1.0 inclusive, got {self.fill}"
        assert self.weight is None or (
            self.weight > 0.0
        ), f"weight must be strictly greater than 0.0, got {self.weight}"
        assert self.optical_size is None or (
            self.optical_size > 0.0
        ), f"optical_size must be strictly greater than 0.0, got {self.optical_size}"
