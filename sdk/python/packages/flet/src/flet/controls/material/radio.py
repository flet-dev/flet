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
