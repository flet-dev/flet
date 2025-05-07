from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["Slider", "SliderInteraction"]


class SliderInteraction(Enum):
    TAP_AND_SLIDE = "tapAndSlide"
    TAP_ONLY = "tapOnly"
    SLIDE_ONLY = "slideOnly"
    SLIDE_THUMB = "slideThumb"


@control("Slider")
class Slider(ConstrainedControl, AdaptiveControl):
    """
    A slider provides a visual indication of adjustable content, as well as the
    current setting in the total range of content.

    Use a slider when you want people to set defined values (such as volume or
    brightness), or when people would benefit from instant feedback on the effect
    of setting changes.

    Online docs: https://flet.dev/docs/controls/slider
    """

    value: OptionalNumber = None
    label: Optional[str] = None
    min: Number = 0.0
    max: Number = 1.0
    divisions: Optional[int] = None
    round: int = 0
    autofocus: bool = False
    active_color: OptionalColorValue = None
    inactive_color: OptionalColorValue = None
    thumb_color: OptionalColorValue = None
    interaction: Optional[SliderInteraction] = None
    secondary_active_color: OptionalColorValue = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    secondary_track_value: OptionalNumber = None
    mouse_cursor: Optional[MouseCursor] = None
    padding: Optional[PaddingValue] = None
    year_2023: Optional[bool] = None
    on_change: OptionalControlEventCallable = None
    on_change_start: OptionalControlEventCallable = None
    on_change_end: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.max is None or self.min <= self.max
        ), "min must be less than or equal to max"
        assert (
            self.value is None or self.value >= self.min
        ), "value must be greater than or equal to min"
        assert (
            self.value is None or self.value <= self.max
        ), "value must be less than or equal to max"
