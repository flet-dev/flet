from numbers import Number
from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    ClipBehavior,
    NotchShape,
    OptionalColorValue,
    OptionalNumber,
)

__all__ = ["BottomAppBar"]


@control("BottomAppBar")
class BottomAppBar(ConstrainedControl):
    """
    A material design bottom app bar.

    Online docs: https://flet.dev/docs/controls/bottomappbar
    """

    content: Optional[Control] = None
    """
    A child Control contained by the BottomAppBar.
    """

    surface_tint_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used as an overlay on `bgcolor` 
    to indicate elevation.

    If this is `None`, no overlay will be applied. Otherwise this color will be 
    composited on top of `bgcolor` with an opacity related to `elevation` and used to 
    paint the BottomAppBar's background.

    Defaults to `None`.
    """

    bgcolor: OptionalColorValue = None
    """
    The fill [color](https://flet.dev/docs/reference/colors) to use for the 
    BottomAppBar. Default color is defined by current theme.
    """

    shadow_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the shadow below the 
    BottomAppBar.
    """

    padding: OptionalPaddingValue = None
    """
    Empty space to inscribe inside a container decoration (background, border). Padding 
    is an instance of [`Padding`](https://flet.dev/docs/reference/types/padding) class.

    Defaults to `padding.symmetric(vertical=12.0, horizontal=16.0)`.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    The content will be clipped (or not) according to this option.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior) 
    and defaults to `ClipBehavior.NONE`.
    """

    shape: Optional[NotchShape] = None
    """
    The notch that is made for the floating action button.

    Value is of type [`NotchShape`](https://flet.dev/docs/reference/types/notchshape).
    """

    notch_margin: Number = 4.0
    """
    The margin between the `FloatingActionButton` and the BottomAppBar's notch.

    Can be visible only if `shape=None`.
    """

    elevation: OptionalNumber = None
    """
    This property controls the size of the shadow below the BottomAppBar.
    """

    def before_update(self):
        super().before_update()
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
