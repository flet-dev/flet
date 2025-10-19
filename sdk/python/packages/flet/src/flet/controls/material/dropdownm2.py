from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.material.form_field_control import FormFieldControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    Number,
)

__all__ = ["DropdownM2", "Option"]


@control("Option")
class Option(Control):
    """
    Represents an item in a dropdown. Either `key` or `text` must be specified, else a
    `ValueError` will be raised.
    """

    key: Optional[str] = None
    """
    Option's key. If not specified `text` will be used as fallback.
    """

    text: Optional[str] = None
    """
    Option's display text. If not specified `key` will be used as fallback.
    """

    content: Optional[Control] = None
    """
    A `Control` to display in this option. If not specified, `text` will be used as
    fallback, else `text` will be ignored.
    """

    alignment: Optional[Alignment] = None
    """
    Defines the alignment of this option in it's container.

    Defaults to `Alignment.center_left()`.
    """

    text_style: Optional[TextStyle] = None
    """
    Defines the style of the `text`.
    """

    on_click: Optional[ControlEventHandler["Option"]] = None
    """
    Called when this option is clicked.
    """

    def before_update(self):
        super().before_update()
        if self.key is None and self.text is None:
            raise ValueError("key or text must be specified")


@control("DropdownM2")
class DropdownM2(FormFieldControl):
    """
    A dropdown lets the user select from a number of items. The dropdown shows the
    currently selected item as well as an arrow that opens a menu for selecting another
    item.

    ```python
    ft.DropdownM2(
        width=220,
        value="Alice",
        options=[
            ft.dropdownm2.Option(key="Alice", text="Alice"),
            ft.dropdownm2.Option(key="Bob", text="Bob"),
        ],
    )
    ```
    """

    value: Optional[str] = None
    """
    `key` value of the selected option.
    """

    options: Optional[list[Option]] = None
    """
    A list of `Option` controls representing items in this dropdown.
    """

    alignment: Optional[Alignment] = None
    """
    Defines how the `hint` or the selected item is positioned within this dropdown.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than
    one control on a page with autofocus set, then the first one added to the page will
    get focus.
    """

    hint_content: Optional[Control] = None
    """
    A placeholder `Control` for the dropdown's value that is displayed when `value` is
    `None`.
    """

    select_icon: Optional[IconDataOrControl] = None
    """
    The [name of the icon](https://flet.dev/docs/reference/icons) or `Control` to use
    for the drop-down select button's icon.

    Defaults to `Icon(ft.Icons.ARROW_DROP_DOWN)`.
    """

    elevation: Number = 8
    """
    The dropdown's elevation.
    """

    item_height: Optional[Number] = None
    """
    The height of the items/options in the dropdown menu.
    """

    max_menu_height: Optional[Number] = None
    """
    The maximum height of the dropdown menu.
    """

    select_icon_size: Number = 24.0
    """
    The size of the icon button which wraps `select_icon`.
    """

    enable_feedback: Optional[bool] = None
    """
    Whether detected gestures should provide acoustic and/or haptic feedback. On
    Android, for example, setting this to `True` produce a click sound and a long-press
    will produce a short vibration.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding around the visible portion of this dropdown.
    """

    select_icon_enabled_color: Optional[ColorValue] = None
    """
    The color of any `Icon` descendant of `select_icon` if this button is enabled.
    """

    select_icon_disabled_color: Optional[ColorValue] = None
    """
    The color of any `Icon` descendant of `select_icon` if this button is disabled.
    """

    options_fill_horizontally: bool = True
    """
    Whether the dropdown's inner contents to horizontally fill its parent.
    By default this button's inner width is the minimum size of its content.

    If `True`, the inner width is expanded to fill its surrounding container.
    """

    disabled_hint_content: Optional[Control] = None
    """
    A placeholder `Control` for the dropdown's value that is displayed when `value` is
    `None` and the dropdown is disabled.
    """

    on_change: Optional[ControlEventHandler["DropdownM2"]] = None
    """
    Called when the selected item of this dropdown has changed.
    """

    on_focus: Optional[ControlEventHandler["DropdownM2"]] = None
    """
    Called when the control has received focus.
    """

    on_blur: Optional[ControlEventHandler["DropdownM2"]] = None
    """
    Called when the control has lost focus.
    """

    on_click: Optional[ControlEventHandler["DropdownM2"]] = None
    """
    Called when this dropdown is clicked.
    """

    def before_update(self):
        super().before_update()
        if (
            self.bgcolor is not None
            or self.fill_color is not None
            or self.focused_bgcolor is not None
        ) and self.filled is None:
            self.filled = True  # required to display any of the above colors

    def __contains__(self, item):
        return item in self.options
