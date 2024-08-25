from dataclasses import dataclass
from typing import Optional, List, Union

from flet_core.border import Border
from flet_core.box import BoxShape, DecorationImage, BoxShadow
from flet_core.gradients import Gradient
from flet_core.text_style import TextStyle
from flet_core.types import (
    BorderRadiusValue,
    MarginValue,
    PaddingValue,
    TextAlign,
    DurationValue,
    OptionalNumber,
    BlendMode,
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
    margin: MarginValue = None
    padding: PaddingValue = None
    bgcolor: Optional[str] = None
    image: Optional[DecorationImage] = None
    shadow: List[BoxShadow] = None
    blend_mode: Optional[BlendMode] = None
    gradient: Optional[Gradient] = None
    border: Optional[Border] = None
    border_radius: BorderRadiusValue = None
    shape: Optional[BoxShape] = None
    text_style: Optional[TextStyle] = None
    text_align: Optional[TextAlign] = None
    prefer_below: Optional[bool] = None
    show_duration: DurationValue = None
    wait_duration: DurationValue = None
    exit_duration: DurationValue = None
    enable_tap_to_dismiss: Optional[bool] = None
    exclude_from_semantics: Optional[bool] = None
    trigger_mode: Optional[TooltipTriggerMode] = None


TooltipValue = Optional[Union[str, "Tooltip"]]
