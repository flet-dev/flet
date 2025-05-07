from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["RangeSlider"]


@control("RangeSlider")
class RangeSlider(ConstrainedControl):
    """
    A Material Design range slider. Used to select a range from a range of values.
    A range slider can be used to select from either a continuous or a discrete
    set of values.
    The default is to use a continuous range of values from min to max.

    Online docs: https://flet.dev/docs/controls/rangeslider
    """

    start_value: Number
    end_value: Number
    label: Optional[str] = None
    min: OptionalNumber = None
    max: OptionalNumber = None
    divisions: Optional[int] = None
    round: Optional[int] = None
    active_color: OptionalColorValue = None
    inactive_color: OptionalColorValue = None
    overlay_color: OptionalControlStateValue[ColorValue] = None
    mouse_cursor: OptionalControlStateValue[MouseCursor] = None
    on_change: OptionalControlEventCallable = None
    on_change_start: OptionalControlEventCallable = None
    on_change_end: OptionalControlEventCallable = None

    def before_update(self):
        if self.max is not None:
            assert (
                self.end_value <= self.max
            ), "end_value must be less than or equal to max"

        if self.min is not None:
            assert (
                self.start_value >= self.min
            ), "start_value must be greater than or equal to min"

        assert (
            self.start_value <= self.end_value
        ), "start_value must be less than or equal to end_value"
        pass
