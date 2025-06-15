from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    LabelPosition,
    MouseCursor,
    OptionalColorValue,
    OptionalNumber,
    VisualDensity,
)

__all__ = ["Radio"]


@control("Radio")
class Radio(ConstrainedControl, AdaptiveControl):
    """
    Radio buttons let people select a single option from two or more choices.

    Online docs: https://flet.dev/docs/controls/radio
    """

    label: str = ""
    """
    The clickable label to display on the right of a Radio.
    """

    label_position: LabelPosition = LabelPosition.RIGHT
    """
    Value is of type [`LabelPosition`](https://flet.dev/docs/reference/types/labelposition)
    and defaults to `LabelPosition.RIGHT`.
    """

    label_style: Optional[TextStyle] = None
    """
    The label's style.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
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
    The [color](https://flet.dev/docs/reference/colors) that fills the radio, in all or
    specific [`ControlState`](https://flet.dev/docs/reference/types/controlstate) 
    states.
    """

    active_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used to fill this radio when it 
    is selected.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The overlay [color](https://flet.dev/docs/reference/colors) of this radio in all or
    specific [`ControlState`](https://flet.dev/docs/reference/types/controlstate) 
    states.
    """

    hover_color: OptionalColorValue = None
    """
    The color of this radio when it is hovered.
    """

    focus_color: OptionalColorValue = None
    """
    The color of this radio when it has the input focus.
    """

    splash_radius: OptionalNumber = None
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

    Value is of type [`VisualDensity`](https://flet.dev/docs/reference/types/visualdensity).
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor for a mouse pointer entering or hovering over this control.

    Value is of type [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor).
    """

    on_focus: OptionalControlEventHandler["Radio"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["Radio"] = None
    """
    Fires when the control has lost focus.
    """
