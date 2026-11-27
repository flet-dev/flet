from typing import Annotated, Optional

from flet.controls.base_control import ClientWritable, control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.utils.validation import V

__all__ = ["RadioGroup"]


@control("RadioGroup", enabled_only=("change", "value"))
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

    Typically a list of :class:`~flet.Radio` controls nested in a container control,
    e.g. `Column`, `Row`.

    Raises:
        ValueError: If :attr:`content` is not visible.
    """

    value: Annotated[Optional[str], ClientWritable] = None
    """
    Current value of the RadioGroup.
    """

    on_change: Optional[ControlEventHandler["RadioGroup"]] = None
    """
    Called when the state of the RadioGroup is changed.
    """
