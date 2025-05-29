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
    """
    A scatter chart control.

    ScatterChart draws some points in a square space, points are defined by 
    ScatterSpots.
    """
    scatter_spots: list[ScatterChartSpot] = field(default_factory=list)
    """
    List of ScatterChartSpots to show on the chart.
    """
    animate: Optional[AnimationValue] = None
    """
    TBD
    """
    interactive: bool = True
    """
    TBD
    """
    handle_built_in_touches: bool = True
    """
    TBD
    """
    long_press_duration: Optional[int] = None
    """
    TBD
    """
    bgcolor: OptionalColorValue = None
    """
    TBD
    """
    border: Optional[Border] = None
    """
    TBD
    """
    horizontal_grid_lines: Optional[ChartGridLines] = None
    """
    TBD
    """
    vertical_grid_lines: Optional[ChartGridLines] = None
    """
    TBD
    """
    left_axis: Optional[ChartAxis] = None
    """
    TBD
    """
    top_axis: Optional[ChartAxis] = None
    """
    TBD
    """
    right_axis: Optional[ChartAxis] = None
    """
    TBD
    """
    bottom_axis: Optional[ChartAxis] = None
    """
    TBD
    """
    baseline_x: OptionalNumber = None
    """
    TBD
    """
    min_x: OptionalNumber = None
    """
    TBD
    """
    max_x: OptionalNumber = None
    """
    TBD
    """
    baseline_y: OptionalNumber = None
    """
    TBD
    """
    min_y: OptionalNumber = None
    """
    TBD
    """
    max_y: OptionalNumber = None
    """
    TBD
    """
    tooltip_bgcolor: OptionalColorValue = None
    """
    TBD
    """
    tooltip_rounded_radius: OptionalNumber = None
    """
    TBD
    """
    tooltip_padding: OptionalPaddingValue = None
    """
    TBD
    """
    tooltip_horizontal_offset: OptionalNumber = None
    """
    TBD
    """
    tooltip_horizontal_alignment: Optional[ScatterShartTooltipAlignment] = None
    """
    TBD
    """
    tooltip_border_side: Optional[BorderSide] = None
    """
    TBD
    """
    tooltip_fit_inside_horizontally: Optional[bool] = None
    """
    TBD
    """
    tooltip_fit_inside_vertically: Optional[bool] = None
    """
    TBD
    """
    on_chart_event: OptionalEventCallable[ScatterChartEvent] = None
    """
    TBD
    """