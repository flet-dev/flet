from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.border import Border, BorderSide
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEvent
from flet.controls.core.charts.chart_axis import ChartAxis
from flet.controls.core.charts.chart_grid_lines import ChartGridLines
from flet.controls.core.charts.scatter_chart_spot import ScatterChartSpot
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    OptionalColorValue,
    OptionalEventCallable,
    OptionalNumber,
)


class ScatterShartTooltipAlignment(Enum):
    START = "start"
    CENTER = "center"
    END = "end"


@dataclass
class ScatterChartEvent(ControlEvent):
    type: str
    """
    Type of the event (e.g. tapDown, panUpdate)
    """

    spot_index: Optional[int] = None
    """
    Index of the touched spot, if any
    """


@control("ScatterChart")
class ScatterChart(ConstrainedControl):
    scatter_spots: list[ScatterChartSpot] = field(default_factory=list)
    animate: Optional[AnimationValue] = None
    interactive: bool = True
    handle_built_in_touches: bool = True
    long_press_duration: Optional[int] = None
    bgcolor: OptionalColorValue = None
    border: Optional[Border] = None
    horizontal_grid_lines: Optional[ChartGridLines] = None
    vertical_grid_lines: Optional[ChartGridLines] = None
    left_axis: Optional[ChartAxis] = None
    top_axis: Optional[ChartAxis] = None
    right_axis: Optional[ChartAxis] = None
    bottom_axis: Optional[ChartAxis] = None
    baseline_x: OptionalNumber = None
    min_x: OptionalNumber = None
    max_x: OptionalNumber = None
    baseline_y: OptionalNumber = None
    min_y: OptionalNumber = None
    max_y: OptionalNumber = None
    tooltip_bgcolor: OptionalColorValue = None
    tooltip_rounded_radius: OptionalNumber = None
    tooltip_padding: OptionalPaddingValue = None
    tooltip_horizontal_offset: OptionalNumber = None
    tooltip_horizontal_alignment: Optional[ScatterShartTooltipAlignment] = None
    tooltip_border_side: Optional[BorderSide] = None
    tooltip_fit_inside_horizontally: Optional[bool] = None
    tooltip_fit_inside_vertically: Optional[bool] = None
    on_chart_event: OptionalEventCallable[ScatterChartEvent] = None
