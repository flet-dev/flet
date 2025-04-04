from typing import Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import control
from flet.core.types import OptionalColorValue, OptionalNumber

__all__ = ["CupertinoActivityIndicator"]


@control("CupertinoActivityIndicator")
class CupertinoActivityIndicator(ConstrainedControl):
    """
    An iOS-style activity indicator that spins clockwise.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoactivityindicator
    """

    radius: OptionalNumber = None
    color: OptionalColorValue = None
    animating: Optional[bool] = None
