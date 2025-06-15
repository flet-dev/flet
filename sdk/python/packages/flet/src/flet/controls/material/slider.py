from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
    OptionalColorValue,
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
    """
    The currently selected value for this slider.

    The slider's thumb is drawn at a position that corresponds to this value.

    Defaults to value of `min` property.
    """

    label: Optional[str] = None
    """
    Format with `{value}`.

    A label to show above the slider when the slider is active. The value of
    `label` may contain `{value}` which will be replaced with a current slider
    value.

    It is used to display the value of a discrete slider, and it is displayed as
    part of the value indicator shape.

    If not set, then the value indicator will not be displayed.
    """

    min: Number = 0.0
    """
    The minimum value the user can select. Must be less than or equal to `max`.

    If the `max` is equal to the `min`, then the slider is disabled.

    Defaults to `0.0`.
    """

    max: Number = 1.0
    """
    The maximum value the user can select. Must be greater than or equal to `min`.

    If the `max` is equal to the `min`, then the slider is disabled.

    Defaults to `1.0`.
    """

    divisions: Optional[int] = None
    """
    The number of discrete divisions.

    Typically used with `label` to show the current discrete value.

    If not set, the slider is continuous.
    """

    round: int = 0
    """
    The number of decimals displayed on the `label` containing `value`.

    Defaults to `0`, which displays value rounded to the nearest integer.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more
    than one control on a page with autofocus set, then the first one added to the
    page will get focus.
    """

    active_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for the portion of
    the slider track that is active.

    The "active" side of the slider is the side between the thumb and the minimum
    value.
    """

    inactive_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) for the inactive portion of
    the slider track.

    The "inactive" side of the slider is the side between the thumb and the maximum
    value.
    """

    thumb_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the thumb.
    """

    interaction: Optional[SliderInteraction] = None
    """
    The allowed way for the user to interact with this slider. Value is a
    [`SliderInteraction`](https://flet.dev/docs/reference/types/sliderinteraction)
    and defaults to `SliderInteraction.TAP_AND_SLIDE`.
    """

    secondary_active_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for the portion of
    the slider track between the thumb and the `secondary_track_value`.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The highlight [color](https://flet.dev/docs/reference/colors) that's typically
    used to indicate that the range slider thumb is in `ControlState.HOVERED` or
    `DRAGGED`
    [`ControlState`](https://flet.dev/docs/reference/types/controlstate)s.
    """

    secondary_track_value: OptionalNumber = None
    """
    The secondary track value for this slider.

    If not null, a secondary track using `secondary_active_color` is drawn between
    the thumb and this value, over the inactive track. If less than `value`, then
    the secondary track is not shown.

    It can be ideal for media scenarios such as showing the buffering progress
    while the `value` shows the play progress.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over this
    control.

    Value is of type
    [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor).
    """

    padding: Optional[PaddingValue] = None
    """
    TBD
    """

    year_2023: Optional[bool] = None
    """
    TBD
    """

    on_change: OptionalControlEventHandler["Slider"] = None
    """
    Fires when the state of the Slider is changed.
    """

    on_change_start: OptionalControlEventHandler["Slider"] = None
    """
    Fires when the user starts selecting a new value for the slider.
    """

    on_change_end: OptionalControlEventHandler["Slider"] = None
    """
    Fires when the user is done selecting a new value for the slider.
    """

    on_focus: OptionalControlEventHandler["Slider"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["Slider"] = None
    """
    Fires when the control has lost focus.
    """

    def before_update(self):
        super().before_update()
        assert self.max is None or self.min <= self.max, (
            "min must be less than or equal to max"
        )
        assert self.value is None or self.value >= self.min, (
            "value must be greater than or equal to min"
        )
        assert self.value is None or self.value <= self.max, (
            "value must be less than or equal to max"
        )
