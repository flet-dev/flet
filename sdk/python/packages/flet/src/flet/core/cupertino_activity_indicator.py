from flet.core.constrained_control import ConstrainedControl
from flet.core.control import control
from flet.core.types import Number, OptionalColorValue

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
