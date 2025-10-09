from dataclasses import dataclass, field
from typing import Optional, Union

import flet as ft
from flet_charts.types import ChartDataPointTooltip

__all__ = ["CandlestickChartSpot", "CandlestickChartSpotTooltip"]


@dataclass
class CandlestickChartSpotTooltip(ChartDataPointTooltip):
    """Tooltip configuration for the [`CandlestickChartSpot`][(p).]."""

    bottom_margin: ft.Number = 8
    """
    Space between the tooltip bubble and the candlestick.
    """

    def copy(
        self,
        *,
        text: Optional[str] = None,
        text_style: Optional[ft.TextStyle] = None,
        text_align: Optional[ft.TextAlign] = None,
        text_spans: Optional[list[ft.TextSpan]] = None,
        rtl: Optional[bool] = None,
        bottom_margin: Optional[ft.Number] = None,
    ) -> "CandlestickChartSpotTooltip":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return CandlestickChartSpotTooltip(
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


@ft.control("CandlestickChartSpot")
class CandlestickChartSpot(ft.BaseControl):
    """Represents a candlestick rendered on a [`CandlestickChart`][(p).]."""

    x: ft.Number
    """
    The position of the candlestick on the X axis.
    """

    open: ft.Number
    """
    The open value of the candlestick.
    """

    high: ft.Number
    """
    The high value of the candlestick.
    """

    low: ft.Number
    """
    The low value of the candlestick.
    """

    close: ft.Number
    """
    The close value of the candlestick.
    """

    selected: bool = False
    """
    Whether to treat this candlestick as selected.
    """

    tooltip: Union[CandlestickChartSpotTooltip, str] = field(
        default_factory=lambda: CandlestickChartSpotTooltip()
    )
    """
    Tooltip configuration for this candlestick.
    """

    show_tooltip: bool = True
    """
    Whether the tooltip should be shown when this candlestick is highlighted.
    """

    def before_update(self):
        super().before_update()
        self._internals["tooltip"] = (
            CandlestickChartSpotTooltip(text=self.tooltip)
            if isinstance(self.tooltip, str)
            else self.tooltip
        )
