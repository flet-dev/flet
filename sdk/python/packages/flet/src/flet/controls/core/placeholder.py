from typing import Optional

from flet.controls.colors import Colors
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.types import ColorValue, Number, OptionalNumber

__all__ = ["Placeholder"]


@control("Placeholder")
class Placeholder(ConstrainedControl):
    """
    A placeholder box.

    -----

    Online docs: https://flet.dev/docs/controls/placeholder
    """

    content: Optional[Control] = None
    color: ColorValue = Colors.BLUE_GREY_700
    fallback_height: Number = 400.0
    fallback_width: Number = 400.0
    stroke_width: OptionalNumber = 2.0
