from typing import Optional

from flet.controls.control import Control, control

__all__ = ["AdaptiveControl"]


@control(kw_only=True)
class AdaptiveControl(Control):
    adaptive: Optional[bool] = None
