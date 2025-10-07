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

    ```python
    ft.RadioGroup(
        value="option_2",
        content=ft.Column(
            intrinsic_width=True,
            controls=[
                ft.CupertinoRadio(value="option_1", label="Option 1"),
                ft.CupertinoRadio(value="option_2", label="Option 2"),
                ft.CupertinoRadio(value="option_3", label="Option 3"),
            ],
        ),
    )
    ```
    """

    label: Optional[str] = None
    """
    The clickable label to display on the right of this radio.
    """

    value: str = ""
    """
    The value to set to [`RadioGroup`][flet.] ancestor/parent when this radio
    is selected.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    The position of the label relative to this radio.
    """

    fill_color: Optional[ColorValue] = None
    """
    The color that fills this radio.
    """

    active_color: Optional[ColorValue] = Colors.PRIMARY
    """
    The color used to fill this radio when it is selected.
    """

    inactive_color: Optional[ColorValue] = None
    """
    The color used to fill this radio when it is not selected.
    """

    autofocus: bool = False
    """
    Whether this radio will be selected as the initial focus.

    If there is more than one control on a page with autofocus set, then the first
    one added to the page will get focus.
    """

    use_checkmark_style: bool = False
    """
    Whether the radio displays in a checkbox style instead of the default radio style.
    """

    toggleable: bool = False
    """
    Whether this radio button can return to an indeterminate state
    by selecting it again when already selected.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color for the radio's border when it has the input focus.
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
