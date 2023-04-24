from typing import Any, Optional

from flet_core.control import Control


class InlineSpan(Control):
    def __init__(
        self,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)
