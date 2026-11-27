from dataclasses import field
from enum import Enum
from typing import Optional

import flet as ft

__all__ = ["ChartAxis", "ChartAxisLabel", "ChartAxisLabelAlignment"]


class ChartAxisLabelAlignment(Enum):
    """
    Where the labels of a :class:`~flet_charts.ChartAxis` are drawn, relative to
    the border of the chart.
    """

    OUTSIDE = "outside"
    """
    Outside the chart area, in the space reserved by
    :attr:`flet_charts.ChartAxis.label_size`.
    """

    BORDER = "border"
    """
    Straddling the border of the chart area, with half of
    :attr:`flet_charts.ChartAxis.label_size` reserved outside it.
    """

    INSIDE = "inside"
    """
    Inside the chart area, over the chart's content, with no space reserved
    outside it.
    """


@ft.control("ChartAxisLabel")
class ChartAxisLabel(ft.BaseControl):
    """
    Configures a custom label for specific value.
    """

    value: Optional[ft.Number] = None
    """
    A value to draw label for.
    """

    label: Optional[ft.StrOrControl] = None
    """
    The label to display for the specified :attr:`value`.
    """


@ft.control("ChartAxis")
class ChartAxis(ft.BaseControl):
    """
    Configures chart axis.
    """

    title: Optional[ft.Control] = None
    """
    A `Control` to display as axis title.
    """

    title_size: ft.Number = 16
    """
    The size of title area.
    """

    show_labels: bool = True
    """
    Whether to display the :attr:`labels` along the axis.
    If `labels` is empty then automatic labels are displayed.
    """

    labels: list[ChartAxisLabel] = field(default_factory=list)
    """
    The list of :class:`~flet_charts.ChartAxisLabel`
    objects to set custom axis labels for only specific values.
    """

    label_spacing: Optional[ft.Number] = None
    """
    The spacing/interval between labels.

    If a value is not set, a suitable value
    will be automatically calculated and used.
    """

    label_size: ft.Number = 22
    """
    The maximum space for each label in :attr:`labels`.

    Each label will stretch to fit this space.
    """

    show_min: bool = True
    """
    Whether to display a label for the minimum value
    independent of the sampling interval.
    """

    show_max: bool = True
    """
    Whether to display a label for the maximum value
    independent of the sampling interval.
    """

    label_alignment: ChartAxisLabelAlignment = ChartAxisLabelAlignment.OUTSIDE
    """
    Where the labels are drawn, relative to the border of the chart.
    """

    def before_update(self):
        super().before_update()
        if self.label_spacing == 0:
            raise ValueError("label_spacing cannot be 0")
