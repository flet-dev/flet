from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.animation import OptionalAnimationValue
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
    """
    Type of the event.

    Value is of type [`PieChartEventType`](https://flet.dev/docs/reference/types/piecharteventtype).
    """

    section_index: Optional[int] = None
    """
    Section's index or `-1` if no section was hovered.
    """

    local_x: Optional[float] = None
    """
    X coordinate of the local position where the event occurred.
    """

    local_y: Optional[float] = None
    """
    Y coordinate of the local position where the event occurred.
    """


@control("PieChart")
class PieChart(ConstrainedControl):
    sections: list[PieChartSection] = field(default_factory=list)
    center_space_color: OptionalColorValue = None
    center_space_radius: OptionalNumber = None
    sections_space: OptionalNumber = None
    start_degree_offset: OptionalNumber = None
    animate: OptionalAnimationValue = None
    on_chart_event: OptionalEventCallable[PieChartEvent] = None
