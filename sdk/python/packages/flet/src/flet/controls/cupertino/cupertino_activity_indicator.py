from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import ColorValue, Number

__all__ = ["CupertinoActivityIndicator"]


@control("CupertinoActivityIndicator")
class CupertinoActivityIndicator(ConstrainedControl):
    """
    An iOS-style activity indicator that spins clockwise.

    Raises:
        ValueError: If `radius` is not strictly greater than 0.
    """

    radius: Number = 10
    """
    The radius of the activity indicator.

    Note:
        Must be strictly greater than 0.
    """

    color: Optional[ColorValue] = None
    """
    Defines the color of the activity
    indicator.
    """

    animating: bool = True
    """
    Whether the activity indicator is running its animation.
    """

    def before_update(self):
        super().before_update()
        assert self.radius > 0.0, (
            f"radius must be strictly greater than 0.0, got {self.radius}"
        )
