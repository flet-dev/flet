from typing import Any, List, Optional

from beartype import beartype
from flet.animation import Curve
from flet.border import Border
from flet.charts.line_chart_axis import LineChartAxis
from flet.charts.line_chart_data import LineChartData
from flet.charts.grid_lines import GridLines

from flet.control import Control, MainAxisAlignment, OptionalNumber
from flet.ref import Ref
from flet.types import PaddingValue


class LineChart(Control):
    def __init__(
        self,
        data_series: Optional[List[LineChartData]] = None,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        swap_animation_duration: Optional[int] = None,
        swap_animation_curve: Optional[Curve] = None,
        bgcolor: Optional[str] = None,
        border: Optional[Border] = None,
        horizontal_grid_lines: Optional[GridLines] = None,
        vertical_grid_lines: Optional[GridLines] = None,
        left_axis: Optional[LineChartAxis] = None,
        top_axis: Optional[LineChartAxis] = None,
        right_axis: Optional[LineChartAxis] = None,
        bottom_axis: Optional[LineChartAxis] = None,
        baseline_x: OptionalNumber = None,
        min_x: OptionalNumber = None,
        max_x: OptionalNumber = None,
        baseline_y: OptionalNumber = None,
        min_y: OptionalNumber = None,
        max_y: OptionalNumber = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

    def _get_control_name(self):
        return "linechart"

    def _get_children(self):
        children = []
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        for action in self.__actions:
            action._set_attr_internal("n", "action")
            children.append(action)
        return children

    # data_series
    @property
    def data_series(self):
        return self.__data_series

    @data_series.setter
    def data_series(self, value):
        self.__data_series = value if value is not None else []
