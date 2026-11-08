from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["PieChartSection", "PieChartSectionSegment"]


@ft.control("PieChartSectionSegment")
class PieChartSectionSegment(ft.BaseControl):
    """
    A band of a :class:`~flet_charts.PieChartSection`, drawn over the section from
    :attr:`from_radius` to :attr:`to_radius`.

    Segments split a section into concentric layers, as in a stacked pie chart.
    """

    to_radius: ft.Number
    """
    The distance from the inner edge of the section to the outer edge of this
    segment.

    It is clamped between `0` and the section's
    :attr:`~flet_charts.PieChartSection.radius`.
    """

    from_radius: ft.Number = 0
    """
    The distance from the inner edge of the section to the inner edge of this
    segment.

    It is clamped between `0` and the section's
    :attr:`~flet_charts.PieChartSection.radius`. If it is not smaller than
    :attr:`to_radius`, this segment is not drawn.
    """

    color: ft.ColorValue = ft.Colors.PURPLE
    """
    The color of this segment.
    """

    gradient: Optional[ft.Gradient] = None
    """
    The gradient this segment is filled with.

    Takes precedence over :attr:`color`.
    """


@ft.control("PieChartSection")
class PieChartSection(ft.BaseControl):
    """
    Configures a :class:`~flet_charts.PieChart` section.
    """

    value: ft.Number
    """
    Determines how much the section should occupy. This depends on sum of all sections,
    each section should occupy (`value` / sum of all values) * `360` degrees.
    """

    radius: Optional[ft.Number] = None
    """
    External radius of the section.
    """

    color: Optional[ft.ColorValue] = None
    """
    Background color of the section.
    """

    border_side: ft.BorderSide = field(default_factory=lambda: ft.BorderSide.none())
    """
    The border around section shape.
    """

    title: Optional[str] = None
    """
    A title drawn at the center of the section.
    """

    title_style: Optional[ft.TextStyle] = None
    """
    The style to draw `title` with.
    """

    title_position: Optional[ft.Number] = None
    """
    The position/offset of the :attr:`title` relative to the section's center.

    - `0.0`: near the center
    - `1.0`: near the outside of the chart

    By default the :attr:`title` is drawn in the middle of the section.
    """

    badge: Optional[ft.Control] = None
    """
    An optional `Control` drawn in the middle of a section.
    """

    badge_position: Optional[ft.Number] = None
    """
    The position/offset of the :attr:`badge` relative to the section's center.

    - `0.0`: near the center
    - `1.0`: near the outside of the chart

    By default the :attr:`badge` is drawn in the middle of the section.
    """

    gradient: Optional[ft.Gradient] = None
    """
    Defines the gradient of section. If specified, overrides the color setting.
    """

    corner_radius: ft.Number = 0
    """
    The radius of the rounded corners of the section.

    Negative values are treated as `0`.
    """

    segments: list[PieChartSectionSegment] = field(default_factory=list)
    """
    The segments drawn over this section, in order.
    """

    def init(self):
        super().init()
        self._internals["skip_properties"] = ["badge"]
