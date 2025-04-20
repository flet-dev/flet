from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import Number, OptionalColorValue

__all__ = ["CupertinoActivityIndicator"]


@control("CupertinoActivityIndicator")
class CupertinoActivityIndicator(ConstrainedControl):
    """
    An iOS-style activity indicator that spins clockwise.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoactivityindicator
    """

    radius: Number = 10
    color: OptionalColorValue = None
    animating: bool = True
