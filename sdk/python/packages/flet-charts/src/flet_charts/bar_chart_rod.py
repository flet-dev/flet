from dataclasses import field
from typing import Optional, Union

import flet as ft
from flet_charts.bar_chart_rod_stack_item import BarChartRodStackItem
from flet_charts.types import ChartDataPointTooltip

__all__ = ["BarChartRod", "BarChartRodLabel", "BarChartRodTooltip"]


@ft.value
class BarChartRodTooltip(ChartDataPointTooltip):
    """
    Tooltip configuration for the  :class:`~flet_charts.BarChartRod`.
    """

    text: Optional[str] = None
    """
    The text to display in the tooltip.

    When `None`, defaults to
    :attr:`flet_charts.BarChartRod.to_y`.
    """

    def copy(
        self,
        *,
        text: Optional[str] = None,
        text_style: Optional[ft.TextStyle] = None,
        text_align: Optional[ft.TextAlign] = None,
        text_spans: Optional[list[ft.TextSpan]] = None,
        rtl: Optional[bool] = None,
    ) -> "BarChartRodTooltip":
        """
        Returns a copy of this object with the specified properties overridden.
        """
        return BarChartRodTooltip(
            text=text if text is not None else self.text,
            text_style=text_style if text_style is not None else self.text_style,
            text_align=text_align if text_align is not None else self.text_align,
            text_spans=text_spans.copy()
            if text_spans is not None
            else (self.text_spans.copy() if self.text_spans is not None else None),
            rtl=rtl if rtl is not None else self.rtl,
        )


@ft.value
class BarChartRodLabel:
    """
    A text label drawn past the tip of a :class:`~flet_charts.BarChartRod`.
    """

    text: str = ""
    """
    The text of the label.

    If empty, no label is drawn.
    """

    text_style: Optional[ft.TextStyle] = None
    """
    The text style of the label.

    Defaults to the theme's :attr:`flet.TextTheme.body_medium`.
    """

    angle: ft.Number = 0
    """
    The rotation of the label, in degrees.
    """

    offset: ft.Offset = field(default_factory=lambda: ft.Offset(0, 8))
    """
    The position of the label relative to the tip of the rod, in logical pixels.

    `x` moves the label sideways, and `y` moves it away from the rod.
    """


@ft.control("BarChartRod")
class BarChartRod(ft.BaseControl):
    """A bar rod in a :class:`~flet_charts.BarChartGroup`."""

    stack_items: list[BarChartRodStackItem] = field(default_factory=list)
    """
    Optional list of :class:`~flet_charts.BarChartRodStackItem` objects to draw a \
    stacked bar.
    """

    from_y: ft.Number = 0
    """
    Specifies a starting position of this rod on Y axis.
    """

    to_y: Optional[ft.Number] = None
    """
    Specifies an ending position of this rod on Y axis.
    """

    width: Optional[ft.Number] = None
    """
    The width of this rod.
    """

    color: Optional[ft.ColorValue] = None
    """
    Rod color.
    """

    gradient: Optional[ft.Gradient] = None
    """
    Gradient to draw rod's background.
    """

    border_radius: Optional[ft.BorderRadiusValue] = None
    """
    Border radius of a bar rod.
    """

    border_side: Optional[ft.BorderSide] = None
    """
    Border to draw around rod.
    """

    bg_from_y: Optional[ft.Number] = None
    """
    An optional starting position of a background behind this rod.
    """

    bg_to_y: Optional[ft.Number] = None
    """
    An optional ending position of a background behind this rod.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    An optional color of a background behind
    this rod.
    """

    background_gradient: Optional[ft.Gradient] = None
    """
    An optional gradient to draw a background with.
    """

    selected: bool = False
    """
    If set to `True` a tooltip is always shown on top of the bar when
    :attr:`flet_charts.BarChart.interactive`
    is set to `False`.
    """

    tooltip: Union[BarChartRodTooltip, str] = field(
        default_factory=lambda: BarChartRodTooltip()
    )
    """
    The rod's tooltip configuration for this rod.
    """

    show_tooltip: bool = True
    """
    Whether a tooltip should be shown on top of hovered bar.
    """

    label: Optional[Union[str, BarChartRodLabel]] = None
    """
    The label drawn past the tip of this rod, such as its value.

    A string is drawn with the default :class:`~flet_charts.BarChartRodLabel`
    settings.
    """

    def before_update(self):
        super().before_update()
        self._internals["tooltip"] = (
            BarChartRodTooltip(text=self.tooltip)
            if isinstance(self.tooltip, str)
            else self.tooltip
        )
