from typing import Optional

from flet.controls.border import BorderSide
from flet.controls.control import Control, control
from flet.controls.text_style import TextStyle
from flet.controls.types import OptionalColorValue, OptionalNumber


@control("s")
class PieChartSection(Control):
    value: OptionalNumber = None
    radius: OptionalNumber = None
    color: OptionalColorValue = None
    border_side: Optional[BorderSide] = None
    title: Optional[str] = None
    title_style: Optional[TextStyle] = None
    title_position: OptionalNumber = None
    badge: Optional[Control] = None
    badge_position: OptionalNumber = None
