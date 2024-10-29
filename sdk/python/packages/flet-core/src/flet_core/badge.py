from dataclasses import dataclass
from typing import Optional, Union

from flet_core.alignment import Alignment
from flet_core.text_style import TextStyle
from flet_core.types import OffsetValue, OptionalNumber, PaddingValue


@dataclass
class Badge:
    """Badges are used to show notifications, counts, or status information on navigation items such as NavigationBar or NavigationRail destinations
    or a button's icon."""

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


BadgeValue = Union[str, "Badge"]
