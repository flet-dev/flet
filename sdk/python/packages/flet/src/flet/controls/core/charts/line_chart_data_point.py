from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.core.charts.chart_point_line import ChartPointLine
from flet.controls.core.charts.chart_point_shape import ChartPointShape
from flet.controls.text_style import TextStyle
from flet.controls.types import OptionalNumber, TextAlign


@control("p")
class LineChartDataPoint(Control):
    x: OptionalNumber = None
    """
    The position of a point on `X` axis.
    """

    y: OptionalNumber = None
    """
    The position of a point on `Y` axis.
    """

    selected: Optional[bool] = None
    """
    Draw the point as selected when `LineChart.interactive` is set to False.
    """

    show_tooltip: Optional[bool] = None
    """
    Whether a tooltip should be shown on top of hovered data point.

    Defaults to `True`.
    """

    tooltip_text: Optional[str] = None
    """
    A custom tooltip value.

    Default is `y`.
    """

    tooltip_style: Optional[TextStyle] = None
    """
    A text style to display tooltip with.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    tooltip_align: Optional[TextAlign] = None
    """
    An align for the tooltip.

    Value is of type [`TextAlign`](https://flet.dev/docs/reference/types/textalign).
    """

    point: Union[None, bool, ChartPointShape] = None
    """
    Defines the appearance and shape of a line point.

    Value is of type [`ChartPointShape`](https://flet.dev/docs/reference/types/chartpointshape).
    """

    selected_point: Union[None, bool, ChartPointShape] = None
    """
    Defines the appearance and shape of a selected line point.

    Value is of type [`ChartPointShape`](https://flet.dev/docs/reference/types/chartpointshape).
    """

    show_above_line: Optional[bool] = None
    """
    Whether to display a line above data point.

    Defaults to `True`.
    """

    show_below_line: Optional[bool] = None
    """
    Whether to display a line below data point.

    Defaults to `True`.
    """

    selected_below_line: Union[None, bool, ChartPointLine] = None
    """
    A vertical line drawn between selected line point and the bottom adge of the chart.

    The value is either `True` - draw a line with default style, `False` - do not draw a
    line under selected point, or an instance of
    [`ChartPointLine`](https://flet.dev/docs/reference/types/chartpointline) class to
    specify line style to draw.
    """
