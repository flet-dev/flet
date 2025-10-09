from dataclasses import dataclass, field
from typing import Any, Optional

import flet as ft
from flet_charts.chart_axis import ChartAxis
from flet_charts.line_chart_data import LineChartData
from flet_charts.types import ChartEventType, ChartGridLines, HorizontalAlignment

__all__ = [
    "LineChart",
    "LineChartEvent",
    "LineChartEventSpot",
    "LineChartTooltip",
]


@dataclass
class LineChartEventSpot:
    bar_index: int
    """
    The line's index or `-1` if no line was hovered.
    """

    spot_index: int
    """
    The line's point index or `-1` if no point was hovered.
    """

    def copy(
        self,
        *,
        bar_index: Optional[int] = None,
        spot_index: Optional[int] = None,
    ) -> "LineChartEventSpot":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return LineChartEventSpot(
            bar_index=bar_index if bar_index is not None else self.bar_index,
            spot_index=spot_index if spot_index is not None else self.spot_index,
        )


@dataclass
class LineChartEvent(ft.Event["LineChart"]):
    type: ChartEventType
    """
    The type of event that occured.
    """

    spots: list[LineChartEventSpot]
    """
    Spots on which the event occurred.
    """


@dataclass
class LineChartTooltip:
    """Configuration of the tooltip for [`LineChart`][(p).]s."""

    bgcolor: ft.ColorValue = "#FF607D8B"
    """
    Background color of tooltip.
    """

    border_radius: Optional[ft.BorderRadiusValue] = None
    """
    The tooltip's border radius.
    """

    margin: ft.Number = 16
    """
    Applies a bottom margin for showing tooltip on top of rods.
    """

    padding: ft.PaddingValue = field(
        default_factory=lambda: ft.Padding.symmetric(vertical=8, horizontal=16)
    )
    """
    Applies a padding for showing contents inside the tooltip.
    """

    max_width: ft.Number = 120
    """
    Restricts the tooltip's width.
    """

    rotation: ft.Number = 0.0
    """
    The tooltip's rotation angle in degrees.
    """

    horizontal_offset: ft.Number = 0.0
    """
    Applies horizontal offset for showing tooltip.
    """

    border_side: ft.BorderSide = field(default_factory=lambda: ft.BorderSide.none())
    """
    Defines the borders of this tooltip.
    """

    fit_inside_horizontally: bool = False
    """
    Forces the tooltip to shift horizontally inside the chart, if overflow happens.
    """

    fit_inside_vertically: bool = False
    """
    Forces the tooltip to shift vertically inside the chart, if overflow happens.
    """

    show_on_top_of_chart_box_area: bool = False
    """
    Whether to force the tooltip container to top of the line.
    """

    horizontal_alignment: HorizontalAlignment = HorizontalAlignment.CENTER
    """
    The horizontal alignment of this tooltip.
    """

    def copy(
        self,
        *,
        bgcolor: Optional[ft.ColorValue] = None,
        border_radius: Optional[ft.BorderRadiusValue] = None,
        margin: Optional[ft.Number] = None,
        padding: Optional[ft.PaddingValue] = None,
        max_width: Optional[ft.Number] = None,
        rotation: Optional[ft.Number] = None,
        horizontal_offset: Optional[ft.Number] = None,
        border_side: Optional[ft.BorderSide] = None,
        fit_inside_horizontally: Optional[bool] = None,
        fit_inside_vertically: Optional[bool] = None,
        show_on_top_of_chart_box_area: Optional[bool] = None,
    ) -> "LineChartTooltip":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return LineChartTooltip(
            bgcolor=bgcolor if bgcolor is not None else self.bgcolor,
            border_radius=border_radius
            if border_radius is not None
            else self.border_radius,
            margin=margin if margin is not None else self.margin,
            padding=padding if padding is not None else self.padding,
            max_width=max_width if max_width is not None else self.max_width,
            rotation=rotation if rotation is not None else self.rotation,
            horizontal_offset=horizontal_offset
            if horizontal_offset is not None
            else self.horizontal_offset,
            border_side=border_side if border_side is not None else self.border_side,
            fit_inside_horizontally=fit_inside_horizontally
            if fit_inside_horizontally is not None
            else self.fit_inside_horizontally,
            fit_inside_vertically=fit_inside_vertically
            if fit_inside_vertically is not None
            else self.fit_inside_vertically,
            show_on_top_of_chart_box_area=show_on_top_of_chart_box_area
            if show_on_top_of_chart_box_area is not None
            else self.show_on_top_of_chart_box_area,
        )


@ft.control("LineChart")
class LineChart(ft.LayoutControl):
    """
    Draws a line chart.
    """

    data_series: list[LineChartData] = field(default_factory=list)
    """
    A list of [`LineChartData`][(p).]
    controls drawn as separate lines on a chart.
    """

    animation: ft.AnimationValue = field(
        default_factory=lambda: ft.Animation(
            duration=ft.Duration(milliseconds=150), curve=ft.AnimationCurve.LINEAR
        )
    )
    """
    Controls chart implicit animation.
    """

    interactive: bool = True
    """
    Enables automatic tooltips and points highlighting when hovering over the chart.
    """

    point_line_start: Optional[ft.Number] = None
    """
    The start of the vertical line drawn under the selected point.

    Defaults to chart's bottom edge.
    """

    point_line_end: Optional[ft.Number] = None
    """
    The end of the vertical line drawn at selected point position.

    Defaults to data point's `y` value.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    Background color of the chart.
    """

    border: Optional[ft.Border] = None
    """
    The border around the chart.
    """

    horizontal_grid_lines: Optional[ChartGridLines] = None
    """
    Controls drawing of chart's horizontal lines.
    """

    vertical_grid_lines: Optional[ChartGridLines] = None
    """
    Controls drawing of chart's vertical lines.
    """

    left_axis: Optional[ChartAxis] = None
    """
    Defines the appearance of the left axis, its title and labels.
    """

    top_axis: Optional[ChartAxis] = None
    """
    Defines the appearance of the top axis, its title and labels.
    """

    right_axis: Optional[ChartAxis] = None
    """
    Defines the appearance of the right axis, its title and labels.
    """

    bottom_axis: Optional[ChartAxis] = None
    """
    Defines the appearance of the bottom axis, its title and labels.
    """

    baseline_x: Optional[ft.Number] = None
    """
    Baseline value for X axis.
    """

    min_x: Optional[ft.Number] = None
    """
    Defines the minimum displayed value for X axis.
    """

    max_x: Optional[ft.Number] = None
    """
    Defines the maximum displayed value for X axis.
    """

    baseline_y: Optional[ft.Number] = None
    """
    Baseline value for Y axis.
    """

    min_y: Optional[ft.Number] = None
    """
    Defines the minimum displayed value for Y axis.
    """

    max_y: Optional[ft.Number] = None
    """
    Defines the maximum displayed value for Y axis.
    """

    tooltip: Optional[LineChartTooltip] = field(
        default_factory=lambda: LineChartTooltip()
    )
    """
    The tooltip configuration for this chart.

    If set to `None`, no tooltips will be shown throughout this chart.
    """

    on_event: Optional[ft.EventHandler[LineChartEvent]] = None
    """
    Fires when a chart line is hovered or clicked.
    """

    def __post_init__(self, ref: Optional[ft.Ref[Any]]):
        super().__post_init__(ref)
        self._internals["skip_properties"] = ["tooltip"]
        self._internals["skip_inherited_notifier"] = True
