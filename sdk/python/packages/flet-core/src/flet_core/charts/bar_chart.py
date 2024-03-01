import json
from typing import Any, List, Optional, Union

from flet_core.border import Border
from flet_core.charts.bar_chart_group import BarChartGroup
from flet_core.charts.chart_axis import ChartAxis
from flet_core.charts.chart_grid_lines import ChartGridLines
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.event_handler import EventHandler
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class BarChart(ConstrainedControl):
    def __init__(
        self,
        bar_groups: Optional[List[BarChartGroup]] = None,
        groups_space: OptionalNumber = None,
        animate: AnimationValue = None,
        interactive: Optional[bool] = None,
        bgcolor: Optional[str] = None,
        tooltip_bgcolor: Optional[str] = None,
        border: Optional[Border] = None,
        horizontal_grid_lines: Optional[ChartGridLines] = None,
        vertical_grid_lines: Optional[ChartGridLines] = None,
        left_axis: Optional[ChartAxis] = None,
        top_axis: Optional[ChartAxis] = None,
        right_axis: Optional[ChartAxis] = None,
        bottom_axis: Optional[ChartAxis] = None,
        baseline_y: OptionalNumber = None,
        min_y: OptionalNumber = None,
        max_y: OptionalNumber = None,
        on_chart_event=None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        def convert_linechart_event_data(e):
            d = json.loads(e.data)
            return BarChartEvent(**d)

        self.__on_chart_event = EventHandler(convert_linechart_event_data)
        self._add_event_handler("chart_event", self.__on_chart_event.get_handler())

        self.bar_groups = bar_groups
        self.groups_space = groups_space
        self.animate = animate
        self.interactive = interactive
        self.bgcolor = bgcolor
        self.tooltip_bgcolor = tooltip_bgcolor
        self.border = border
        self.horizontal_grid_lines = horizontal_grid_lines
        self.vertical_grid_lines = vertical_grid_lines
        self.left_axis = left_axis
        self.top_axis = top_axis
        self.right_axis = right_axis
        self.bottom_axis = bottom_axis
        self.baseline_y = baseline_y
        self.min_y = min_y
        self.max_y = max_y
        self.on_chart_event = on_chart_event

    def _get_control_name(self):
        return "barchart"

    def before_update(self):
        super().before_update()
        self._set_attr_json("horizontalGridLines", self.__horizontal_grid_lines)
        self._set_attr_json("verticalGridLines", self.__vertical_grid_lines)
        self._set_attr_json("animate", self.__animate)
        self._set_attr_json("border", self.__border)

    def _get_children(self):
        children = []
        for ds in self.__bar_groups:
            children.append(ds)
        if self.__left_axis:
            self.__left_axis._set_attr_internal("n", "l")
            children.append(self.__left_axis)
        if self.__top_axis:
            self.__top_axis._set_attr_internal("n", "t")
            children.append(self.__top_axis)
        if self.__right_axis:
            self.__right_axis._set_attr_internal("n", "r")
            children.append(self.__right_axis)
        if self.__bottom_axis:
            self.__bottom_axis._set_attr_internal("n", "b")
            children.append(self.__bottom_axis)
        return children

    # bar_groups
    @property
    def bar_groups(self):
        return self.__bar_groups

    @bar_groups.setter
    def bar_groups(self, value):
        self.__bar_groups = value if value is not None else []

    # groups_space
    @property
    def groups_space(self) -> OptionalNumber:
        return self._get_attr("groupsSpace", data_type="float")

    @groups_space.setter
    def groups_space(self, value: OptionalNumber):
        self._set_attr("groupsSpace", value)

    # animate
    @property
    def animate(self) -> AnimationValue:
        return self.__animate

    @animate.setter
    def animate(self, value: AnimationValue):
        self.__animate = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # interactive
    @property
    def interactive(self) -> Optional[bool]:
        return self._get_attr("interactive", data_type="bool", def_value=True)

    @interactive.setter
    def interactive(self, value: Optional[bool]):
        self._set_attr("interactive", value)

    # tooltip_bgcolor
    @property
    def tooltip_bgcolor(self) -> Optional[str]:
        return self._get_attr("tooltipBgcolor")

    @tooltip_bgcolor.setter
    def tooltip_bgcolor(self, value: Optional[str]):
        self._set_attr("tooltipBgcolor", value)

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    def border(self, value: Optional[Border]):
        self.__border = value

    # horizontal_grid_lines
    @property
    def horizontal_grid_lines(self) -> Optional[ChartGridLines]:
        return self.__horizontal_grid_lines

    @horizontal_grid_lines.setter
    def horizontal_grid_lines(self, value: Optional[ChartGridLines]):
        self.__horizontal_grid_lines = value

    # vertical_grid_lines
    @property
    def vertical_grid_lines(self) -> Optional[ChartGridLines]:
        return self.__vertical_grid_lines

    @vertical_grid_lines.setter
    def vertical_grid_lines(self, value: Optional[ChartGridLines]):
        self.__vertical_grid_lines = value

    # left_axis
    @property
    def left_axis(self) -> Optional[ChartAxis]:
        return self.__left_axis

    @left_axis.setter
    def left_axis(self, value: Optional[ChartAxis]):
        self.__left_axis = value

    # top_axis
    @property
    def top_axis(self) -> Optional[ChartAxis]:
        return self.__top_axis

    @top_axis.setter
    def top_axis(self, value: Optional[ChartAxis]):
        self.__top_axis = value

    # right_axis
    @property
    def right_axis(self) -> Optional[ChartAxis]:
        return self.__right_axis

    @right_axis.setter
    def right_axis(self, value: Optional[ChartAxis]):
        self.__right_axis = value

    # bottom_axis
    @property
    def bottom_axis(self) -> Optional[ChartAxis]:
        return self.__bottom_axis

    @bottom_axis.setter
    def bottom_axis(self, value: Optional[ChartAxis]):
        self.__bottom_axis = value

    # baseline_y
    @property
    def baseline_y(self) -> OptionalNumber:
        return self._get_attr("baseliney", data_type="float")

    @baseline_y.setter
    def baseline_y(self, value: OptionalNumber):
        self._set_attr("baseliney", value)

    # min_y
    @property
    def min_y(self) -> OptionalNumber:
        return self._get_attr("miny", data_type="float")

    @min_y.setter
    def min_y(self, value: OptionalNumber):
        self._set_attr("miny", value)

    # max_y
    @property
    def max_y(self) -> OptionalNumber:
        return self._get_attr("maxy", data_type="float")

    @max_y.setter
    def max_y(self, value: OptionalNumber):
        self._set_attr("maxy", value)

    # on_chart_event
    @property
    def on_chart_event(self):
        return self.__on_chart_event

    @on_chart_event.setter
    def on_chart_event(self, handler):
        self.__on_chart_event.subscribe(handler)
        if handler is not None:
            self._set_attr("onChartEvent", True)
        else:
            self._set_attr("onChartEvent", None)


class BarChartEvent(ControlEvent):
    def __init__(self, type, group_index, rod_index, stack_item_index) -> None:
        self.type: str = type
        self.group_index: int = group_index
        self.rod_index: int = rod_index
        self.stack_item_index: int = stack_item_index
