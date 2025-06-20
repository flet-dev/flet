from typing import Optional

from flet.controls.base_control import control
from flet.controls.colors import Colors
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.types import ColorValue, Number, OptionalNumber

__all__ = ["Placeholder"]


@control("Placeholder")
class Placeholder(ConstrainedControl):
    """
    A placeholder box.

    Online docs: https://flet.dev/docs/controls/placeholder
    """

    content: Optional[Control] = None
    """
    An optional `Control` to display inside the placeholder.
    """

    color: ColorValue = Colors.BLUE_GREY_700
    """
    The [color](https://flet.dev/docs/reference/colors) of the placeholder box.
    """

    fallback_height: Number = 400.0
    """
    The height to use when the placeholder is in a situation with an unbounded height.

    Value is of `float` and defaults to `400.0`.
    """

    fallback_width: Number = 400.0
    """
    The width to use when the placeholder is in a situation with an unbounded width.

    Value is of `float` and defaults to `400.0`.
    """

    stroke_width: OptionalNumber = 2.0
    """
    The width of the lines in the placeholder box.

    Value is of `float` and defaults to `2.0`.
    """

