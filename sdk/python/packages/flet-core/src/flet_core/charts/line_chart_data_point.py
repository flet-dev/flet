from typing import Any, Optional, Union

from flet_core.charts.chart_point_line import ChartPointLine
from flet_core.charts.chart_point_shape import ChartPointShape
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import TextAlign


class LineChartDataPoint(Control):
    def __init__(
        self,
        x: OptionalNumber = None,
        y: OptionalNumber = None,
        selected: Optional[bool] = None,
        show_tooltip: Optional[bool] = None,
        tooltip: Optional[str] = None,
        tooltip_style: Optional[TextStyle] = None,
        tooltip_align: Optional[TextAlign] = None,
        point: Union[None, bool, ChartPointShape] = None,
        selected_point: Union[None, bool, ChartPointShape] = None,
        show_above_line: Optional[bool] = None,
        show_below_line: Optional[bool] = None,
        selected_below_line: Union[None, bool, ChartPointLine] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.x = x
        self.y = y
        self.selected = selected
        self.show_tooltip = show_tooltip
        self.tooltip = tooltip
        self.tooltip_align = tooltip_align
        self.tooltip_style = tooltip_style
        self.point = point
        self.selected_point = selected_point
        self.show_above_line = show_above_line
        self.show_below_line = show_below_line
        self.selected_below_line = selected_below_line

    def _get_control_name(self):
        return "p"

    def before_update(self):
        super().before_update()
        self._set_attr_json("tooltipStyle", self.__tooltip_style)
        self._set_attr_json("point", self.__point)
        self._set_attr_json("selectedPoint", self.__selected_point)
        self._set_attr_json("selectedBelowLine", self.__selected_below_line)

    def _get_children(self):
        children = []
        return children

    # x
    @property
    def x(self) -> OptionalNumber:
        return self._get_attr("x", data_type="float", def_value=0)

    @x.setter
    def x(self, value: OptionalNumber):
        self._set_attr("x", value)

    # y
    @property
    def y(self) -> OptionalNumber:
        return self._get_attr("y", data_type="float", def_value=0)

    @y.setter
    def y(self, value: OptionalNumber):
        self._set_attr("y", value)

    # selected
    @property
    def selected(self) -> Optional[bool]:
        return self._get_attr("selected", data_type="bool", def_value=False)

    @selected.setter
    def selected(self, value: Optional[bool]):
        self._set_attr("selected", value)

    # show_tooltip
    @property
    def show_tooltip(self) -> Optional[bool]:
        return self._get_attr("showTooltip", data_type="bool", def_value=True)

    @show_tooltip.setter
    def show_tooltip(self, value: Optional[bool]):
        self._set_attr("showTooltip", value)

    # tooltip
    @property
    def tooltip(self) -> Optional[str]:
        return self._get_attr("tooltip")

    @tooltip.setter
    def tooltip(self, value: Optional[str]):
        self._set_attr("tooltip", value)

    # tooltip_align
    @property
    def tooltip_align(self) -> Optional[TextAlign]:
        return self.__tooltip_align

    @tooltip_align.setter
    def tooltip_align(self, value: Optional[TextAlign]):
        self.__tooltip_align = value
        self._set_attr(
            "tooltipAlign", value.value if isinstance(value, TextAlign) else value
        )

    # tooltip_style
    @property
    def tooltip_style(self):
        return self.__tooltip_style

    @tooltip_style.setter
    def tooltip_style(self, value: Optional[TextStyle]):
        self.__tooltip_style = value

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

    # show_above_line
    @property
    def show_above_line(self) -> Optional[bool]:
        return self._get_attr("showAboveLine", data_type="bool", def_value=True)

    @show_above_line.setter
    def show_above_line(self, value: Optional[bool]):
        self._set_attr("showAboveLine", value)

    # show_below_line
    @property
    def show_below_line(self) -> Optional[bool]:
        return self._get_attr("showBelowLine", data_type="bool", def_value=True)

    @show_below_line.setter
    def show_below_line(self, value: Optional[bool]):
        self._set_attr("showBelowLine", value)

    # selected_below_line
    @property
    def selected_below_line(self) -> Union[None, bool, ChartPointLine]:
        return self.__selected_below_line

    @selected_below_line.setter
    def selected_below_line(self, value: Union[None, bool, ChartPointLine]):
        self.__selected_below_line = value
