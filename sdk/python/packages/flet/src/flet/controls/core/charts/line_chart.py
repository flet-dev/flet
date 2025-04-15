from dataclasses import dataclass, field
from typing import Any, List, Optional

from flet.controls.animation import AnimationValue
from flet.controls.border import Border, BorderSide
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import control
from flet.controls.control_event import ControlEvent
from flet.controls.core.charts.chart_axis import ChartAxis
from flet.controls.core.charts.chart_grid_lines import ChartGridLines
from flet.controls.core.charts.line_chart_data import LineChartData
from flet.controls.padding import OptionalPaddingValue
from flet.controls.ref import Ref
from flet.controls.types import (
    OptionalColorValue,
    OptionalEventCallable,
    OptionalNumber,
)


@dataclass
class LineChartEventSpot:
    bar_index: int
    spot_index: int


@dataclass
class LineChartEvent(ControlEvent):
    type: str
    spots: List[LineChartEventSpot]


@control("LineChart")
class LineChart(ConstrainedControl):
    data_series: List[LineChartData] = field(default_factory=list)
    animate: Optional[AnimationValue] = None
    interactive: Optional[bool] = None
    point_line_start: OptionalNumber = None
    point_line_end: OptionalNumber = None
    bgcolor: OptionalColorValue = None
    tooltip_bgcolor: OptionalColorValue = None
    border: Optional[Border] = None
    horizontal_grid_lines: Optional[ChartGridLines] = None
    vertical_grid_lines: Optional[ChartGridLines] = None
    left_axis: Optional[ChartAxis] = None
    top_axis: Optional[ChartAxis] = None
    right_axis: Optional[ChartAxis] = None
    bottom_axis: Optional[ChartAxis] = None
    baseline_x: OptionalNumber = None
    min_x: OptionalNumber = None
    max_x: OptionalNumber = None
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
    tooltip_show_on_top_of_chart_box_area: Optional[bool] = None
    _skip_inherited_notifier: Optional[bool] = None
    on_chart_event: OptionalEventCallable[LineChartEvent] = None

    def init(self):
        super().init()
        self._skip_inherited_notifier = True
