from dataclasses import dataclass
from typing import List, Optional, Union

from flet.controls.border import Border
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.box import BoxShadow, BoxShape, DecorationImage
from flet.controls.gradients import Gradient
from flet.controls.margin import OptionalMarginValue
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    BlendMode,
    DurationValue,
    OptionalColorValue,
    OptionalNumber,
    TextAlign,
)


class TooltipTriggerMode:
    MANUAL = "manual"
    TAP = "tap"
    LONG_PRESS = "long_press"


@dataclass
class Tooltip:
    """Tooltips provide text labels which help explain the function of a button or other user interface action."""

    message: str
    enable_feedback: Optional[bool] = None
    height: OptionalNumber = None
    vertical_offset: OptionalNumber = None
    margin: OptionalMarginValue = None
    padding: OptionalPaddingValue = None
    bgcolor: OptionalColorValue = None
    image: Optional[DecorationImage] = None
    shadow: Optional[List[BoxShadow]] = None
    blend_mode: Optional[BlendMode] = None
    gradient: Optional[Gradient] = None
    border: Optional[Border] = None
    border_radius: OptionalBorderRadiusValue = None
    shape: Optional[BoxShape] = None
    text_style: Optional[TextStyle] = None
    text_align: Optional[TextAlign] = None
    prefer_below: Optional[bool] = None
    show_duration: Optional[DurationValue] = None
    wait_duration: Optional[DurationValue] = None
    exit_duration: Optional[DurationValue] = None
    enable_tap_to_dismiss: Optional[bool] = None
    exclude_from_semantics: Optional[bool] = None
    trigger_mode: Optional[TooltipTriggerMode] = None


TooltipValue = Union[str, Tooltip]
