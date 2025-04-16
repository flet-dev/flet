from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control

__all__ = ["AdaptiveControl"]


@control(kw_only=True)
class AdaptiveControl(Control):
    adaptive: Optional[bool] = None
