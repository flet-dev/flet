from typing import Any, List, Optional, Union

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.core.charts.chart_point_shape import ChartPointShape
from flet.controls.core.text_span import TextSpan
from flet.controls.text_style import TextStyle
from flet.controls.types import OptionalColorValue, OptionalNumber, TextAlign


@control("s")
class ScatterChartSpot(Control):
    x: OptionalNumber = None
    y: OptionalNumber = None
    show: Optional[bool] = None
    radius: OptionalNumber = None
    color: OptionalColorValue = None
    render_priority: OptionalNumber = None
    x_error: Optional[Any] = None
    y_error: Optional[Any] = None
    selected: Optional[bool] = None
    show_tooltip: Optional[bool] = None
    tooltip_text: Optional[str] = None
    tooltip_style: Optional[TextStyle] = None
    tooltip_align: Optional[TextAlign] = None
    tooltip_spans: Optional[List[TextSpan]] = None
    tooltip_bgcolor: OptionalColorValue = None
    point: Union[None, bool, ChartPointShape] = None
