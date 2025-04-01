from typing import Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber, control
from flet.core.types import ClipBehavior, ColorValue, NotchShape, PaddingValue


@control("BottomAppBar")
class BottomAppBar(ConstrainedControl):
    """
    A material design bottom app bar.

    -----

    Online docs: https://flet.dev/docs/controls/bottomappbar
    """

    content: Optional[Control] = None
    surface_tint_color: Optional[ColorValue] = None
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    padding: Optional[PaddingValue] = None
    clip_behavior: Optional[ClipBehavior] = None
    shape: Optional[NotchShape] = None
    notch_margin: OptionalNumber = None
    elevation: OptionalNumber = None

    def before_update(self):
        super().before_update()
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
