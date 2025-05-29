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
    """
    A pie chart control displaying multiple sections as slices of a circle.
    """

    sections: list[PieChartSection] = field(default_factory=list)
    """
    A list of [`PieChartSection`](https://flet.dev/docs/reference/types/piechartsection)
    controls drawn in a circle.
    """

    center_space_color: OptionalColorValue = None
    """
    Free space [color](https://flet.dev/docs/reference/colors) in the middle of a chart.
    """

    center_space_radius: OptionalNumber = None
    """
    Free space radius in the middle of a chart.
    """

    sections_space: OptionalNumber = None
    """
    A gap between `sections`.
    """

    start_degree_offset: OptionalNumber = None
    """
    By default, `sections` are drawn from zero degree (right side of the circle)
    clockwise. You can change the starting point by setting `start_degree_offset`
    (in degrees).
    """

    animate: OptionalAnimationValue = None
    """
    Controls chart implicit animation.

    Value is of type [`AnimationValue`](https://flet.dev/docs/reference/types/animationvalue).
    """

    on_chart_event: OptionalEventCallable[PieChartEvent] = None
    """
    Fires when a chart section is hovered or clicked.

    Event data is an instance [`PieChartEvent`](https://flet.dev/docs/reference/types/piechartevent).
    """

