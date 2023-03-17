from typing import Any, List, Optional, Union

from flet_core.charts.chart_point_shape import ChartPointShape
from flet_core.charts.line_chart_data_point import LineChartDataPoint
from flet_core.container import BoxShadow
from flet_core.control import Control, OptionalNumber
from flet_core.gradients import Gradient
from flet_core.ref import Ref


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
        color: Optional[str] = None,
        gradient: Optional[Gradient] = None,
        stroke_width: OptionalNumber = None,
        stroke_cap_round: Optional[bool] = None,
        dash_pattern: Optional[List[int]] = None,
        shadow: Optional[BoxShadow] = None,
        above_line_color: Optional[str] = None,
        above_line_gradient: Optional[Gradient] = None,
        below_line_color: Optional[str] = None,
        below_line_gradient: Optional[Gradient] = None,
        point: Union[None, bool, ChartPointShape] = None,
        selected_point: Union[None, bool, ChartPointShape] = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.data_points = data_points
        self.curved = curved
        self.color = color
        self.gradient = gradient
        self.stroke_width = stroke_width
        self.stroke_cap_round = stroke_cap_round
        self.shadow = shadow
        self.dash_pattern = dash_pattern
        self.above_line_color = above_line_color
        self.above_line_gradient = above_line_gradient
        self.below_line_color = below_line_color
        self.below_line_gradient = below_line_gradient
        self.point = point
        self.selected_point = selected_point

    def _get_control_name(self):
        return "data"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("gradient", self.__gradient)
        self._set_attr_json("shadow", self.__shadow)
        self._set_attr_json("point", self.__point)
        self._set_attr_json("selectedPoint", self.__selected_point)
        self._set_attr_json("dashPattern", self.__dash_pattern)
        self._set_attr_json("aboveLineGradient", self.__above_line_gradient)
        self._set_attr_json("belowLineGradient", self.__below_line_gradient)

    def _get_children(self):
        return self.__data_points

    # data_points
    @property
    def data_points(self):
        return self.__data_points

    @data_points.setter
    def data_points(self, value):
        self.__data_points = value if value is not None else []

    # stroke_width
    @property
    def stroke_width(self) -> OptionalNumber:
        return self._get_attr("strokeWidth", data_type="float", def_value=1.0)

    @stroke_width.setter
    def stroke_width(self, value: OptionalNumber):
        self._set_attr("strokeWidth", value)

    # curved
    @property
    def curved(self) -> Optional[bool]:
        return self._get_attr("curved", data_type="bool", def_value=False)

    @curved.setter
    def curved(self, value: Optional[bool]):
        self._set_attr("curved", value)

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # gradient
    @property
    def gradient(self) -> Optional[Gradient]:
        return self.__gradient

    @gradient.setter
    def gradient(self, value: Optional[Gradient]):
        self.__gradient = value

    # stroke_cap_round
    @property
    def stroke_cap_round(self) -> Optional[bool]:
        return self._get_attr("strokeCapRound", data_type="bool", def_value=False)

    @stroke_cap_round.setter
    def stroke_cap_round(self, value: Optional[bool]):
        self._set_attr("strokeCapRound", value)

    # dash_pattern
    @property
    def dash_pattern(self):
        return self.__dash_pattern

    @dash_pattern.setter
    def dash_pattern(self, value: Optional[List[int]]):
        self.__dash_pattern = value

    # shadow
    @property
    def shadow(self):
        return self.__shadow

    @shadow.setter
    def shadow(self, value: Optional[BoxShadow]):
        self.__shadow = value

    # point
    @property
    def point(self):
        return self.__point

    @point.setter
    def point(self, value: Union[None, bool, ChartPointShape]):
        self.__point = value

    # selected_point
    @property
    def selected_point(self):
        return self.__selected_point

    @selected_point.setter
    def selected_point(self, value: Union[None, bool, ChartPointShape]):
        self.__selected_point = value

    # above_line_color
    @property
    def above_line_color(self) -> Optional[str]:
        return self._get_attr("aboveLineColor")

    @above_line_color.setter
    def above_line_color(self, value: Optional[str]):
        self._set_attr("aboveLineColor", value)

    # above_line_gradient
    @property
    def above_line_gradient(self) -> Optional[Gradient]:
        return self.__above_line_gradient

    @above_line_gradient.setter
    def above_line_gradient(self, value: Optional[Gradient]):
        self.__above_line_gradient = value

    # below_line_color
    @property
    def below_line_color(self) -> Optional[str]:
        return self._get_attr("belowLineColor")

    @below_line_color.setter
    def below_line_color(self, value: Optional[str]):
        self._set_attr("belowLineColor", value)

    # below_line_gradient
    @property
    def below_line_gradient(self) -> Optional[Gradient]:
        return self.__below_line_gradient

    @below_line_gradient.setter
    def below_line_gradient(self, value: Optional[Gradient]):
        self.__below_line_gradient = value
