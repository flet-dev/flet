from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
)

__all__ = ["Slider", "SliderInteraction"]


class SliderInteraction(Enum):
    TAP_AND_SLIDE = "tapAndSlide"
    TAP_ONLY = "tapOnly"
    SLIDE_ONLY = "slideOnly"
    SLIDE_THUMB = "slideThumb"


@control("Slider")
class Slider(LayoutControl, AdaptiveControl):
    """
    A slider provides a visual indication of adjustable content, as well as the
    current setting in the total range of content.

    Use a slider when you want people to set defined values (such as volume or
    brightness), or when people would benefit from instant feedback on the effect
    of setting changes.

    ```python
    ft.Slider(label="Slider", value=0.3)
    ```

    """

    value: Optional[Number] = None
    """
    The currently selected value for this slider.

    The slider's thumb is drawn at a position that corresponds to this value.

    Defaults to value of [`min`][(c).].

    Raises:
        ValueError: If [`value`][(c).] is less than [`min`][(c).] or greater than
            [`max`][(c).].
    """

    label: Optional[str] = None
    """
    A label to show above the slider when the slider is active. The value of
    `label` may contain `{value}` which will be dynamically replaced with a current
    slider value. For example, `"Volume: {value}"`.

    It is used to display the value of a discrete slider, and it is displayed as
    part of the value indicator shape.

    If not set, then the value indicator will not be displayed.
    """

    min: Number = 0.0
    """
    The minimum value the user can select.

    Note:
        - Must be less than or equal to [`max`][(c).].
        - If the [`max`][(c).] is equal to the `min`, then this slider
            is disabled.

    Raises:
        ValueError: If [`min`][(c).] is greater than [`max`][(c).].
    """

    max: Number = 1.0
    """
    The maximum value the user can select.

    Note:
        - Must be greater than or equal to [`min`][(c).].
        - If the [`min`][(c).] is equal to the `max`, then this slider
            is disabled.

    Raises:
        ValueError: If [`max`][(c).] is less than [`min`][(c).].
    """

    divisions: Optional[int] = None
    """
    The number of discrete divisions.

    Typically used with [`label`][(c).] to show the current discrete value.

    If `None`, this slider is continuous.
    """

    round: int = 0
    """
    The number of decimals displayed on the [`label`][(c).]
    containing [`value`][(c).].

    Defaults to `0`, which displays value rounded to the nearest integer.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more
    than one control on a page with autofocus set, then the first one added to the
    page will get focus.
    """

    active_color: Optional[ColorValue] = None
    """
    The color to use for the portion of
    the slider track that is active.

    The "active" side of the slider is the side between the thumb and the minimum
    value.
    """

    inactive_color: Optional[ColorValue] = None
    """
    The color for the inactive portion of
    the slider track.

    The "inactive" side of the slider is the side between the thumb and the maximum
    value.
    """

    thumb_color: Optional[ColorValue] = None
    """
    The color of the thumb.
    """

    interaction: Optional[SliderInteraction] = None
    """
    The allowed way for the user to interact with this slider.

    If `None`, [`SliderTheme.interaction`][flet.] is used.
    If that's is also `None`, defaults to
    [`SliderInteraction.TAP_AND_SLIDE`][flet.].
    """

    secondary_active_color: Optional[ColorValue] = None
    """
    The color to use for the portion of
    the slider track between the thumb and
    the [`secondary_track_value`][(c).].
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The highlight color that's typically
    used to indicate that the range slider thumb is in
    [`ControlState.HOVERED`][flet.] or
    [`ControlState.DRAGGED`][flet.] states.
    """

    secondary_track_value: Optional[Number] = None
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
    """

    padding: Optional[PaddingValue] = None
    """
    Determines the padding around this slider.
    """

    year_2023: Optional[bool] = None
    """
    If this is set to `False`, this slider will use the latest
    Material Design 3 appearance, which was introduced in December 2023.

    When `True`, the Slider will use the 2023 Material Design 3 appearance.

    If not set, then the
    [`SliderTheme.year_2023`][flet.] will be
    used, which is `False` by default.

    If [`Theme.use_material3`][flet.] is `False`,
    then this property is ignored.
    """

    on_change: Optional[ControlEventHandler["Slider"]] = None
    """
    Called when the state of this slider is changed.
    """

    on_change_start: Optional[ControlEventHandler["Slider"]] = None
    """
    Called when the user starts selecting a new value for this slider.
    """

    on_change_end: Optional[ControlEventHandler["Slider"]] = None
    """
    Called when the user is done selecting a new value for this slider.
    """

    on_focus: Optional[ControlEventHandler["Slider"]] = None
    """
    Called when this slider has received focus.
    """

    on_blur: Optional[ControlEventHandler["Slider"]] = None
    """
    Called when this slider has lost focus.
    """

    def before_update(self):
        super().before_update()
        if self.max is not None and self.min > self.max:
            raise ValueError(
                f"min ({self.min}) must be less than or equal to max ({self.max})"
            )
        if self.value is not None and self.value < self.min:
            raise ValueError(
                f"value ({self.value}) must be greater than or "
                f"equal to min ({self.min})"
            )
        if self.value is not None and self.value > self.max:
            raise ValueError(
                f"value ({self.value}) must be less than or equal to max ({self.max})"
            )
