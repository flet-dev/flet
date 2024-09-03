from typing import Optional

from flet_core.control import Control


class AdaptiveControl(Control):
    def __init__(self, adaptive: Optional[bool] = None):
        self.adaptive = adaptive

    # adaptive
    @property
    def adaptive(self) -> bool:
        return self._get_attr("adaptive", data_type="bool", def_value=False)

    @adaptive.setter
    def adaptive(self, value: Optional[bool]):
        self._set_attr("adaptive", value)
