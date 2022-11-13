import dataclasses
import time
from typing import Any, Optional

from flet.callable_control import CallableControl
from flet.ref import Ref


class HapticFeedback(CallableControl):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        data: Any = None,
    ):

        CallableControl.__init__(
            self,
            ref=ref,
            data=data,
        )

    def _get_control_name(self):
        return "hapticfeedback"

    def _is_isolated(self):
        return True

    def heavy_impact(self):
        self._call_method("heavy_impact", [], wait_for_result=False)

    def light_impact(self):
        self._call_method("light_impact", [], wait_for_result=False)

    def medium_impact(self):
        self._call_method("medium_impact", [], wait_for_result=False)

    def vibrate(self):
        self._call_method("vibrate", [], wait_for_result=False)
