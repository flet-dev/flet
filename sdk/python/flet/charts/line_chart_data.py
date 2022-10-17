from typing import Any, List, Optional

from beartype import beartype
from flet.animation import Curve
from flet.charts.line_chart_data_point import LineChartDataPoint
from flet.charts.grid_lines import GridLines

from flet.control import Control, MainAxisAlignment, OptionalNumber
from flet.ref import Ref
from flet.types import PaddingValue


class LineChartData(Control):
    def __init__(
        self,
        data_points: Optional[List[LineChartDataPoint]] = None,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        curved: Optional[bool] = None,
        color: Optional[bool] = None,
        stroke_width: OptionalNumber = None,
        stroke_cap_round: Optional[bool] = None,
        above_line_color: Optional[str] = None,
        below_line_color: Optional[str] = None,
        show_markers: Optional[bool] = None,
        #
        #
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

    def _get_control_name(self):
        return "data"

    def _get_children(self):
        children = []
        return children
