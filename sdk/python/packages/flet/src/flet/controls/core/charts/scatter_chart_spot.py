from typing import Any, Optional, Union

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.core.charts.chart_point_shape import ChartPointShape
from flet.controls.core.text_span import TextSpan
from flet.controls.text_style import TextStyle
from flet.controls.types import Number, OptionalColorValue, OptionalNumber, TextAlign


@control("s")
class ScatterChartSpot(Control):
    x: OptionalNumber = None
    """
    The position of a spot on `X` axis.
    """
    y: OptionalNumber = None
    """
    The position of a spot on `Y` axis.
    """
    show: bool = True
    """
    Determines wether to show or hide the spot.
    """
    radius: OptionalNumber = None
    """
    Radius of a spot.
    """
    color: OptionalColorValue = None
    """
    Color of a spot.
    """
    render_priority: Number = 0
    """
    Sort by this to manage overlap.
    """
    x_error: Optional[Any] = None
    """
    Determines the error range of the data point using 
    (FlErrorRange)[https://github.com/imaNNeo/fl_chart/blob/main/repo_files/documentations/base_chart.md#flerrorrange] 
    (which ontains lowerBy and upperValue) for the `X` axis.
    """
    y_error: Optional[Any] = None
    """
    Determines the error range of the data point using 
    (FlErrorRange)[https://github.com/imaNNeo/fl_chart/blob/main/repo_files/documentations/base_chart.md#flerrorrange] 
    (which ontains lowerBy and upperValue) for the `Y` axis.
    """
    selected: bool = False
    """
    TBD
    """
    show_tooltip: bool = True
    """
    Wether to show tooltip.
    """
    tooltip_text: Optional[str] = None
    """
    Text string of each row in the tooltip bubble.
    """
    tooltip_style: Optional[TextStyle] = None
    """
    TextStyle of the showing text row.
    """
    tooltip_align: Optional[TextAlign] = None
    """
    Tooltip text horizontal align.
    """
    tooltip_spans: Optional[list[TextSpan]] = None
    """
    TextSpans to show on a tooltip.
    """
    tooltip_bgcolor: OptionalColorValue = None
    """
    Background color of the tooltip bubble.
    """
    label_text: Optional[str] = None
    """
    TBD
    """
    label_style: Optional[TextStyle] = None
    """
    TBD
    """
    point: Union[None, bool, ChartPointShape] = None
    """
    TBD
    """
