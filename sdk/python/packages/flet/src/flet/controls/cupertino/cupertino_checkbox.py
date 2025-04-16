from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.types import (
    ColorValue,
    LabelPosition,
    MouseCursor,
    OptionalColorValue,
    OptionalControlEventCallable,
)

__all__ = ["CupertinoCheckbox"]


@control("CupertinoCheckbox")
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
    label_position: LabelPosition = LabelPosition.RIGHT
    value: Optional[bool] = None
    tristate: bool = True
    autofocus: bool = False
    check_color: OptionalColorValue = None
    active_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    fill_color: OptionalControlStateValue[ColorValue] = None
    shape: Optional[OutlinedBorder] = None
    mouse_cursor: Optional[MouseCursor] = None
    semantics_label: Optional[str] = None
    border_side: OptionalControlStateValue[BorderSide] = None
    on_change: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
