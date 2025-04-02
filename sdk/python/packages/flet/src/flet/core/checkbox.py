from typing import Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.border import BorderSide
from flet.core.buttons import OutlinedBorder
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import control
from flet.core.text_style import TextStyle
from flet.core.types import (
    ColorValue,
    ControlStateValue,
    LabelPosition,
    MouseCursor,
    OptionalControlEventCallable,
    OptionalNumber,
    VisualDensity,
)

__all__ = ["Checkbox"]


@control("Checkbox")
class Checkbox(ConstrainedControl, AdaptiveControl):
    """
    Checkbox allows to select one or more items from a group, or switch between two mutually exclusive options (checked or unchecked, on or off).

    Example:
    ```
    import flet as ft

    def main(page):
        def button_clicked(e):
            t.value = (
                f"Checkboxes values are:  {c1.value}, {c2.value}, {c3.value}, {c4.value}, {c5.value}."
            )
            page.update()

        t = ft.Text()
        c1 = ft.Checkbox(label="Unchecked by default checkbox", value=False)
        c2 = ft.Checkbox(label="Undefined by default tristate checkbox", tristate=True)
        c3 = ft.Checkbox(label="Checked by default checkbox", value=True)
        c4 = ft.Checkbox(label="Disabled checkbox", disabled=True)
        c5 = ft.Checkbox(
            label="Checkbox with rendered label_position='left'", label_position=ft.LabelPosition.LEFT
        )
        b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
        page.add(c1, c2, c3, c4, c5, b, t)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/checkbox
    """

    label: Optional[str] = None
    value: Optional[bool] = None
    label_position: Optional[LabelPosition] = None
    label_style: Optional[TextStyle] = None
    tristate: Optional[bool] = None
    autofocus: Optional[bool] = None
    fill_color: ControlStateValue[ColorValue] = None
    overlay_color: ControlStateValue[ColorValue] = None
    check_color: Optional[ColorValue] = None
    active_color: Optional[ColorValue] = None
    hover_color: Optional[ColorValue] = None
    focus_color: Optional[ColorValue] = None
    semantics_label: Optional[str] = None
    shape: Optional[OutlinedBorder] = None
    splash_radius: OptionalNumber = None
    border_side: ControlStateValue[BorderSide] = None
    is_error: Optional[bool] = None
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: Optional[MouseCursor] = None
    on_change: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
