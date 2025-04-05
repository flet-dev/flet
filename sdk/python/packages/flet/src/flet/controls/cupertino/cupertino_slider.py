from typing import Optional

from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import control
from flet.controls.types import (
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["CupertinoSlider"]


@control("CupertinoSlider")
class CupertinoSlider(ConstrainedControl):
    """
    An iOS-type slider.

    It provides a visual indication of adjustable content, as well as the current setting in the total range of content.

    Use a slider when you want people to set defined values (such as volume or brightness), or when people would benefit from instant feedback on the effect of setting changes.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoslider
    """

    value: OptionalNumber = None
    min: Number = 0.0
    max: Number = 1.0
    divisions: Optional[int] = None
    round: int = 0
    active_color: OptionalColorValue = None
    thumb_color: OptionalColorValue = None
    on_change: OptionalControlEventCallable = None
    on_change_start: OptionalControlEventCallable = None
    on_change_end: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        self.value = self.value if self.value is not None else self.min
        assert self.min <= self.max, "min must be less than or equal to max"
        assert self.value is None or (
            self.value >= self.min
        ), "value must be greater than or equal to min"
        assert self.value is None or (
            self.value <= self.max
        ), "value must be less than or equal to max"
