import json
from enum import Enum
from typing import Any, List, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.charts.pie_chart_section import PieChartSection
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class PieChart(ConstrainedControl):
    def __init__(
        self,
        sections: Optional[List[PieChartSection]] = None,
        center_space_color: Optional[ColorValue] = None,
        center_space_radius: OptionalNumber = None,
        sections_space: OptionalNumber = None,
        start_degree_offset: OptionalNumber = None,
        animate: Optional[AnimationValue] = None,
        on_chart_event: OptionalEventCallable["PieChartEvent"] = None,
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
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
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
            badge=badge,
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
    def center_space_color(self) -> Optional[ColorValue]:
        return self.__center_space_color

    @center_space_color.setter
    def center_space_color(self, value: Optional[ColorValue]):
        self.__center_space_color = value
        self._set_enum_attr("centerSpaceColor", value, ColorEnums)

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
    def on_chart_event(self) -> OptionalEventCallable["PieChartEvent"]:
        return self.__on_chart_event.handler

    @on_chart_event.setter
    def on_chart_event(self, handler: OptionalEventCallable["PieChartEvent"]):
        self.__on_chart_event.handler = handler
        self._set_attr("onChartEvent", True if handler is not None else None)


class PieChartEventType(Enum):
    POINTER_ENTER = "pointerEnter"
    POINTER_EXIT = "pointerExit"
    POINTER_HOVER = "pointerHover"
    PAN_CANCEL = "panCancel"
    PAN_DOWN = "panDown"
    PAN_END = "panEnd"
    PAN_START = "panStart"
    PAN_UPDATE = "panUpdate"
    LONG_PRESS_END = "longPressEnd"
    LONG_PRESS_MOVE_UPDATE = "longPressMoveUpdate"
    LONG_PRESS_START = "longPressStart"
    TAP_CANCEL = "tapCancel"
    TAP_DOWN = "tapDown"
    TAP_UP = "tapUp"
    UNDEFINED = "undefined"


class PieChartEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.type: PieChartEventType = PieChartEventType(d.get("type"))
        self.section_index: int = d.get("section_index")
        self.local_x: Optional[float] = d.get("lx")
        self.local_y: Optional[float] = d.get("ly")
        # self.radius: float = d["radius"]
        # self.angle: float = d["angle"]
