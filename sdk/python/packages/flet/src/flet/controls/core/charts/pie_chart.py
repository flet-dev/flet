from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEvent
from flet.controls.core.charts.pie_chart_section import PieChartSection
from flet.controls.types import (
    OptionalColorValue,
    OptionalEventCallable,
    OptionalNumber,
)


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


@dataclass
class PieChartEvent(ControlEvent):
    type: PieChartEventType
    section_index: Optional[int]
    local_x: Optional[float] = field(metadata={"data_field": "lx"})
    local_y: Optional[float] = field(metadata={"data_field": "ly"})


@control("PieChart")
class PieChart(ConstrainedControl):
    sections: List[PieChartSection] = field(default_factory=list)
    center_space_color: OptionalColorValue = None
    center_space_radius: OptionalNumber = None
    sections_space: OptionalNumber = None
    start_degree_offset: OptionalNumber = None
    animate: Optional[AnimationValue] = None
    on_chart_event: OptionalEventCallable[PieChartEvent] = None
