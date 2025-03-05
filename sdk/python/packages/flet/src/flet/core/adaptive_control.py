from typing import Optional

from flet.core.control import Control, control


@control(kw_only=True)
class AdaptiveControl(Control):
    adaptive: Optional[bool] = None
