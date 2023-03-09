from typing import Any, List, Optional

from beartype import beartype
from flet.charts.line_chart_data_point import LineChartDataPoint

from flet.control import Control, OptionalNumber
from flet.ref import Ref


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
        stroke_width: OptionalNumber = None,
        stroke_cap_round: Optional[bool] = None,
        above_line_color: Optional[str] = None,
        below_line_color: Optional[str] = None,
        show_markers: Optional[bool] = None,
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
        self.stroke_width = stroke_width
        self.stroke_cap_round = stroke_cap_round
        self.show_markers = show_markers
        self.above_line_color = above_line_color
        self.below_line_color = below_line_color

    def _get_control_name(self):
        return "data"

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
    @beartype
    def stroke_width(self, value: OptionalNumber):
        self._set_attr("strokeWidth", value)

    # curved
    @property
    def curved(self) -> Optional[bool]:
        return self._get_attr("curved", data_type="bool", def_value=False)

    @curved.setter
    @beartype
    def curved(self, value: Optional[bool]):
        self._set_attr("curved", value)

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color")

    @color.setter
    @beartype
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # stroke_cap_round
    @property
    def stroke_cap_round(self) -> Optional[bool]:
        return self._get_attr("strokeCapRound", data_type="bool", def_value=False)

    @stroke_cap_round.setter
    @beartype
    def stroke_cap_round(self, value: Optional[bool]):
        self._set_attr("strokeCapRound", value)

    # show_markers
    @property
    def show_markers(self) -> Optional[bool]:
        return self._get_attr("showMarkers", data_type="bool", def_value=False)

    @show_markers.setter
    @beartype
    def show_markers(self, value: Optional[bool]):
        self._set_attr("showMarkers", value)

    # above_line_color
    @property
    def above_line_color(self) -> Optional[str]:
        return self._get_attr("aboveLineColor")

    @above_line_color.setter
    @beartype
    def above_line_color(self, value: Optional[str]):
        self._set_attr("aboveLineColor", value)

    # below_line_color
    @property
    def below_line_color(self) -> Optional[str]:
        return self._get_attr("belowLineColor")

    @below_line_color.setter
    @beartype
    def below_line_color(self, value: Optional[str]):
        self._set_attr("belowLineColor", value)
