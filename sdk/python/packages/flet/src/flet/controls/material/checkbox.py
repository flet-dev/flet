from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.buttons import OutlinedBorder
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
    StrOrControl,
    VisualDensity,
)

__all__ = ["Checkbox"]


@control("Checkbox")
class Checkbox(ConstrainedControl, AdaptiveControl):
    """
    Checkbox allows to select one or more items from a group, or switch between two mutually exclusive options (checked or unchecked, on or off).

    Online docs: https://flet.dev/docs/controls/checkbox
    """

    label: Optional[StrOrControl] = None
    value: Optional[bool] = None
    label_position: LabelPosition = LabelPosition.RIGHT
    label_style: Optional[TextStyle] = None
    tristate: bool = False
    autofocus: bool = False
    fill_color: OptionalControlStateValue[ColorValue] = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    check_color: OptionalColorValue = None
    active_color: OptionalColorValue = None
    hover_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    semantics_label: Optional[str] = None
    shape: Optional[OutlinedBorder] = None
    splash_radius: OptionalNumber = None
    border_side: OptionalControlStateValue[BorderSide] = None
    is_error: bool = False
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: Optional[MouseCursor] = None
    on_change: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
