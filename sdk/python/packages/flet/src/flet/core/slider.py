from dataclasses import field
from enum import Enum
from typing import Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import control
from flet.core.types import (
    ColorValue,
    ControlStateValue,
    MouseCursor,
    Number,
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
    A slider provides a visual indication of adjustable content, as well as the current setting in the total range of content.

    Use a slider when you want people to set defined values (such as volume or brightness), or when people would benefit from instant feedback on the effect of setting changes.

    Example:
    ```
    import flet as ft

    def main(page):
        page.add(
            ft.Text("Slider with value:"),
            ft.Slider(value=0.3),
            ft.Text("Slider with a custom range and label:"),
            ft.Slider(min=0, max=100, divisions=10, label="{value}%"))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/slider
    """

    value: Number = field(default=0.0)
    label: Optional[str] = None
    min: Number = field(default=0.0)
    max: Number = field(default=1.0)
    divisions: Optional[int] = None
    round: int = field(default=0)
    autofocus: bool = field(default=False)
    active_color: Optional[ColorValue] = None
    inactive_color: Optional[ColorValue] = None
    thumb_color: Optional[ColorValue] = None
    interaction: Optional[SliderInteraction] = None
    secondary_active_color: Optional[ColorValue] = None
    overlay_color: ControlStateValue[ColorValue] = None
    secondary_track_value: OptionalNumber = None
    mouse_cursor: Optional[MouseCursor] = None
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
        assert self.value >= self.min, "value must be greater than or equal to min"
        assert self.value <= self.max, "value must be less than or equal to max"
        # self._set_attr_json("overlayColor", self.__overlay_color, wrap_attr_dict=True)
