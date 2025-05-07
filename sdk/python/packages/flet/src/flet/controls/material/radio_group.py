from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.types import OptionalControlEventCallable

__all__ = ["RadioGroup"]


@control("RadioGroup")
class RadioGroup(Control):
    """
    Radio buttons let people select a single option from two or more choices.

    Online docs: https://flet.dev/docs/controls/radio
    """

    content: Control
    value: Optional[str] = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
