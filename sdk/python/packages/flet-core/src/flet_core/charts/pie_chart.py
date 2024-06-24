import json
from typing import Any, List, Optional, Union, Callable

from flet_core.charts.pie_chart_section import PieChartSection
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
    OptionalEventCallable,
)


class PieChart(ConstrainedControl):
    def __init__(
        self,
        sections: Optional[List[PieChartSection]] = None,
        center_space_color: Optional[str] = None,
        center_space_radius: OptionalNumber = None,
        sections_space: OptionalNumber = None,
        start_degree_offset: OptionalNumber = None,
        animate: AnimationValue = None,
        on_chart_event: Optional[Callable[["PieChartEvent"], None]] = None,
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
        on_animation_end: OptionalEventCallable = None,
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

        self.__on_chart_event = EventHandler(lambda e: PieChartEvent(e))
        self._add_event_handler("chart_event", self.__on_chart_event.get_handler())

        self.sections = sections
        self.center_space_color = center_space_color
        self.center_space_radius = center_space_radius
        self.sections_space = sections_space
        self.start_degree_offset = start_degree_offset
        self.animate = animate
        self.on_chart_event = on_chart_event

    def _get_control_name(self):
        return "piechart"

    def before_update(self):
        super().before_update()
        self._set_attr_json("animate", self.__animate)

    def _get_children(self):
        children = []
        for ds in self.__sections:
            children.append(ds)
        return children

    # sections
    @property
    def sections(self):
        return self.__sections

    @sections.setter
    def sections(self, value):
        self.__sections = value if value is not None else []

    # center_space_color
    @property
    def center_space_color(self) -> Optional[str]:
        return self._get_attr("centerSpaceColor")

    @center_space_color.setter
    def center_space_color(self, value: Optional[str]):
        self._set_attr("centerSpaceColor", value)

    # center_space_radius
    @property
    def center_space_radius(self) -> OptionalNumber:
        return self._get_attr("centerSpaceRadius", data_type="float")

    @center_space_radius.setter
    def center_space_radius(self, value: OptionalNumber):
        self._set_attr("centerSpaceRadius", value)

    # sections_space
    @property
    def sections_space(self) -> OptionalNumber:
        return self._get_attr("sectionsSpace", data_type="float")

    @sections_space.setter
    def sections_space(self, value: OptionalNumber):
        self._set_attr("sectionsSpace", value)

    # start_degree_offset
    @property
    def start_degree_offset(self) -> OptionalNumber:
        return self._get_attr("startDegreeOffset", data_type="float")

    @start_degree_offset.setter
    def start_degree_offset(self, value: OptionalNumber):
        self._set_attr("startDegreeOffset", value)

    # animate
    @property
    def animate(self) -> AnimationValue:
        return self.__animate

    @animate.setter
    def animate(self, value: AnimationValue):
        self.__animate = value

    # on_chart_event
    @property
    def on_chart_event(self):
        return self.__on_chart_event

    @on_chart_event.setter
    def on_chart_event(self, handler: Optional[Callable[["PieChartEvent"], None]]):
        self.__on_chart_event.subscribe(handler)
        self._set_attr("onChartEvent", True if handler is not None else None)


class PieChartEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.type: str = d["type"]
        self.section_index: int = d["section_index"]
        # self.radius: float = d["radius"]
        # self.angle: float = d["angle"]
