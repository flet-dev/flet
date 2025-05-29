from dataclasses import field
from typing import Optional, Union

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
    data_points: list[LineChartDataPoint] = field(default_factory=list)
    """
    A list of points (dots) of
    [`LineChartDataPoint`](https://flet.dev/docs/reference/types/linechartdatapoint)
    type representing a single chart line.
    """

    curved: Optional[bool] = None
    """
    Set to `True` to draw chart line as a curve.

    Defaults to `False`.
    """

    color: OptionalColorValue = None
    """
    A [color](https://flet.dev/docs/reference/colors) of chart line.
    """

    gradient: Optional[Gradient] = None
    """
    Gradient to draw line's background.

    Value is of type [`Gradient`](https://flet.dev/docs/reference/types/gradient).
    """

    stroke_width: OptionalNumber = None
    """
    The width of a chart line.
    """

    stroke_cap_round: Optional[bool] = None
    """
    Set to `True` to draw rounded line caps.

    Defaults to `False`.
    """

    prevent_curve_over_shooting: Optional[bool] = None
    """
    Whether to prevent overshooting when draw curve line on linear sequence spots.

    Defaults to `False`.
    """

    prevent_curve_over_shooting_threshold: OptionalNumber = None
    """
    Threshold to prevent overshooting algorithm.

    Defaults to `10.0`.
    """

    dash_pattern: Optional[list[int]] = None
    """
    Defines dash effect of the line. The value is a circular list of dash offsets
    and lengths. For example, the list `[5, 10]` would result in dashes 5 pixels
    long followed by blank spaces 10 pixels long. By default, a solid line is
    drawn.
    """

    shadow: Optional[BoxShadow] = None
    """
    Shadow to drop by a chart line.

    Value is of type [`BoxShadow`](https://flet.dev/docs/reference/types/boxshadow).
    """

    above_line_bgcolor: OptionalColorValue = None
    """
    Fill the area above chart line with the specified
    [color](https://flet.dev/docs/reference/colors).
    """

    above_line_gradient: Optional[Gradient] = None
    """
    Fill the area above chart line with the specified gradient.
    """

    above_line_cutoff_y: OptionalNumber = None
    """
    Cut off filled area above line chart at specific Y value.
    """

    above_line: Optional[ChartPointLine] = None
    """
    A vertical line drawn between a line point and the top edge of the chart.

    Value is of type [`ChartPointLine`](https://flet.dev/docs/reference/types/chartpointline).
    """

    below_line_bgcolor: OptionalColorValue = None
    """
    Fill the area below chart line with the specified
    [color](https://flet.dev/docs/reference/colors).
    """

    below_line_gradient: Optional[Gradient] = None
    """
    Fill the area below chart line with the specified gradient.
    """

    below_line_cutoff_y: OptionalNumber = None
    """
    Cut off filled area below line chart at specific Y value.
    """

    below_line: Optional[ChartPointLine] = None
    """
    A vertical line drawn between a line point and the bottom edge of the chart.

    Value is of type [`ChartPointLine`](https://flet.dev/docs/reference/types/chartpointline).
    """

    selected_below_line: Union[None, bool, ChartPointLine] = None
    """
    A vertical line drawn between selected line point and the bottom adge of the
    chart. The value is either `True` - draw a line with default style, `False` - do
    not draw a line under selected point, or an instance of
    [`ChartPointLine`](https://flet.dev/docs/reference/types/chartpointline) class to
    specify line style to draw.
    """

    point: Union[None, bool, ChartPointShape] = None
    """
    Defines the appearance and shape of a line point (dot).

    Value is of type bool (`True` - draw a point with default style or `False` - do
    not draw a line point) or of type
    [`ChartPointShape`](https://flet.dev/docs/reference/types/chartpointshape).
    """

    selected_point: Union[None, bool, ChartPointShape] = None
    """
    Defines the appearance and shape of a selected line point.

    Value is of type [`ChartPointShape`](https://flet.dev/docs/reference/types/chartpointshape).
    """
