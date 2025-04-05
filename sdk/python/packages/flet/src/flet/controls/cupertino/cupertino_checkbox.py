from typing import Optional

from flet.controls.border import BorderSide
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import (
    ColorValue,
    ControlStateValue,
    LabelPosition,
    MouseCursor,
    OptionalColorValue,
    OptionalControlEventCallable,
)

__all__ = ["CupertinoCheckbox"]


class CupertinoCheckbox(ConstrainedControl):
    """
    A macOS style checkbox. Checkbox allows to select one or more items from a group, or switch between two mutually exclusive options (checked or unchecked, on or off).

    Example:
    ```
    import flet as ft

    def main(page):
        c = ft.CupertinoCheckbox(
            label="Cupertino Checkbox",
            active_color=ft.colors.GREEN,
            inactive_color=ft.colors.RED,
            check_color=ft.colors.BLUE,
        ),
        page.add(c)

    ft.app(target=main)
    ```

    -----
    Online docs: https://flet.dev/docs/controls/cupertinocheckbox
    """

    label: Optional[str] = None
    label_position: Optional[LabelPosition] = None
    value: Optional[bool] = None
    tristate: Optional[bool] = None
    autofocus: Optional[bool] = None
    check_color: OptionalColorValue = None
    active_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    fill_color: ControlStateValue[ColorValue] = None
    shape: Optional[OutlinedBorder] = None
    mouse_cursor: Optional[MouseCursor] = None
    semantics_label: Optional[str] = None
    border_side: ControlStateValue[BorderSide] = None
    on_change: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    # def before_update(self):
    #     super().before_update()
    #     self._set_attr_json("borderSide", self.__border_side, wrap_attr_dict=True)
    #     self._set_attr_json("fillColor", self.__fill_color, wrap_attr_dict=True)
