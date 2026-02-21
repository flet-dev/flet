from typing import Annotated, Optional

from flet.controls._validation import V
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler

__all__ = ["RadioGroup"]


@control("RadioGroup")
class RadioGroup(Control):
    """
    Radio buttons let people select a single option from two or more choices.
    """

    content: Annotated[
        Control,
        V.visible_control(),
    ]
    """
    The content of the RadioGroup.

    Typically a list of `Radio` controls nested in a container control, e.g. `Column`,
    `Row`.

    Raises:
        ValueError: If [`content`][(c).] is not visible.
    """

    value: Optional[str] = None
    """
    Current value of the RadioGroup.
    """

    on_change: Optional[ControlEventHandler["RadioGroup"]] = None
    """
    Called when the state of the RadioGroup is changed.
    """
