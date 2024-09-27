from dataclasses import dataclass
from typing import List, Optional, Union

from flet_core.alignment import Alignment
from flet_core.border import Border
from flet_core.box import BoxShadow, BoxShape, DecorationImage

# from flet_core.control import Control
# from flet_core.control import Control
from flet_core.gradients import Gradient
from flet_core.text_style import TextStyle
from flet_core.types import (
    BlendMode,
    BorderRadiusValue,
    DurationValue,
    MarginValue,
    OffsetValue,
    OptionalNumber,
    PaddingValue,
    TextAlign,
)

# class TooltipTriggerMode:
#     MANUAL = "manual"
#     TAP = "tap"
#     LONG_PRESS = "long_press"


@dataclass
class Badge:
    """Badges are used to show notifications, counts, or status information on navigation items such as NavigationBar or NavigationRail destinations
    or a button's icon."""

    # content: Optional[Control] = None
    text: Optional[str] = None
    offset: OffsetValue = None
    alignment: Optional[Alignment] = None
    bgcolor: Optional[str] = None
    label_visible: Optional[bool] = None
    large_size: OptionalNumber = None
    padding: Optional[PaddingValue] = None
    small_size: OptionalNumber = None
    text_color: Optional[str] = None
    text_style: Optional[TextStyle] = None

    # message: Optional[str] = None
    # enable_feedback: Optional[bool] = None
    # height: OptionalNumber = None
    # vertical_offset: OptionalNumber = None
    # margin: MarginValue = None
    # padding: PaddingValue = None
    # bgcolor: Optional[str] = None
    # image: Optional[DecorationImage] = None
    # shadow: List[BoxShadow] = None
    # blend_mode: Optional[BlendMode] = None
    # gradient: Optional[Gradient] = None
    # border: Optional[Border] = None
    # border_radius: BorderRadiusValue = None
    # shape: Optional[BoxShape] = None
    # text_style: Optional[TextStyle] = None
    # text_align: Optional[TextAlign] = None
    # prefer_below: Optional[bool] = None
    # show_duration: DurationValue = None
    # wait_duration: DurationValue = None
    # exit_duration: DurationValue = None
    # enable_tap_to_dismiss: Optional[bool] = None
    # exclude_from_semantics: Optional[bool] = None
    # trigger_mode: Optional[TooltipTriggerMode] = None


BadgeValue = Optional[Union[str, "Badge"]]
