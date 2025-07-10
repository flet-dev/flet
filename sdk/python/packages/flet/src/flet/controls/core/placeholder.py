from typing import Optional

from flet.controls.base_control import control
from flet.controls.colors import Colors
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.types import ColorValue, Number

__all__ = ["Placeholder"]


@control("Placeholder")
class Placeholder(ConstrainedControl):
    """
    A placeholder box.
    """

    content: Optional[Control] = None
    """
    An optional `Control` to display inside the placeholder.
    """

    color: ColorValue = Colors.BLUE_GREY_700
    """
    The color of the placeholder box.
    """

    fallback_height: Number = 400.0
    """
    The height to use when the placeholder is in a situation with an unbounded height.
    """

    fallback_width: Number = 400.0
    """
    The width to use when the placeholder is in a situation with an unbounded width.
    """

    stroke_width: Optional[Number] = 2.0
    """
    The width of the lines in the placeholder box.
    """
