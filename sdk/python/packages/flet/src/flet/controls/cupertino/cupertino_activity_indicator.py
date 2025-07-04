from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import ColorValue, Number

__all__ = ["CupertinoActivityIndicator"]


@control("CupertinoActivityIndicator")
class CupertinoActivityIndicator(ConstrainedControl):
    """
    An iOS-style activity indicator that spins clockwise.
    """

    radius: Number = 10
    """
    The radius of the activity indicator.
    """

    color: Optional[ColorValue] = None
    """
    Defines the [color](https://flet.dev/docs/reference/colors) of the activity
    indicator.
    """

    animating: bool = True
    """
    Whether the activity indicator is running its animation.
    """
