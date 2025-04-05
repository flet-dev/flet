from typing import Optional, Union

from flet.controls.control import Control, control
from flet.controls.core.charts.chart_point_line import ChartPointLine
from flet.controls.core.charts.chart_point_shape import ChartPointShape
from flet.controls.text_style import TextStyle
from flet.controls.types import OptionalNumber, TextAlign


@control("p")
class LineChartDataPoint(Control):
    x: OptionalNumber = None
    y: OptionalNumber = None
    selected: Optional[bool] = None
    show_tooltip: Optional[bool] = None
    tooltip: Optional[str] = None
    tooltip_style: Optional[TextStyle] = None
    tooltip_align: Optional[TextAlign] = None
    point: Union[None, bool, ChartPointShape] = None
    selected_point: Union[None, bool, ChartPointShape] = None
    show_above_line: Optional[bool] = None
    show_below_line: Optional[bool] = None
    selected_below_line: Union[None, bool, ChartPointLine] = None
