from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control

__all__ = ["TransparentPointer"]


@control("TransparentPointer")
class TransparentPointer(ConstrainedControl):
    content: Optional[Control] = None
