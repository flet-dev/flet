from typing import Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber, control
from flet.core.types import ColorValue


@control("CupertinoActivityIndicator")
class CupertinoActivityIndicator(ConstrainedControl):
    """
    An iOS-style activity indicator that spins clockwise.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoactivityindicator
    """

    radius: OptionalNumber = None
    color: Optional[ColorValue] = None
    animating: Optional[bool] = None
