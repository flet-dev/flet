from dataclasses import field
from typing import List, Optional, Union

from flet.controls.base_control import control
from flet.controls.box import BoxShadow
from flet.controls.control import Control
from flet.controls.core.charts.chart_point_line import ChartPointLine
from flet.controls.core.charts.chart_point_shape import ChartPointShape
from flet.controls.core.charts.line_chart_data_point import LineChartDataPoint
from flet.controls.gradients import Gradient
from flet.controls.types import OptionalColorValue, OptionalNumber


@control("d")
class LineChartData(Control):
    data_points: List[LineChartDataPoint] = field(default_factory=list)
    curved: Optional[bool] = None
    color: OptionalColorValue = None
    gradient: Optional[Gradient] = None
    stroke_width: OptionalNumber = None
    stroke_cap_round: Optional[bool] = None
    prevent_curve_over_shooting: Optional[bool] = None
    prevent_curve_over_shooting_threshold: OptionalNumber = None
    dash_pattern: Optional[List[int]] = None
    shadow: Optional[BoxShadow] = None
    above_line_bgcolor: OptionalColorValue = None
    above_line_gradient: Optional[Gradient] = None
    above_line_cutoff_y: OptionalNumber = None
    above_line: Optional[ChartPointLine] = None
    below_line_bgcolor: OptionalColorValue = None
    below_line_gradient: Optional[Gradient] = None
    below_line_cutoff_y: OptionalNumber = None
    below_line: Optional[ChartPointLine] = None
    selected_below_line: Union[None, bool, ChartPointLine] = None
    point: Union[None, bool, ChartPointShape] = None
    selected_point: Union[None, bool, ChartPointShape] = None
