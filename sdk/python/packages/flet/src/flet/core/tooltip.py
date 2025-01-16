from dataclasses import dataclass
from typing import List, Optional, Union

from flet.core.border import Border
from flet.core.box import BoxShadow, BoxShape, DecorationImage
from flet.core.gradients import Gradient
from flet.core.text_style import TextStyle
from flet.core.types import (
    BlendMode,
    BorderRadiusValue,
    ColorValue,
    DurationValue,
    MarginValue,
    OptionalNumber,
    PaddingValue,
    TextAlign,
)


class TooltipTriggerMode:
    MANUAL = "manual"
    TAP = "tap"
    LONG_PRESS = "long_press"


@dataclass
class Tooltip:
    """Tooltips provide text labels which help explain the function of a button or other user interface action."""

    message: Optional[str] = None
    enable_feedback: Optional[bool] = None
    height: OptionalNumber = None
    vertical_offset: OptionalNumber = None
    margin: Optional[MarginValue] = None
    padding: Optional[PaddingValue] = None
    bgcolor: Optional[ColorValue] = None
    image: Optional[DecorationImage] = None
    shadow: Optional[List[BoxShadow]] = None
    blend_mode: Optional[BlendMode] = None
    gradient: Optional[Gradient] = None
    border: Optional[Border] = None
    border_radius: Optional[BorderRadiusValue] = None
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


TooltipValue = Union[str, "Tooltip"]
