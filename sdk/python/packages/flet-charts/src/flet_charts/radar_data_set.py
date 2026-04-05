from dataclasses import field
from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V

__all__ = ["RadarDataSet", "RadarDataSetEntry"]


@ft.control("RadarDataSetEntry")
class RadarDataSetEntry(ft.BaseControl):
    """
    A single data point rendered on a :class:`~flet_charts.RadarChart`.
    """

    value: ft.Number
    """
    The numeric value drawn for this entry.
    """


@ft.control("RadarDataSet")
class RadarDataSet(ft.BaseControl):
    """
    A collection of :class:`~flet_charts.RadarDataSetEntry` drawn as a filled radar \
    shape.
    """

    entries: Annotated[
        list[RadarDataSetEntry],
        V.or_(
            V.length_eq(0),
            V.length_ge(3),
            message=lambda _control, _field_name, value: (
                f"entries can contain either 0 or at least 3 items, got {len(value)}"
            ),
        ),
    ] = field(default_factory=list)
    """
    The data points that compose this set.
    """

    fill_color: ft.ColorValue = ft.Colors.CYAN
    """
    The color used to fill this dataset.
    """

    fill_gradient: Optional[ft.Gradient] = None
    """
    The gradient used to fill this dataset.

    Takes precedence over :attr:`fill_color`.
    """

    border_color: ft.ColorValue = ft.Colors.CYAN
    """
    The color of the dataset outline.
    """

    border_width: ft.Number = 2.0
    """
    The width of the dataset outline.
    """

    entry_radius: ft.Number = 5.0
    """
    The radius of each entry.
    """
