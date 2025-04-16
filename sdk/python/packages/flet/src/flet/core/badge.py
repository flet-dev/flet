from dataclasses import dataclass
from typing import Optional, Union

from flet.core.alignment import Alignment
from flet.core.text_style import TextStyle
from flet.core.types import ColorValue, OffsetValue, OptionalNumber, PaddingValue


@dataclass
class Badge:
    """Badges are used to show notifications, counts, or status information on navigation items such as NavigationBar or NavigationRail destinations
    or a button's icon."""

    text: Optional[str] = None
    offset: Optional[OffsetValue] = None
    alignment: Optional[Alignment] = None
    bgcolor: Optional[ColorValue] = None
    label_visible: Optional[bool] = None
    large_size: OptionalNumber = None
    padding: Optional[PaddingValue] = None
    small_size: OptionalNumber = None
    text_color: Optional[ColorValue] = None
    text_style: Optional[TextStyle] = None


BadgeValue = Union[str, "Badge"]
