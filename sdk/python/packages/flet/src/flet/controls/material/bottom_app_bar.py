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

    -----

    Online docs: https://flet.dev/docs/controls/bottomappbar
    """

    content: Optional[Control] = None
    surface_tint_color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    padding: OptionalPaddingValue = None
    clip_behavior: Optional[ClipBehavior] = None
    shape: Optional[NotchShape] = None
    notch_margin: OptionalNumber = None
    elevation: OptionalNumber = None

    def before_update(self):
        super().before_update()
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
