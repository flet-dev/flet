from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler

__all__ = ["RadioGroup"]


@control("RadioGroup")
class RadioGroup(Control):
    """
    Radio buttons let people select a single option from two or more choices.

    Online docs: https://flet.dev/docs/controls/radio
    """

    content: Control
    """
    The content of the RadioGroup.

    Typically a list of `Radio` controls nested in a container control, e.g. `Column`,
    `Row`.
    """

    value: Optional[str] = None
    """
    Current value of the RadioGroup.
    """

    on_change: OptionalControlEventHandler["RadioGroup"] = None
    """
    Fires when the state of the RadioGroup is changed.
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
