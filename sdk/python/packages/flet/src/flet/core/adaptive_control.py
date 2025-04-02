from typing import Optional

from flet.core.control import Control, control

__all__ = ["AdaptiveControl"]


@control(kw_only=True)
class AdaptiveControl(Control):
    adaptive: Optional[bool] = None
