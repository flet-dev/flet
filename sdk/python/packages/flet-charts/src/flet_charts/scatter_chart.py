from dataclasses import dataclass, field
from typing import Any, Optional

import flet as ft
from flet_charts.chart_axis import ChartAxis
from flet_charts.scatter_chart_spot import ScatterChartSpot
from flet_charts.types import ChartEventType, ChartGridLines, HorizontalAlignment

__all__ = ["ScatterChart", "ScatterChartEvent", "ScatterChartTooltip"]


@dataclass
class ScatterChartTooltip:
    """Configuration of the tooltip for [`ScatterChart`][(p).]s."""

    bgcolor: ft.ColorValue = "#FF607D8B"
    """
    The tooltip's background color.
    """

    border_radius: Optional[ft.BorderRadiusValue] = None
    """
    The tooltip's border radius.
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

    horizontal_offset: ft.Number = 0
    """
    Applies horizontal offset for showing tooltip.
    """

    horizontal_alignment: HorizontalAlignment = HorizontalAlignment.CENTER
    """
    The tooltip's horizontal alignment.
    """

    border_side: ft.BorderSide = field(default_factory=lambda: ft.BorderSide.none())
    """
    The tooltip's border side.
    """

    fit_inside_horizontally: bool = False
    """
    Forces the tooltip to shift horizontally inside the chart, if overflow happens.
    """

    fit_inside_vertically: bool = False
    """
    Forces the tooltip to shift vertically inside the chart, if overflow happens.
    """

    def copy(
        self,
        *,
        bgcolor: Optional[ft.ColorValue] = None,
        border_radius: Optional[ft.BorderRadiusValue] = None,
        padding: Optional[ft.PaddingValue] = None,
        max_width: Optional[ft.Number] = None,
        rotation: Optional[ft.Number] = None,
        horizontal_offset: Optional[ft.Number] = None,
        horizontal_alignment: Optional[HorizontalAlignment] = None,
        border_side: Optional[ft.BorderSide] = None,
        fit_inside_horizontally: Optional[bool] = None,
        fit_inside_vertically: Optional[bool] = None,
    ) -> "ScatterChartTooltip":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return ScatterChartTooltip(
            bgcolor=bgcolor if bgcolor is not None else self.bgcolor,
            border_radius=border_radius
            if border_radius is not None
            else self.border_radius,
            padding=padding if padding is not None else self.padding,
            max_width=max_width if max_width is not None else self.max_width,
            rotation=rotation if rotation is not None else self.rotation,
            horizontal_offset=horizontal_offset
            if horizontal_offset is not None
            else self.horizontal_offset,
            horizontal_alignment=horizontal_alignment
            if horizontal_alignment is not None
            else self.horizontal_alignment,
            border_side=border_side if border_side is not None else self.border_side,
            fit_inside_horizontally=fit_inside_horizontally
            if fit_inside_horizontally is not None
            else self.fit_inside_horizontally,
            fit_inside_vertically=fit_inside_vertically
            if fit_inside_vertically is not None
            else self.fit_inside_vertically,
        )


@dataclass
class ScatterChartEvent(ft.Event["ScatterChart"]):
    type: ChartEventType
    """
    The type of the event that occurred.
    """

    spot_index: Optional[int] = None
    """
    The index of the touched spot, if any.
    """


@ft.control("ScatterChart")
class ScatterChart(ft.LayoutControl):
    """
    A scatter chart control.

    ScatterChart draws some points in a square space,
    points are defined by [`ScatterChartSpot`][(p).]s.
    """

    spots: list[ScatterChartSpot] = field(default_factory=list)
    """
    List of [`ScatterChartSpot`][(p).]s to show on the chart.
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
    Enables automatic tooltips when hovering chart bars.
    """

    long_press_duration: Optional[ft.DurationValue] = None
    """
    The duration of a long press on the chart.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The chart's background color.
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
    Configures the appearance of the left axis, its title and labels.
    """

    top_axis: Optional[ChartAxis] = None
    """
    Configures the appearance of the top axis, its title and labels.
    """

    right_axis: Optional[ChartAxis] = None
    """
    Configures the appearance of the right axis, its title and labels.
    """

    bottom_axis: Optional[ChartAxis] = None
    """
    Configures the appearance of the bottom axis, its title and labels.
    """

    baseline_x: Optional[ft.Number] = None
    """
    The baseline value for X axis.
    """

    min_x: Optional[ft.Number] = None
    """
    The minimum displayed value for X axis.
    """

    max_x: Optional[ft.Number] = None
    """
    The maximum displayed value for X axis.
    """

    baseline_y: Optional[ft.Number] = None
    """
    Baseline value for Y axis.
    """

    min_y: Optional[ft.Number] = None
    """
    The minimum displayed value for Y axis.
    """

    max_y: Optional[ft.Number] = None
    """
    The maximum displayed value for Y axis.
    """

    tooltip: ScatterChartTooltip = field(default_factory=lambda: ScatterChartTooltip())
    """
    The tooltip configuration for the chart.
    """

    show_tooltips_for_selected_spots_only: bool = False
    """
    Whether to permanently and only show the tooltips of spots with their
    [`selected`][(p).ScatterChartSpot.selected] property set to `True`.
    """

    rotation_quarter_turns: ft.Number = 0
    """
    Number of quarter turns (90-degree increments) to rotate the chart.
    Ex: `1` rotates the chart `90` degrees clockwise,
    `2` rotates `180` degrees and `0` for no rotation.
    """

    on_event: Optional[ft.EventHandler[ScatterChartEvent]] = None
    """
    Called when an event occurs on this chart.
    """

    def __post_init__(self, ref: Optional[ft.Ref[Any]]):
        super().__post_init__(ref)
        self._internals["skip_properties"] = ["tooltip"]
