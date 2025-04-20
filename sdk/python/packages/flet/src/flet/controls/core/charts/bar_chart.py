from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.border import Border, BorderSide
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEvent
from flet.controls.core.charts.bar_chart_group import BarChartGroup
from flet.controls.core.charts.chart_axis import ChartAxis
from flet.controls.core.charts.chart_grid_lines import ChartGridLines
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    OptionalColorValue,
    OptionalEventCallable,
    OptionalNumber,
)


class TooltipDirection(Enum):
    AUTO = "auto"
    TOP = "top"
    BOTTOM = "bottom"


@dataclass
class BarChartEvent(ControlEvent):
    type: str
    group_index: Optional[int] = None
    rod_index: Optional[int] = None
    stack_item_index: Optional[int] = None


@control("BarChart")
class BarChart(ConstrainedControl):
    bar_groups: List[BarChartGroup] = field(default_factory=list)
    groups_space: OptionalNumber = None
    animate: Optional[AnimationValue] = None
    interactive: Optional[bool] = None
    bgcolor: OptionalColorValue = None
    tooltip_bgcolor: OptionalColorValue = None
    border: Optional[Border] = None
    horizontal_grid_lines: Optional[ChartGridLines] = None
    vertical_grid_lines: Optional[ChartGridLines] = None
    left_axis: Optional[ChartAxis] = None
    top_axis: Optional[ChartAxis] = None
    right_axis: Optional[ChartAxis] = None
    bottom_axis: Optional[ChartAxis] = None
    baseline_y: OptionalNumber = None
    min_y: OptionalNumber = None
    max_y: OptionalNumber = None
    tooltip_rounded_radius: OptionalNumber = None
    tooltip_margin: OptionalNumber = None
    tooltip_padding: OptionalPaddingValue = None
    tooltip_max_content_width: OptionalNumber = None
    tooltip_rotate_angle: OptionalNumber = None
    tooltip_tooltip_horizontal_offset: OptionalNumber = None
    tooltip_tooltip_border_side: Optional[BorderSide] = None
    tooltip_fit_inside_horizontally: Optional[bool] = None
    tooltip_fit_inside_vertically: Optional[bool] = None
    tooltip_direction: Optional[TooltipDirection] = None
    on_chart_event: OptionalEventCallable["BarChartEvent"] = None
