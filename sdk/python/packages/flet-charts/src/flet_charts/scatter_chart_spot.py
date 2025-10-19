from dataclasses import dataclass, field
from typing import Any, Optional, Union

import flet as ft
from flet_charts.types import ChartDataPointTooltip, ChartPointShape

__all__ = ["ScatterChartSpot", "ScatterChartSpotTooltip"]


@dataclass
class ScatterChartSpotTooltip(ChartDataPointTooltip):
    """
    Tooltip configuration for the [`ScatterChartSpot`][(p).].
    """

    text: Optional[str] = None
    """
    The text to display in the tooltip.

    When `None`, defaults to [`ScatterChartSpot.y`][(p).].
    """

    bottom_margin: ft.Number = 8
    """
    The bottom space from the spot.
    """

    def copy(
        self,
        *,
        text: Optional[str] = None,
        text_style: Optional[ft.TextStyle] = None,
        text_align: Optional[ft.TextAlign] = None,
        text_spans: Optional[list[ft.TextSpan]] = None,
        rtl: Optional[bool] = None,
        bottom_margin: Optional[float] = None,
    ) -> "ScatterChartSpotTooltip":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return ScatterChartSpotTooltip(
            text=text if text is not None else self.text,
            text_style=text_style if text_style is not None else self.text_style,
            text_align=text_align if text_align is not None else self.text_align,
            text_spans=text_spans.copy()
            if text_spans is not None
            else (self.text_spans.copy() if self.text_spans is not None else None),
            rtl=rtl if rtl is not None else self.rtl,
            bottom_margin=bottom_margin
            if bottom_margin is not None
            else self.bottom_margin,
        )


@ft.control("ScatterChartSpot")
class ScatterChartSpot(ft.BaseControl):
    """A spot on a scatter chart."""

    x: Optional[ft.Number] = None
    """
    The position of a spot on `X` axis.
    """

    y: Optional[ft.Number] = None
    """
    The position of a spot on `Y` axis.
    """

    visible: bool = True
    """
    Determines wether to show or hide the spot.
    """

    radius: Optional[ft.Number] = None
    """
    Radius of a spot.
    """

    color: Optional[ft.ColorValue] = None
    """
    Color of a spot.
    """

    render_priority: ft.Number = 0
    """
    Sort by this to manage overlap.
    """

    x_error: Optional[Any] = None
    """
    Determines the error range of the data point using
    [FlErrorRange](https://github.com/imaNNeo/fl_chart/blob/main/repo_files/documentations/base_chart.md#flerrorrange)
    (which contains lowerBy and upperValue) for the `X` axis.
    """

    y_error: Optional[Any] = None
    """
    Determines the error range of the data point using
    [FlErrorRange](https://github.com/imaNNeo/fl_chart/blob/main/repo_files/documentations/base_chart.md#flerrorrange)
    (which contains lowerBy and upperValue) for the `Y` axis.
    """

    selected: bool = False
    """
    Whether to treat this spot as selected.
    """

    tooltip: Union[ScatterChartSpotTooltip, str] = field(
        default_factory=lambda: ScatterChartSpotTooltip()
    )
    """
    Tooltip configuration for this spot.
    """

    show_tooltip: bool = True
    """
    Wether to show the tooltip.
    """

    label_text: str = ""
    """
    TBD
    """

    label_text_style: ft.TextStyle = field(default_factory=lambda: ft.TextStyle())
    """
    TBD
    """

    point: Union[None, bool, ChartPointShape] = None
    """
    TBD
    """

    def before_update(self):
        super().before_update()
        self._internals["tooltip"] = (
            ScatterChartSpotTooltip(text=self.tooltip)
            if isinstance(self.tooltip, str)
            else self.tooltip
        )
