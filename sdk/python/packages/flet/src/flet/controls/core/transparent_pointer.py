from typing import Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control

__all__ = ["TransparentPointer"]


@control("TransparentPointer")
class TransparentPointer(ConstrainedControl):
    content: Optional[Control] = None
