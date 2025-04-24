from typing import List, Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.material.form_field_control import FormFieldControl
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    IconValueOrControl,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["DropdownM2", "Option"]


@control("Option")
class Option(Control):
    """
    Represents an item in a dropdown. Either `key` or `text` must be specified, else an `AssertionError` will be raised.
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
    A `Control` to display in this option. If not specified, `text` will be used as fallback, else `text` will be ignored.
    """

    alignment: Optional[Alignment] = None
    """
    Defines the alignment of this option in it's container.

    Value is of type [`Alignment`](https://flet.dev/docs/reference/types/alignment) and defaults to `alignment.center_left`.
    """

    text_style: Optional[TextStyle] = None
    """
    Defines the style of the `text`.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    on_click: OptionalControlEventCallable = None
    """
    Fires when this option is clicked.
    """

    def before_update(self):
        super().before_update()
        assert (
            self.key is not None or self.text is not None
        ), "key or text must be specified"


@control("DropdownM2")
class DropdownM2(FormFieldControl):
    """
    A dropdown lets the user select from a number of items. The dropdown shows the currently selected item as well as an arrow that opens a menu for selecting another item.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def button_clicked(e):
            t.value = f"Dropdown value is:  {dd.value}"
            page.update()

        t = ft.Text()
        b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
        dd = ft.DropdownM2(
            width=200,
            options=[
                ft.dropdown.Option("Red"),
                ft.dropdown.Option("Green"),
                ft.dropdown.Option("Blue"),
            ],
        )
        page.add(dd, b, t)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/dropdown
    """

    value: Optional[str] = None
    options: Optional[List[Option]] = None
    alignment: Optional[Alignment] = None
    autofocus: bool = False
    hint_content: Optional[Control] = None
    select_icon: Optional[IconValueOrControl] = None
    elevation: Number = 8
    item_height: OptionalNumber = None
    max_menu_height: OptionalNumber = None
    select_icon_size: Number = 24.0
    enable_feedback: Optional[bool] = None
    padding: OptionalPaddingValue = None
    select_icon_enabled_color: OptionalColorValue = None
    select_icon_disabled_color: OptionalColorValue = None
    options_fill_horizontally: bool = True
    disabled_hint_content: Optional[Control] = None
    on_change: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
    on_click: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        if (
            (
                self.bgcolor is not None
                or self.fill_color is not None
                or self.focused_bgcolor is not None
            )
        ) and self.filled is None:
            self.filled = True  # required to display any of the above colors

    def __contains__(self, item):
        return item in self.options
