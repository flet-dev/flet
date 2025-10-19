from dataclasses import field
from typing import Optional, Union

import flet as ft
from flet_charts.line_chart_data_point import LineChartDataPoint
from flet_charts.types import ChartPointLine, ChartPointShape

__all__ = ["LineChartData"]


@ft.control("LineChartData")
class LineChartData(ft.BaseControl):
    points: list[LineChartDataPoint] = field(default_factory=list)
    """
    A list of points (dots) of [`LineChartDataPoint`][(p).]
    type representing a single chart line.
    """

    curved: bool = False
    """
    Whether to draw this chart line as a curve.
    """

    color: ft.ColorValue = ft.Colors.CYAN
    """
    A color of chart line.
    """

    gradient: Optional[ft.Gradient] = None
    """
    Gradient to draw line's background.
    """

    stroke_width: ft.Number = 2.0
    """
    The width of a chart line.
    """

    rounded_stroke_cap: bool = False
    """
    Whether to draw rounded line caps.
    """

    prevent_curve_over_shooting: bool = False
    """
    Whether to prevent overshooting when draw curve line on linear sequence spots.
    """

    prevent_curve_over_shooting_threshold: ft.Number = 10.0
    """
    Threshold for [`prevent_curve_over_shooting`][(c).] algorithm.
    """

    dash_pattern: Optional[list[int]] = None
    """
    Defines dash effect of the line. The value is a circular list of dash offsets
    and lengths. For example, the list `[5, 10]` would result in dashes 5 pixels
    long followed by blank spaces 10 pixels long. By default, a solid line is
    drawn.
    """

    shadow: ft.BoxShadow = field(
        default_factory=lambda: ft.BoxShadow(color=ft.Colors.TRANSPARENT)
    )
    """
    Shadow to drop by a chart line.
    """

    above_line_bgcolor: Optional[ft.ColorValue] = None
    """
    Fill the area above chart line with the specified
    color.
    """

    above_line_gradient: Optional[ft.Gradient] = None
    """
    Fill the area above chart line with the specified gradient.
    """

    above_line_cutoff_y: Optional[ft.Number] = None
    """
    Cut off filled area above line chart at specific Y value.
    """

    above_line: Optional[ChartPointLine] = None
    """
    A vertical line drawn between a line point and the top edge of the chart.
    """

    below_line_bgcolor: Optional[ft.ColorValue] = None
    """
    Fill the area below chart line with the specified
    color.
    """

    below_line_gradient: Optional[ft.Gradient] = None
    """
    Fill the area below chart line with the specified gradient.
    """

    below_line_cutoff_y: Optional[ft.Number] = None
    """
    Cut off filled area below line chart at specific Y value.
    """

    below_line: Optional[ChartPointLine] = None
    """
    A vertical line drawn between a line point and the bottom edge of the chart.
    """

    selected_below_line: Union[None, bool, ChartPointLine] = None
    """
    A vertical line drawn between selected line point and the bottom adge of the
    chart.

    Setting this property to `True` will draw a line with default style.
    """

    point: Union[None, bool, ChartPointShape] = None
    """
    Defines the appearance and shape of a line point (dot).

    Setting this property to `True` will draw a point with default style.
    """

    selected_point: Union[None, bool, ChartPointShape] = None
    """
    Defines the appearance and shape of a selected line point.
    """

    curve_smoothness: ft.Number = 0.35
    """
    Defines the smoothness of a curve line,
    when [`curved`][(c).] is set to `True`.
    """

    rounded_stroke_join: bool = False
    """
    Whether to draw rounded line joins.
    """

    step_direction: Optional[ft.Number] = None
    """
    Determines the direction of each step.

    If not `None`, this chart will be drawn as a
    [Step Line Chart](https://docs.anychart.com/Basic_Charts/Step_Line_Chart).

    Below are some typical values:

    - `0.0`: Go to the next spot directly, with the current point's y value.
    - `0.5`: Go to the half with the current spot y, and with the next spot y
        for the rest.
    - `1.0`: Go to the next spot y and direct line to the next spot.
    """
