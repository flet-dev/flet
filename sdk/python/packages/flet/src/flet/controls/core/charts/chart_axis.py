from dataclasses import field
from typing import List, Optional

from flet.controls.control import Control, control
from flet.controls.core.charts.chart_axis_label import ChartAxisLabel
from flet.controls.types import OptionalNumber


@control("a")
class ChartAxis(Control):
    title: Optional[Control] = None
    title_size: OptionalNumber = None
    show_labels: Optional[bool] = None
    labels: List[ChartAxisLabel] = field(default_factory=list)
    labels_interval: OptionalNumber = None
    labels_size: OptionalNumber = None
