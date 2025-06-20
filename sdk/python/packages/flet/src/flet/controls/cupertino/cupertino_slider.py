from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.types import (
    Number,
    OptionalColorValue,
    OptionalNumber,
)

__all__ = ["CupertinoSlider"]


@control("CupertinoSlider")
class CupertinoSlider(ConstrainedControl):
    """
    An iOS-type slider.

    It provides a visual indication of adjustable content, as well as the current
    setting in the total range of content.

    Use a slider when you want people to set defined values (such as volume or
    brightness), or when people would benefit from instant feedback on the effect of
    setting changes.

    Online docs: https://flet.dev/docs/controls/cupertinoslider
    """

    value: OptionalNumber = None
    """
    The currently selected value for this slider.

    The slider's thumb is drawn at a position that corresponds to this value.
    """

    min: Number = 0.0
    """
    The minimum value the user can select.

    Defaults to `0.0`. Must be less than or equal to `max`.

    If the `max` is equal to the `min`, then the slider is disabled.
    """

    max: Number = 1.0
    """
    The maximum value the user can select.

    Defaults to `1.0`. Must be greater than or equal to `min`.

    If the `max` is equal to the `min`, then the slider is disabled.
    """

    divisions: Optional[int] = None
    """
    The number of discrete divisions.

    If not set, the slider is continuous.
    """

    round: int = 0
    """
    TBD
    """

    active_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for the portion of the 
    slider track that is active.

    The "active" side of the slider is the side between the thumb and the minimum 
    value.
    """

    thumb_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the thumb.
    """

    on_change: OptionalControlEventHandler["CupertinoSlider"] = None
    """
    Fires when the state of the Slider is changed.
    """

    on_change_start: OptionalControlEventHandler["CupertinoSlider"] = None
    """
    Fires when the user starts selecting a new value for the slider.
    """

    on_change_end: OptionalControlEventHandler["CupertinoSlider"] = None
    """
    Fires when the user is done selecting a new value for the slider.
    """

    on_focus: OptionalControlEventHandler["CupertinoSlider"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["CupertinoSlider"] = None
    """
    Fires when the control has lost focus.
    """

    def before_update(self):
        super().before_update()
        self.value = self.value if self.value is not None else self.min
        assert self.min <= self.max, "min must be less than or equal to max"
        assert self.value is None or (self.value >= self.min), (
            "value must be greater than or equal to min"
        )
        assert self.value is None or (self.value <= self.max), (
            "value must be less than or equal to max"
        )
