from typing import Optional

from flet.controls.base_control import control
from flet.controls.colors import Colors
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ColorValue,
    LabelPosition,
    MouseCursor,
)

__all__ = ["CupertinoRadio"]


@control("CupertinoRadio")
class CupertinoRadio(LayoutControl):
    """
    A macOS-styled radio button, allowing the user to select a single option from two
    or more choices.
    """

    label: Optional[str] = None
    """
    The clickable label to display on the right of a Radio.
    """

    value: str = ""
    """
    The value to set to [`RadioGroup`][flet.RadioGroup] ancestor/parent when the radio
    is selected.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    The position of the label relative to the radio.
    """

    fill_color: Optional[ColorValue] = None
    """
    The color that fills the radio.
    """

    active_color: Optional[ColorValue] = Colors.PRIMARY
    """
    The color used to fill this radio
    when it is selected.
    """

    inactive_color: Optional[ColorValue] = None
    """
    The color used to fill this radio
    when it is not selected.
    """

    autofocus: bool = False
    """
    Whether this radio will be selected as the initial focus.

    If there is more than one control on a page with autofocus set, then the first
    one added to the page will get focus.
    """

    use_checkmark_style: bool = False
    """
    Whether the radio displays in a checkbox style or the default radio style.
    """

    toggleable: bool = False
    """
    Set to `True` if this radio button is allowed to be returned to an indeterminate
    state by selecting it again when selected.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color for the radio's border
    when it has the input focus.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor for a mouse pointer when it enters or is hovering over this radio.
    """

    on_focus: Optional[ControlEventHandler["CupertinoRadio"]] = None
    """
    Called when this radio has received focus.
    """

    on_blur: Optional[ControlEventHandler["CupertinoRadio"]] = None
    """
    Called when this radio has lost focus.
    """
