from typing import Optional

from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import control
from flet.controls.types import (
    LabelPosition,
    MouseCursor,
    OptionalColorValue,
    OptionalControlEventCallable,
)

__all__ = ["CupertinoRadio"]


@control("CupertinoRadio")
class CupertinoRadio(ConstrainedControl):
    """
    Radio buttons let people select a single option from two or more choices.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoradio
    """

    label: Optional[str] = None
    value: str = ""
    label_position: LabelPosition = LabelPosition.RIGHT
    fill_color: OptionalColorValue = None
    active_color: OptionalColorValue = None
    inactive_color: OptionalColorValue = None
    autofocus: bool = False
    use_checkmark_style: bool = False
    toggleable: bool = False
    focus_color: OptionalColorValue = None
    mouse_cursor: Optional[MouseCursor] = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
