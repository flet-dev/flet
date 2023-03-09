from typing import Any, List, Optional

from beartype import beartype
from flet.border import Border
from flet.charts.line_chart_axis import LineChartAxis
from flet.charts.line_chart_data import LineChartData
from flet.charts.grid_lines import GridLines

from flet.control import Control, OptionalNumber
from flet.ref import Ref
from flet.types import AnimationValue


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
        animate: AnimationValue = None,
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

        self.data_series = data_series
        self.animate = animate
        self.bgcolor = bgcolor
        self.border = border
        self.horizontal_grid_lines = horizontal_grid_lines
        self.vertical_grid_lines = vertical_grid_lines
        self.left_axis = left_axis
        self.top_axis = top_axis
        self.right_axis = right_axis
        self.bottom_axis = bottom_axis
        self.baseline_x = baseline_x
        self.baseline_y = baseline_y
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def _get_control_name(self):
        return "linechart"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("horizontalGridLines", self.__horizontal_grid_lines)
        self._set_attr_json("verticalGridLines", self.__vertical_grid_lines)

    def _get_children(self):
        children = []
        for ds in self.__data_series:
            ds._set_attr_internal("n", "data")
            children.append(ds)
        if self.__left_axis:
            self.__left_axis._set_attr_internal("n", "left_axis")
            children.append(self.__left_axis)
        if self.__top_axis:
            self.__top_axis._set_attr_internal("n", "top_axis")
            children.append(self.__top_axis)
        if self.__right_axis:
            self.__right_axis._set_attr_internal("n", "right_axis")
            children.append(self.__right_axis)
        if self.__bottom_axis:
            self.__bottom_axis._set_attr_internal("n", "bottom_axis")
            children.append(self.__bottom_axis)
        return children

    # data_series
    @property
    def data_series(self):
        return self.__data_series

    @data_series.setter
    def data_series(self, value):
        self.__data_series = value if value is not None else []

    # animate
    @property
    def animate(self) -> AnimationValue:
        return self.__animate

    @animate.setter
    @beartype
    def animate(self, value: AnimationValue):
        self.__animate = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    @beartype
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    @beartype
    def border(self, value: Optional[Border]):
        self.__border = value

    # horizontal_grid_lines
    @property
    def horizontal_grid_lines(self) -> Optional[GridLines]:
        return self.__horizontal_grid_lines

    @horizontal_grid_lines.setter
    @beartype
    def horizontal_grid_lines(self, value: Optional[GridLines]):
        self.__horizontal_grid_lines = value

    # vertical_grid_lines
    @property
    def vertical_grid_lines(self) -> Optional[GridLines]:
        return self.__vertical_grid_lines

    @vertical_grid_lines.setter
    @beartype
    def vertical_grid_lines(self, value: Optional[GridLines]):
        self.__vertical_grid_lines = value

    # left_axis
    @property
    def left_axis(self) -> Optional[LineChartAxis]:
        return self.__left_axis

    @left_axis.setter
    @beartype
    def left_axis(self, value: Optional[LineChartAxis]):
        self.__left_axis = value

    # top_axis
    @property
    def top_axis(self) -> Optional[LineChartAxis]:
        return self.__top_axis

    @top_axis.setter
    @beartype
    def top_axis(self, value: Optional[LineChartAxis]):
        self.__top_axis = value

    # right_axis
    @property
    def right_axis(self) -> Optional[LineChartAxis]:
        return self.__right_axis

    @right_axis.setter
    @beartype
    def right_axis(self, value: Optional[LineChartAxis]):
        self.__right_axis = value

    # bottom_axis
    @property
    def bottom_axis(self) -> Optional[LineChartAxis]:
        return self.__bottom_axis

    @bottom_axis.setter
    @beartype
    def bottom_axis(self, value: Optional[LineChartAxis]):
        self.__bottom_axis = value

    # baseline_x
    @property
    def baseline_x(self) -> OptionalNumber:
        return self._get_attr("baselinex", data_type="float", def_value=1.0)

    @baseline_x.setter
    @beartype
    def baseline_x(self, value: OptionalNumber):
        self._set_attr("baselinex", value)

    # baseline_y
    @property
    def baseline_y(self) -> OptionalNumber:
        return self._get_attr("baseliney", data_type="float", def_value=1.0)

    @baseline_y.setter
    @beartype
    def baseline_y(self, value: OptionalNumber):
        self._set_attr("baseliney", value)

    # min_x
    @property
    def min_x(self) -> OptionalNumber:
        return self._get_attr("minx", data_type="float", def_value=1.0)

    @min_x.setter
    @beartype
    def min_x(self, value: OptionalNumber):
        self._set_attr("minx", value)

    # max_x
    @property
    def max_x(self) -> OptionalNumber:
        return self._get_attr("maxx", data_type="float", def_value=1.0)

    @max_x.setter
    @beartype
    def max_x(self, value: OptionalNumber):
        self._set_attr("maxx", value)

    # min_y
    @property
    def min_y(self) -> OptionalNumber:
        return self._get_attr("miny", data_type="float", def_value=1.0)

    @min_y.setter
    @beartype
    def min_y(self, value: OptionalNumber):
        self._set_attr("miny", value)

    # max_y
    @property
    def max_y(self) -> OptionalNumber:
        return self._get_attr("maxy", data_type="float", def_value=1.0)

    @max_y.setter
    @beartype
    def max_y(self, value: OptionalNumber):
        self._set_attr("maxy", value)
