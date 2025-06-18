from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.types import (
    LabelPosition,
    MouseCursor,
    OptionalColorValue,
)

__all__ = ["CupertinoRadio"]


@control("CupertinoRadio")
class CupertinoRadio(ConstrainedControl):
    """
    Radio buttons let people select a single option from two or more choices.

    Online docs: https://flet.dev/docs/controls/cupertinoradio
    """

    label: Optional[str] = None
    """
    The clickable label to display on the right of a Radio.
    """

    value: str = ""
    """
    The value to set to containing `RadioGroup` when the radio is selected.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    The position of the label relative to the radio.

    Value is of type 
    [LabelPosition](https://flet.dev/docs/reference/types/labelposition) and 
    defaults to `LabelPosition.RIGHT`.
    """

    fill_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) that fills the radio.
    """

    active_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used to fill this radio 
    when it is selected.
    """

    inactive_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used to fill this radio 
    when it is not selected.

    Defaults to `colors.WHITE`.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus.

    If there is more than one control on a page with autofocus set, then the first 
    one added to the page will get focus.
    """

    use_checkmark_style: bool = False
    """
    Defines whether the radio displays in a checkbox style or the default radio style.

    Defaults to `False`.
    """

    toggleable: bool = False
    """
    Set to `True` if this radio button is allowed to be returned to an indeterminate 
    state by selecting it again when selected.

    Defaults to `False`.
    """

    focus_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) for the radio's border 
    when it has the input focus.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    TBD
    """

    on_focus: OptionalControlEventHandler["CupertinoRadio"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["CupertinoRadio"] = None
    """
    Fires when the control has lost focus.
    """
