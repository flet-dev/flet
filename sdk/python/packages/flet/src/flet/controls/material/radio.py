from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    LabelPosition,
    MouseCursor,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    VisualDensity,
)

__all__ = ["Radio"]


@control("Radio")
class Radio(ConstrainedControl, AdaptiveControl):
    """
    Radio buttons let people select a single option from two or more choices.

    Example:
    ```
    import flet as ft

    def main(page):
    def button_clicked(e):
        t.value = f"Your favorite color is:  {cg.value}"
        page.update()

    t = ft.Text()
    b = ft.ElevatedButton(text='Submit', on_click=button_clicked)
    cg = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="red", label="Red"),
        ft.Radio(value="green", label="Green"),
        ft.Radio(value="blue", label="Blue")]))

    page.add(ft.Text("Select your favorite color:"), cg, b, t)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/radio
    """

    label: str = ""
    label_position: LabelPosition = LabelPosition.RIGHT
    label_style: Optional[TextStyle] = None
    value: Optional[str] = None
    autofocus: bool = False
    fill_color: OptionalControlStateValue[ColorValue] = None
    active_color: OptionalColorValue = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    hover_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    splash_radius: OptionalNumber = None
    toggleable: bool = False
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: Optional[MouseCursor] = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    # def before_update(self):
    #     super().before_update()
    #     self._set_attr_json("fillColor", self.__fill_color, wrap_attr_dict=True)
    #     self._set_attr_json("overlayColor", self.__overlay_color, wrap_attr_dict=True)
