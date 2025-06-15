from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
    OptionalColorValue,
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
    """
    The currently selected start value for the slider.

    The slider's left thumb is drawn at a position that corresponds to this value.
    """

    end_value: Number
    """
    The currently selected end value for the slider.

    The slider's right thumb is drawn at a position that corresponds to this value.
    """

    label: Optional[str] = None
    """
    A label to show above the slider thumbs when the slider is active. The value of
    `label` may contain `{value}` which will be replaced with a current slider
    `start_value` and `end_value`.

    If not set, then the labels will not be displayed.
    """

    min: OptionalNumber = None
    """
    The minimum value the user can select.

    Defaults to `0.0`. Must be less than or equal to `max`.

    If the `max` is equal to the `min`, then the slider is disabled.
    """

    max: OptionalNumber = None
    """
    The maximum value the user can select. Must be greater than or equal to `min`.

    If the `max` is equal to the `min`, then the slider is disabled.

    Defaults to `1.0`.
    """

    divisions: Optional[int] = None
    """
    The number of discrete divisions.

    Typically used with `label` to show the current discrete values.

    If not set, the slider is continuous.
    """

    round: Optional[int] = None
    """
    The number of decimals displayed on the `label` containing `{value}`.

    The default is 0 (displays value rounded to the nearest integer).
    """

    active_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for the portion of the
    slider track that is active.

    The "active" segment of the range slider is the span between the thumbs.
    """

    inactive_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) for the inactive portions of
    the slider track.

    The "inactive" segments of the slider are the span of tracks between the min and
    the start thumb, and the end thumb and the max.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The highlight [color](https://flet.dev/docs/reference/colors) that's typically
    used to indicate that the range slider thumb is in `HOVERED` or `DRAGGED`
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate)s.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    The cursor for a mouse pointer entering or hovering over this control.

    It's value can be made to depend on the slider's
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate).

    Value is of type
    [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor).
    """

    on_change: OptionalControlEventHandler["RangeSlider"] = None
    """
    Fires when the state of the Slider is changed.
    """

    on_change_start: OptionalControlEventHandler["RangeSlider"] = None
    """
    Fires when the user starts selecting a new value for the slider.
    """

    on_change_end: OptionalControlEventHandler["RangeSlider"] = None
    """
    Fires when the user is done selecting a new value for the slider.
    """

    def before_update(self):
        if self.max is not None:
            assert self.end_value <= self.max, (
                "end_value must be less than or equal to max"
            )

        if self.min is not None:
            assert self.start_value >= self.min, (
                "start_value must be greater than or equal to min"
            )

        assert self.start_value <= self.end_value, (
            "start_value must be less than or equal to end_value"
        )
        pass
