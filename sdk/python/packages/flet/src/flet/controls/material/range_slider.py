from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
)

__all__ = ["RangeSlider"]


@control("RangeSlider")
class RangeSlider(LayoutControl):
    """
    A Material Design range slider. Used to select a range from a range of values.
    A range slider can be used to select from either a continuous or a discrete
    set of values.
    The default is to use a continuous range of values from min to max.

    ```python
    ft.RangeSlider(
        min=0,
        max=10,
        start_value=2,
        divisions=10,
        end_value=7,
    )
    ```

    """

    start_value: Number
    """
    The currently selected start value for the slider.

   The slider's left thumb is drawn at a position that corresponds to this value.

    Raises:
        ValueError: If [`start_value`][(c).] is less than [`min`][(c).] or greater
            than [`end_value`][(c).].
    """

    end_value: Number
    """
    The currently selected end value for the slider.

    The slider's right thumb is drawn at a position that corresponds to this value.

    Raises:
        ValueError: If [`end_value`][(c).] is greater than [`max`][(c).] or less than
            [`start_value`][(c).].
    """

    label: Optional[str] = None
    """
    A label to show above the slider thumbs when the slider is active. The value of
    `label` may contain `{value}` which will be replaced with a current slider
    `start_value` and `end_value`.

    If not set, then the labels will not be displayed.
    """

    min: Optional[Number] = None
    """
    The minimum value the user can select.

    Defaults to `0.0`. Must be less than or equal to `max`.

    If the `max` is equal to the `min`, then the slider is disabled.

    Raises:
        ValueError: If [`min`][(c).] is greater than [`max`][(c).].
    """

    max: Optional[Number] = None
    """
    The maximum value the user can select. Must be greater than or equal to `min`.

    If the `max` is equal to the `min`, then the slider is disabled.

    Defaults to `1.0`.

    Raises:
        ValueError: If [`max`][(c).] is less than [`min`][(c).].
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

    active_color: Optional[ColorValue] = None
    """
    The color to use for the portion of the
    slider track that is active.

    The "active" segment of the range slider is the span between the thumbs.
    """

    inactive_color: Optional[ColorValue] = None
    """
    The color for the inactive portions of
    the slider track.

    The "inactive" segments of the slider are the span of tracks between the min and
    the start thumb, and the end thumb and the max.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The highlight color that's typically
    used to indicate that the range slider thumb is in `HOVERED` or `DRAGGED`
    [`ControlState`][flet.] .
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    The cursor for a mouse pointer entering or hovering over this control.
    """

    on_change: Optional[ControlEventHandler["RangeSlider"]] = None
    """
    Called when the state of the Slider is changed.
    """

    on_change_start: Optional[ControlEventHandler["RangeSlider"]] = None
    """
    Called when the user starts selecting a new value for the slider.
    """

    on_change_end: Optional[ControlEventHandler["RangeSlider"]] = None
    """
    Called when the user is done selecting a new value for the slider.
    """

    def before_update(self):
        if self.max is not None and self.end_value > self.max:
            raise ValueError("end_value must be less than or equal to max")

        if self.min is not None and self.start_value < self.min:
            raise ValueError("start_value must be greater than or equal to min")

        if self.start_value > self.end_value:
            raise ValueError("start_value must be less than or equal to end_value")
        pass
