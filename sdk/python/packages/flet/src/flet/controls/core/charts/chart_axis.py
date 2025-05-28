from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.core.charts.chart_axis_label import ChartAxisLabel
from flet.controls.types import OptionalNumber


@control("a")
class ChartAxis(Control):
    title: Optional[Control] = None
    """
    A `Control` to display as axis title.
    """

    title_size: OptionalNumber = None
    """
    Width or height of title area.
    """

    show_labels: Optional[bool] = None
    """
    If `True`, displays the `labels` along the axis. If `labels` is empty then
    automatic labels are displayed.
    """

    labels: list[ChartAxisLabel] = field(default_factory=list)
    """
    The list of [`ChartAxisLabel`](https://flet.dev/docs/reference/types/chartaxislabel)
    objects to set custom axis labels for only specific values.
    """

    labels_interval: OptionalNumber = None
    """
    The interval between automatic labels.
    """

    labels_size: OptionalNumber = None
    """
    Width or height of labels area.
    """

