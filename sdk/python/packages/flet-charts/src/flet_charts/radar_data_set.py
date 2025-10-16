from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["RadarDataSet", "RadarDataSetEntry"]


@ft.control("RadarDataSetEntry")
class RadarDataSetEntry(ft.BaseControl):
    """
    A single data point rendered on a [`RadarChart`][(p).].
    """

    value: ft.Number
    """
    The numeric value drawn for this entry.
    """


@ft.control("RadarDataSet")
class RadarDataSet(ft.BaseControl):
    """
    A collection of [`RadarDataSetEntry`][(p).] drawn as a filled radar shape.
    """

    entries: list[RadarDataSetEntry] = field(default_factory=list)
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

    Takes precedence over [`fill_color`][..].
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

    def init(self):
        super().init()
        entries_length = len(self.entries)
        if entries_length != 0 and entries_length < 3:
            raise ValueError(
                f"entries can contain either 0 or at least 3 items, "
                f"got {entries_length}"
            )
