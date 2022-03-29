from typing import Optional, Union

from beartype import beartype

from flet.control import Control

try:
    from typing import Literal
except:
    from typing_extensions import Literal


XType = Literal[None, "number", "date"]


class LineChart(Control):
    def __init__(
        self,
        id=None,
        ref=None,
        legend=None,
        tooltips=None,
        stroke_width=None,
        y_min=None,
        y_max=None,
        y_ticks=None,
        y_format=None,
        x_type: XType = None,
        lines=None,
        width=None,
        height=None,
        padding=None,
        margin=None,
        visible=None,
        disabled=None,
    ):

        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            visible=visible,
            disabled=disabled,
        )

        self.__lines = []
        if lines != None:
            for line in lines:
                self.__lines.append(line)

        self.legend = legend
        self.tooltips = tooltips
        self.stroke_width = stroke_width
        self.y_min = y_min
        self.y_max = y_max
        self.y_ticks = y_ticks
        self.y_format = y_format
        self.x_type = x_type

    def _get_control_name(self):
        return "linechart"

    # lines
    @property
    def lines(self):
        return self.__lines

    @lines.setter
    def lines(self, value):
        self.__lines = value

    # legend
    @property
    def legend(self):
        return self._get_attr("legend", data_type="bool", def_value=False)

    @legend.setter
    @beartype
    def legend(self, value: Optional[bool]):
        self._set_attr("legend", value)

    # tooltips
    @property
    def tooltips(self):
        return self._get_attr("tooltips", data_type="bool", def_value=False)

    @tooltips.setter
    @beartype
    def tooltips(self, value: Optional[bool]):
        self._set_attr("tooltips", value)

    # stroke_width
    @property
    def stroke_width(self):
        return self._get_attr("strokeWidth")

    @stroke_width.setter
    @beartype
    def stroke_width(self, value: Optional[int]):
        self._set_attr("strokeWidth", value)

    # y_min
    @property
    def y_min(self):
        return self._get_attr("yMin")

    @y_min.setter
    @beartype
    def y_min(self, value: Union[None, int, float]):
        self._set_attr("yMin", value)

    # y_max
    @property
    def y_max(self):
        return self._get_attr("yMax")

    @y_max.setter
    @beartype
    def y_max(self, value: Union[None, int, float]):
        self._set_attr("yMax", value)

    # y_ticks
    @property
    def y_ticks(self):
        return self._get_attr("yTicks")

    @y_ticks.setter
    @beartype
    def y_ticks(self, value: Optional[int]):
        self._set_attr("yTicks", value)

    # y_format
    @property
    def y_format(self):
        return self._get_attr("yFormat")

    @y_format.setter
    def y_format(self, value):
        self._set_attr("yFormat", value)

    # x_type
    @property
    def x_type(self):
        return self._get_attr("xType")

    @x_type.setter
    @beartype
    def x_type(self, value: XType):
        self._set_attr("xType", value)

    def _get_children(self):
        return self.__lines


class Data(Control):
    def __init__(self, id=None, ref=None, color=None, legend=None, points=None):
        Control.__init__(self, id=id, ref=ref)

        self.color = color
        self.legend = legend
        self.__points = []
        if points != None:
            for point in points:
                self.__points.append(point)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # legend
    @property
    def legend(self):
        return self._get_attr("legend")

    @legend.setter
    def legend(self, value):
        self._set_attr("legend", value)

    # points
    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, value):
        self.__points = value

    def _get_control_name(self):
        return "data"

    def _get_children(self):
        return self.__points


class Point(Control):
    def __init__(
        self,
        id=None,
        ref=None,
        x=None,
        y=None,
        tick=None,
        legend=None,
        x_tooltip=None,
        y_tooltip=None,
    ):
        Control.__init__(self, id=id, ref=ref)

        self.x = x
        self.y = y
        self.tick = tick
        self.legend = legend
        self.x_tooltip = x_tooltip
        self.y_tooltip = y_tooltip

    def _get_control_name(self):
        return "p"

    # x
    @property
    def x(self):
        return self._get_attr("x")

    @x.setter
    def x(self, value):
        self._set_attr("x", value)

    # y
    @property
    def y(self):
        return self._get_attr("y")

    @y.setter
    @beartype
    def y(self, value: Union[None, int, float]):
        self._set_attr("y", value)

    # tick
    @property
    def tick(self):
        return self._get_attr("tick")

    @tick.setter
    def tick(self, value):
        self._set_attr("tick", value)

    # legend
    @property
    def legend(self):
        return self._get_attr("legend")

    @legend.setter
    def legend(self, value):
        self._set_attr("legend", value)

    # x_tooltip
    @property
    def x_tooltip(self):
        return self._get_attr("xTooltip")

    @x_tooltip.setter
    def x_tooltip(self, value):
        self._set_attr("xTooltip", value)

    # y_tooltip
    @property
    def y_tooltip(self):
        return self._get_attr("yTooltip")

    @y_tooltip.setter
    def y_tooltip(self, value):
        self._set_attr("yTooltip", value)
