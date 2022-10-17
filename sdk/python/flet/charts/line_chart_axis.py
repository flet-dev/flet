from typing import Any, List, Optional

from beartype import beartype
from flet.animation import Curve
from flet.charts.line_chart_axis_label import LineChartAxisLabel
from flet.charts.types import GridLines

from flet.control import Control, MainAxisAlignment, OptionalNumber
from flet.ref import Ref
from flet.types import PaddingValue


class LineChartAxis(Control):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        title: Optional[Control] = None,
        show_labels: Optional[bool] = None,
        labels: Optional[List[LineChartAxisLabel]] = None,
        labels_interval: OptionalNumber = None,
        reserved_size: OptionalNumber = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

    def _get_control_name(self):
        return "axis"

    def _get_children(self):
        children = []
        return children
