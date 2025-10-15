from dataclasses import dataclass, field
from typing import Any, Optional

import flet as ft
from flet_charts.candlestick_chart_spot import CandlestickChartSpot
from flet_charts.chart_axis import ChartAxis
from flet_charts.types import ChartEventType, ChartGridLines, HorizontalAlignment

__all__ = [
    "CandlestickChart",
    "CandlestickChartEvent",
    "CandlestickChartTooltip",
]


@dataclass
class CandlestickChartTooltip:
    """Configuration of the tooltip for [`CandlestickChart`][(p).]s."""

    bgcolor: ft.ColorValue = "#FFFFECEF"
    """
    Background color applied to the tooltip bubble.
    """

    border_radius: ft.BorderRadiusValue = field(
        default_factory=lambda: ft.BorderRadius.all(4)
    )
    """
    Corner radius of the tooltip bubble.
    """

    padding: ft.PaddingValue = field(
        default_factory=lambda: ft.Padding.symmetric(vertical=8, horizontal=16)
    )
    """
    Padding inside the tooltip bubble.
    """

    max_width: ft.Number = 120
    """
    Maximum width of the tooltip bubble.
    """

    rotation: ft.Number = 0.0
    """
    Rotation angle (in degrees) applied to the tooltip bubble.
    """

    horizontal_offset: ft.Number = 0
    """
    Horizontal offset applied to the tooltip bubble.
    """

    horizontal_alignment: HorizontalAlignment = HorizontalAlignment.CENTER
    """
    Horizontal alignment of the tooltip relative to the tapped candlestick.
    """

    border_side: ft.BorderSide = field(default_factory=lambda: ft.BorderSide.none())
    """
    The tooltip bubble border.
    """

    fit_inside_horizontally: bool = False
    """
    Forces the tooltip bubble to remain inside the chart horizontally.
    """

    fit_inside_vertically: bool = False
    """
    Forces the tooltip bubble to remain inside the chart vertically.
    """

    show_on_top_of_chart_box_area: bool = False
    """
    When set to `True`, the tooltip is drawn at the top of the chart box.
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
        show_on_top_of_chart_box_area: Optional[bool] = None,
    ) -> "CandlestickChartTooltip":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return CandlestickChartTooltip(
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
            show_on_top_of_chart_box_area=show_on_top_of_chart_box_area
            if show_on_top_of_chart_box_area is not None
            else self.show_on_top_of_chart_box_area,
        )


@dataclass
class CandlestickChartEvent(ft.Event["CandlestickChart"]):
    """Event raised for interactions with a [`CandlestickChart`][(p).]."""

    type: ChartEventType
    """
    Type of pointer gesture that triggered the event.
    """

    spot_index: Optional[int] = None
    """
    Index of the candlestick that was interacted with; `None` if none.
    """


@ft.control("CandlestickChart")
class CandlestickChart(ft.LayoutControl):
    """
    Draws a candlestick chart representing OHLC values.
    """

    spots: list[CandlestickChartSpot] = field(default_factory=list)
    """
    Candlesticks to display on the chart.
    """

    animation: ft.AnimationValue = field(
        default_factory=lambda: ft.Animation(
            duration=ft.Duration(milliseconds=150), curve=ft.AnimationCurve.LINEAR
        )
    )
    """
    Controls chart implicit animations.
    """

    interactive: bool = True
    """
    Enables automatic tooltips and highlighting when hovering the chart.
    """

    show_tooltips_for_selected_spots_only: bool = False
    """
    Whether to permanently and only show the tooltips of spots with their
    [`selected`][(p).CandlestickChartSpot.selected] property set to `True`.
    """

    long_press_duration: Optional[ft.DurationValue] = None
    """
    The duration of a long press on the chart.
    """

    touch_spot_threshold: ft.Number = 4
    """
    The distance threshold to consider a touch near a candlestick.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    Background color of the chart.
    """

    border: Optional[ft.Border] = None
    """
    Border drawn around the chart.
    """

    horizontal_grid_lines: Optional[ChartGridLines] = None
    """
    Horizontal grid lines configuration.
    """

    vertical_grid_lines: Optional[ChartGridLines] = None
    """
    Vertical grid lines configuration.
    """

    left_axis: Optional[ChartAxis] = None
    """
    Appearance of the left axis, its title and labels.
    """

    top_axis: Optional[ChartAxis] = None
    """
    Appearance of the top axis, its title and labels.
    """

    right_axis: Optional[ChartAxis] = None
    """
    Appearance of the right axis, its title and labels.
    """

    bottom_axis: Optional[ChartAxis] = None
    """
    Appearance of the bottom axis, its title and labels.
    """

    baseline_x: Optional[ft.Number] = None
    """
    Baseline value on the X axis.
    """

    min_x: Optional[ft.Number] = None
    """
    Minimum value displayed on the X axis.
    """

    max_x: Optional[ft.Number] = None
    """
    Maximum value displayed on the X axis.
    """

    baseline_y: Optional[ft.Number] = None
    """
    Baseline value on the Y axis.
    """

    min_y: Optional[ft.Number] = None
    """
    Minimum value displayed on the Y axis.
    """

    max_y: Optional[ft.Number] = None
    """
    Maximum value displayed on the Y axis.
    """

    rotation_quarter_turns: ft.Number = 0
    """
    Number of quarter turns (90-degree increments) to rotate the chart.
    """

    tooltip: Optional[CandlestickChartTooltip] = field(
        default_factory=lambda: CandlestickChartTooltip()
    )
    """
    Tooltip configuration for the chart.
    """

    on_event: Optional[ft.EventHandler[CandlestickChartEvent]] = None
    """
    Called when an event occurs on this chart.
    """

    def __post_init__(self, ref: Optional[ft.Ref[Any]]):
        super().__post_init__(ref)
        self._internals["skip_properties"] = ["tooltip"]
