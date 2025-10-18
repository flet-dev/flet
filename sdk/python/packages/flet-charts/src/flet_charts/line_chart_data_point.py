from dataclasses import dataclass, field
from typing import Optional, Union

import flet as ft
from flet_charts.types import ChartDataPointTooltip, ChartPointLine, ChartPointShape

__all__ = ["LineChartDataPoint", "LineChartDataPointTooltip"]


@dataclass
class LineChartDataPointTooltip(ChartDataPointTooltip):
    """Tooltip configuration for the [`LineChartDataPoint`][(p).]."""

    text: Optional[str] = None
    """
    The text to display in the tooltip.

    When `None`, defaults to [`LineChartDataPoint.y`][(p).].
    """

    def copy(
        self,
        *,
        text: Optional[str] = None,
        text_style: Optional[ft.TextStyle] = None,
        text_align: Optional[ft.TextAlign] = None,
        text_spans: Optional[list[ft.TextSpan]] = None,
        rtl: Optional[bool] = None,
    ) -> "LineChartDataPointTooltip":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return LineChartDataPointTooltip(
            text=text if text is not None else self.text,
            text_style=text_style if text_style is not None else self.text_style,
            text_align=text_align if text_align is not None else self.text_align,
            text_spans=text_spans.copy()
            if text_spans is not None
            else (self.text_spans.copy() if self.text_spans is not None else None),
            rtl=rtl if rtl is not None else self.rtl,
        )


@ft.control("LineChartDataPoint")
class LineChartDataPoint(ft.BaseControl):
    """A [`LineChartData`][(p).] point."""

    x: ft.Number
    """
    The position of a point on `X` axis.
    """

    y: ft.Number
    """
    The position of a point on `Y` axis.
    """

    selected: bool = False
    """
    Draw the point as selected when [`LineChart.interactive`][(p).]
    is set to `False`.
    """

    point: Union[None, bool, ChartPointShape] = None
    """
    Defines the appearance and shape of a line point.
    """

    selected_point: Union[None, bool, ChartPointShape] = None
    """
    Defines the appearance and shape of a selected line point.
    """

    show_above_line: bool = True
    """
    Whether to display a line above data point.
    """

    show_below_line: bool = True
    """
    Whether to display a line below data point.
    """

    selected_below_line: Union[None, bool, ChartPointLine] = None
    """
    A vertical line drawn between selected line point and the bottom adge of the chart.

    The value is either `True` - draw a line with default style, `False` - do not draw a
    line under selected point, or an instance of [`ChartPointLine`][(p).] class to
    specify line style to draw.
    """

    tooltip: Union[LineChartDataPointTooltip, str] = field(
        default_factory=lambda: LineChartDataPointTooltip()
    )
    """
    Configuration of the tooltip for this data point.
    """

    show_tooltip: bool = True
    """
    Whether the [`tooltip`][(c).] should be shown when this data point is hovered over.
    """

    def before_update(self):
        super().before_update()
        self._internals["tooltip"] = (
            LineChartDataPointTooltip(text=self.tooltip)
            if isinstance(self.tooltip, str)
            else self.tooltip
        )
