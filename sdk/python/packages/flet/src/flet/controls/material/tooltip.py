from dataclasses import dataclass
from typing import Optional, Union

from flet.controls.border import Border
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.box import BoxShadow, BoxShape, DecorationImage
from flet.controls.duration import OptionalDurationValue
from flet.controls.gradients import Gradient
from flet.controls.margin import OptionalMarginValue
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import BlendMode, OptionalColorValue, OptionalNumber, TextAlign


class TooltipTriggerMode:
    MANUAL = "manual"
    TAP = "tap"
    LONG_PRESS = "long_press"


@dataclass
class Tooltip:
    """
    Tooltips provide text labels which help explain the function of a button or
    other user interface action.
    """

    message: str
    """
    The text to display in the tooltip.
    """

    enable_feedback: Optional[bool] = None
    """
    When `True` (default) the tooltip should provide acoustic and/or haptic
    feedback.

    For example, on Android a tap will produce a clicking sound and a long-press
    will produce a short vibration, when feedback is enabled.
    """

    height: OptionalNumber = None
    """
    The height of the tooltip's content.
    """

    vertical_offset: OptionalNumber = None
    """
    The vertical gap between the control and the displayed tooltip.
    """

    margin: OptionalMarginValue = None
    """
    The empty space that surrounds the tooltip.

    Value is of type [`Margin`](https://flet.dev/docs/reference/types/margin)
    or a number.
    """

    padding: OptionalPaddingValue = None
    """
    The amount of space by which to inset the tooltip's content.

    The value is an instance of
    [`Padding`](https://flet.dev/docs/reference/types/padding) class or a number.

    On mobile, defaults to `16.0` logical pixels horizontally and `4.0` vertically.
    On desktop, defaults to `8.0` logical pixels horizontally and `4.0` vertically.
    """

    bgcolor: OptionalColorValue = None
    """
    Background [color](https://flet.dev/docs/reference/colors) of the tooltip.
    """

    image: Optional[DecorationImage] = None
    """
    The background image of the tooltip.

    Value is of type
    [`DecorationImage`](https://flet.dev/docs/reference/types/decorationimage).
    """

    shadow: Optional[list[BoxShadow]] = None
    """
    A list of [BoxShadow](https://flet.dev/docs/reference/types/boxshadow) to cast
    a shadow behind the tooltip.
    """

    blend_mode: Optional[BlendMode] = None
    """
    The blend mode to apply when painting the tooltip.

    Value is of type [`BlendMode`](https://flet.dev/docs/reference/types/blendmode).
    """

    gradient: Optional[Gradient] = None
    """
    Background gradient of the tooltip.

    Value is of type [`Gradient`](https://flet.dev/docs/reference/types/gradient).
    """

    border: Optional[Border] = None
    """
    [`Border`](https://flet.dev/docs/reference/types/border) around the tooltip.
    """

    border_radius: OptionalBorderRadiusValue = None
    """
    Tooltip's [`border radius`](https://flet.dev/docs/reference/types/borderradius).
    """

    shape: Optional[BoxShape] = None
    """
    The shape of the tooltip.

    Value is of type [`BoxShape`](https://flet.dev/docs/reference/types/boxshape).
    """

    text_style: Optional[TextStyle] = None
    """
    The [TextStyle](https://flet.dev/docs/reference/types/textstyle) to use for the
    message of the tooltip.
    """

    text_align: Optional[TextAlign] = None
    """
    How the message of the tooltip is aligned horizontally.

    Value is of type [`TextAlign`](https://flet.dev/docs/reference/types/textalign)
    and defaults to `TextAlign.LEFT`.
    """

    prefer_below: Optional[bool] = None
    """
    Whether the tooltip defaults to being displayed below the control.

    If there is insufficient space to display the tooltip in the preferred
    direction, the tooltip will be displayed in the opposite direction.

    Defaults to `True`.
    """

    show_duration: OptionalDurationValue = None
    """
    The length of time, in milliseconds, that the tooltip will be shown after a
    long press is released or a tap is released or mouse pointer exits the control.
    """

    wait_duration: OptionalDurationValue = None
    """
    The length of time, in milliseconds, that a pointer must hover over a
    tooltip's control before the tooltip will be shown.

    Defaults to 0 milliseconds (tooltips are shown immediately upon hover).
    """

    exit_duration: OptionalDurationValue = None
    """
    The length of time, in milliseconds, that the tooltip will be shown after a
    long press is released or a tap is released or mouse pointer exits the control.
    """

    enable_tap_to_dismiss: Optional[bool] = None
    """
    Whether the tooltip can be dismissed by tapping on it.

    Defaults to `True`.
    """

    exclude_from_semantics: Optional[bool] = None
    """
    Whether the tooltip's message should be excluded from the semantics tree.

    Defaults to `False`.
    """

    trigger_mode: Optional[TooltipTriggerMode] = None
    """
    The mode of the tooltip's trigger.

    Value is of type
    [`TooltipTriggerMode`](https://flet.dev/docs/reference/types/tooltiptriggermode).
    """


TooltipValue = Union[str, Tooltip]
