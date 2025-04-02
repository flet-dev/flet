from dataclasses import field
from typing import Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import control
from flet.core.types import (
    ColorValue,
    Number,
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
    min: Number = field(default=0.0)
    max: Number = field(default=1.0)
    divisions: Optional[int] = None
    round: int = field(default=0)
    active_color: Optional[ColorValue] = None
    thumb_color: Optional[ColorValue] = None
    on_change: OptionalControlEventCallable = None
    on_change_start: OptionalControlEventCallable = None
    on_change_end: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.min is None or self.max is None or self.min <= self.max
        ), "min must be less than or equal to max"
        assert (
            self.min is None or self.value is None or (self.value >= self.min)
        ), "value must be greater than or equal to min"
        assert (
            self.max is None or self.value is None or (self.value <= self.max)
        ), "value must be less than or equal to max"

    # @property
    # def value(self) -> float:
    #     return self._get_attr("value", data_type="float", def_value=self.min or 0.0)
