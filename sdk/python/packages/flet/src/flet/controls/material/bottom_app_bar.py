from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    NotchShape,
    Number,
)

__all__ = ["BottomAppBar"]


@control("BottomAppBar")
class BottomAppBar(LayoutControl):
    """
    A material design bottom app bar.

    Raises:
        ValueError: If [`elevation`][(c).] is negative.
    """

    content: Optional[Control] = None
    """
    The content of this bottom app bar.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The fill color to use for this app bar.

    Defaults to [`BottomAppBarTheme.bgcolor`][flet.], or if
    that is `None`, falls back to [`ColorScheme.surface`][flet.].
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color of the shadow below this app bar.
    """

    padding: Optional[PaddingValue] = None
    """
    Empty space to inscribe inside a container decoration (background, border).

    Defaults to [`BottomAppBarTheme.padding`][flet.], or if
    that is `None`, falls back to `Padding.symmetric(vertical=12.0, horizontal=16.0)`.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    Defines how the [`content`][(c).] of this app bar should be clipped.
    """

    shape: Optional[NotchShape] = None
    """
    The notch that is made for the floating action button.
    """

    notch_margin: Number = 4.0
    """
    The margin between the [`FloatingActionButton`][flet.] and this
    app bar's notch.

    Can be visible only if [`shape`][(c).] is `None`.
    """

    elevation: Optional[Number] = None
    """
    This property controls the size of the shadow below this app bar.
    """

    def before_update(self):
        super().before_update()
        if self.elevation is not None and self.elevation < 0:
            raise ValueError(
                f"elevation must be greater than or equal to 0, got {self.elevation}"
            )
