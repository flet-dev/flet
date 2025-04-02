from dataclasses import field
from typing import Optional

from flet.core.colors import Colors
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import ColorValue, Number, OptionalNumber

__all__ = ["Placeholder"]


@control("Placeholder")
class Placeholder(ConstrainedControl):
    """
    A placeholder box.

    -----

    Online docs: https://flet.dev/docs/controls/placeholder
    """

    content: Optional[Control] = None
    color: ColorValue = field(default=Colors.BLUE_GREY_700)
    fallback_height: Number = field(default=400.0)
    fallback_width: Number = field(default=400.0)
    stroke_width: OptionalNumber = field(default=2.0)
