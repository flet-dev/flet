from dataclasses import field
from typing import List, Optional

from flet.controls.border import BorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.control import Control, control
from flet.controls.core.charts.bar_chart_rod_stack_item import BarChartRodStackItem
from flet.controls.gradients import Gradient
from flet.controls.text_style import TextStyle
from flet.controls.types import OptionalColorValue, OptionalNumber, TextAlign


@control("r", kw_only=True)
class BarChartRod(Control):
    rod_stack_items: List[BarChartRodStackItem] = field(default_factory=list)
    from_y: OptionalNumber = None
    to_y: OptionalNumber = None
    width: OptionalNumber = None
    color: OptionalColorValue = None
    gradient: Optional[Gradient] = None
    border_radius: OptionalBorderRadiusValue = None
    border_side: Optional[BorderSide] = None
    bg_from_y: OptionalNumber = None
    bg_to_y: OptionalNumber = None
    bg_color: OptionalColorValue = None
    bg_gradient: Optional[Gradient] = None
    selected: Optional[bool] = None
    show_tooltip: Optional[bool] = None
    tooltip: Optional[str] = None
    tooltip_style: Optional[TextStyle] = None
    tooltip_align: Optional[TextAlign] = None
