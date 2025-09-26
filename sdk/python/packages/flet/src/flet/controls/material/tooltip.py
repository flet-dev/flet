from dataclasses import dataclass, field
from typing import Optional, Union

from flet.controls.border_radius import (
    BorderRadius,
)
from flet.controls.box import BoxConstraints, BoxDecoration
from flet.controls.duration import DurationValue
from flet.controls.margin import MarginValue
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ColorValue,
    MouseCursor,
    Number,
    TextAlign,
)


class TooltipTriggerMode:
    MANUAL = "manual"
    """"""

    TAP = "tap"
    """
    Tooltip will be shown after a single tap.
    """

    LONG_PRESS = "long_press"
    """
    Tooltip will be shown after a long press.
    """


@dataclass
class Tooltip:
    """
    Provide text labels which help explain the function of a button or
    other user interface action.
    """

    message: str
    """
    The text to display in the tooltip.
    """

    decoration: Optional[BoxDecoration] = field(
        default_factory=lambda: BoxDecoration(border_radius=BorderRadius.all(4.0))
    )
    """
    The tooltip's background decoration.
    """

    enable_feedback: Optional[bool] = None
    """
    When `True` (default) the tooltip should provide acoustic and/or haptic
    feedback.

    For example, on Android a tap will produce a clicking sound and a long-press
    will produce a short vibration, when feedback is enabled.
    """

    vertical_offset: Optional[Number] = None
    """
    The vertical gap between the control and the displayed tooltip.

    When [`prefer_below`][(c).] is set to `True`
    and tooltips have sufficient space to
    display themselves, this property defines how much vertical space
    tooltips will position themselves under their corresponding controls.
    Otherwise, tooltips will position themselves above their corresponding
    controls with the given offset.
    """

    margin: Optional[MarginValue] = None
    """
    The empty space that surrounds the tooltip.

    If `None`, [`TooltipTheme.margin`][flet.] is used.
    If that's is also `None`, defaults to `Margin.all(0.0)`.
    """

    padding: Optional[PaddingValue] = None
    """
    The amount of space by which to inset the tooltip's content.

    It has the following default values based on the current platform:

    - On mobile platforms: `Padding.symmetric(horizontal=16.0, vertical=4.0)`
    - On desktop platforms: `Padding.symmetric(horizontal=8.0, vertical=4.0)`
    """

    bgcolor: Optional[ColorValue] = None
    """
    Background color of the tooltip.
    """

    text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.] to use for the
    message of the tooltip.
    """

    text_align: Optional[TextAlign] = None
    """
    How the message of the tooltip is aligned horizontally.

    If `None`, [`TooltipTheme.text_align`][flet.] is used.
    If that's is also `None`, defaults to [`TextAlign.START`][flet.].
    """

    prefer_below: Optional[bool] = None
    """
    Whether the tooltip defaults to being displayed below the control.

    If there is insufficient space to display the tooltip in the preferred
    direction, the tooltip will be displayed in the opposite direction.

    If `None`, [`TooltipTheme.prefer_below`][flet.] is used.
    If that's is also `None`, defaults to `True`.
    """

    show_duration: Optional[DurationValue] = None
    """
    The length of time that the tooltip will be shown after a long press is released
    (if triggerMode is [`TooltipTriggerMode.LONG_PRESS`][flet.]) or a tap is released
    (if triggerMode is [`TooltipTriggerMode.TAP`][flet.]).
    This property does not affect mouse pointer devices.

    If `None`, [`TooltipTheme.show_duration`][flet.] is used.
    If that's is also `None`, defaults to `1.5` seconds for long press and tap released
    """

    wait_duration: Optional[DurationValue] = None
    """
    The length of time, in milliseconds, that a pointer must hover over a
    tooltip's control before the tooltip will be shown.

    If `None`, [`TooltipTheme.wait_duration`][flet.] is used.
    If that's is also `None`, defaults to `100` milliseconds.
    """

    exit_duration: Optional[DurationValue] = None
    """
    The length of time that the tooltip will be shown after a
    long press is released or a tap is released or mouse pointer exits the control.

    If `None`, [`TooltipTheme.exit_duration`][flet.] is used.
    If that's is also `None`, defaults to 0 milliseconds - no delay.
    """

    tap_to_dismiss: bool = True
    """
    Whether the tooltip can be dismissed by tapping on it.
    """

    exclude_from_semantics: Optional[bool] = False
    """
    Whether the tooltip's message should be excluded from the semantics tree.
    """

    trigger_mode: Optional[TooltipTriggerMode] = None
    """
    The mode of the tooltip's trigger.

    If `None`, [`TooltipTheme.trigger_mode`][flet.] is used.
    If that's is also `None`, defaults to
    [`TooltipTriggerMode.LONG_PRESS`][flet.].
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor for a mouse pointer when it enters or is hovering over the content.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Defines the constraints on the size of this tooltip.

    If `None`, [`TooltipTheme.size_constraints`][flet.] is used.
    If that's is also `None`, then a default value will be picked
    based on the current platform:

    - on desktop platforms: `BoxConstraints(min_height=24.0)`
    - on mobile platforms: `BoxConstraints(min_height=32.0)`
    """


TooltipValue = Union[str, Tooltip]
