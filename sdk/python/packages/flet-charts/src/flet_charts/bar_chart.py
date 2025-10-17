from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

import flet as ft
from flet_charts.bar_chart_group import BarChartGroup
from flet_charts.chart_axis import ChartAxis
from flet_charts.types import ChartEventType, ChartGridLines, HorizontalAlignment

__all__ = [
    "BarChart",
    "BarChartEvent",
    "BarChartTooltip",
    "BarChartTooltipDirection",
]


class BarChartTooltipDirection(Enum):
    """Controls showing tooltip on top or bottom."""

    AUTO = "auto"
    """Tooltip shows on top if value is positive, on bottom if value is negative."""

    TOP = "top"
    """Tooltip always shows on top."""

    BOTTOM = "bottom"
    """Tooltip always shows on bottom."""


@dataclass
class BarChartTooltip:
    """Configuration of the tooltip for [`BarChart`][(p).]s."""

    bgcolor: ft.ColorValue = ft.Colors.SECONDARY
    """
    Background color of tooltips.
    """

    border_radius: Optional[ft.BorderRadiusValue] = None
    """
    The border radius of the tooltip.
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

    max_width: Optional[ft.Number] = None
    """
    Restricts the tooltip's width.
    """

    rotation: ft.Number = 0.0
    """
    The rotation angle of the tooltip.
    """

    horizontal_offset: ft.Number = 0.0
    """
    The horizontal offset of this tooltip.
    """

    border_side: Optional[ft.BorderSide] = None
    """
    The tooltip border side.
    """

    fit_inside_horizontally: bool = False
    """
    Forces the tooltip to shift horizontally inside the chart, if overflow happens.
    """

    fit_inside_vertically: bool = False
    """
    Forces the tooltip to shift vertically inside the chart, if overflow happens.
    """

    direction: BarChartTooltipDirection = BarChartTooltipDirection.AUTO
    """
    Defines the direction of this tooltip.
    """

    horizontal_alignment: HorizontalAlignment = HorizontalAlignment.CENTER
    """
    Defines the horizontal alignment of this tooltip.
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
        direction: Optional[BarChartTooltipDirection] = None,
        horizontal_alignment: Optional[HorizontalAlignment] = None,
    ) -> "BarChartTooltip":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return BarChartTooltip(
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
            direction=direction if direction is not None else self.direction,
            horizontal_alignment=horizontal_alignment
            if horizontal_alignment is not None
            else self.horizontal_alignment,
        )


@dataclass
class BarChartEvent(ft.Event["BarChart"]):
    type: ChartEventType
    """
    The type of event that occurred on the chart.
    """

    group_index: Optional[int] = None
    """
    Bar's index or `-1` if chart is hovered or clicked outside of any bar.
    """

    rod_index: Optional[int] = None
    """
    Rod's index or `-1` if chart is hovered or clicked outside of any bar.
    """

    stack_item_index: Optional[int] = None
    """
    Stack item's index or `-1` if chart is hovered or clicked outside of any bar.
    """


@ft.control("BarChart")
class BarChart(ft.LayoutControl):
    """
    Draws a bar chart.
    """

    groups: list[BarChartGroup] = field(default_factory=list)
    """
    The list of [`BarChartGroup`][(p).]s to draw.
    """

    group_spacing: ft.Number = 16.0
    """
    An amount of space between bar [`groups`][(c).].
    """

    group_alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.SPACE_EVENLY
    """
    The alignment of the bar [`groups`][(c).] within this chart.

    If set to [`MainAxisAlignment.CENTER`][flet.MainAxisAlignment.CENTER],
    the space between the `groups` can be specified using [`group_spacing`][(c).].
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
    The appearance of the left axis, its title and labels.
    """

    top_axis: Optional[ChartAxis] = None
    """
    The appearance of the top axis, its title and labels.
    """

    right_axis: Optional[ChartAxis] = None
    """
    The appearance of the right axis, its title and labels.
    """

    bottom_axis: Optional[ChartAxis] = None
    """
    The appearance of the bottom axis, its title and labels.
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

    tooltip: Optional[BarChartTooltip] = field(
        default_factory=lambda: BarChartTooltip()
    )
    """
    The tooltip configuration for this chart.

    If set to `None`, tooltips will not shown throughout this chart.
    """

    on_event: Optional[ft.EventHandler[BarChartEvent]] = None
    """
    Called when an event occurs on this chart, such as a click or hover.
    """

    def __post_init__(self, ref: Optional[ft.Ref[Any]]):
        super().__post_init__(ref)
        self._internals["skip_properties"] = ["tooltip"]
