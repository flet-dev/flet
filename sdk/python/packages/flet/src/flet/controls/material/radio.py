from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.layout_control import LayoutControl
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    LabelPosition,
    MouseCursor,
    Number,
    VisualDensity,
)

__all__ = ["Radio"]


@control("Radio")
class Radio(LayoutControl, AdaptiveControl):
    """
    Radio buttons let people select a single option from two or more choices.

    ```python
    ft.RadioGroup(
        content=ft.Row(
            controls=[ft.Radio(label=f"{i}") for i in range(1, 4)],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    ```

    """

    label: str = ""
    """
    The clickable label to display on the right of a Radio.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    Defaults to `LabelPosition.RIGHT`.
    """

    label_style: Optional[TextStyle] = None
    """
    The label's style.
    """

    value: Optional[str] = None
    """
    The value to set to containing `RadioGroup` when the radio is selected.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus.

    If there is more than one control on a page with autofocus set, then the first one
    added to the page will get focus.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color that fills the radio, in all or specific [`ControlState`][flet.] states.
    """

    active_color: Optional[ColorValue] = None
    """
    The color used to fill this radio when it is selected.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The overlay color of this radio in all or specific [`ControlState`][flet.] states.
    """

    hover_color: Optional[ColorValue] = None
    """
    The color of this radio when it is hovered.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color of this radio when it has the input focus.
    """

    splash_radius: Optional[Number] = None
    """
    The splash radius of the circular Material ink response.
    """

    toggleable: bool = False
    """
    Set to `True` if this radio button is allowed to be returned to an indeterminate
    state by selecting it again when selected.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Defines how compact the radio's layout will be.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor for a mouse pointer entering or hovering over this control.
    """

    on_focus: Optional[ControlEventHandler["Radio"]] = None
    """
    Called when the control has received focus.
    """

    on_blur: Optional[ControlEventHandler["Radio"]] = None
    """
    Called when the control has lost focus.
    """
