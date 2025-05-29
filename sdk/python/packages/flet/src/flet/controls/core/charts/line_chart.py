from dataclasses import dataclass, field
from typing import Optional

from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.border import Border, BorderSide
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEvent
from flet.controls.core.charts.chart_axis import ChartAxis
from flet.controls.core.charts.chart_grid_lines import ChartGridLines
from flet.controls.core.charts.line_chart_data import LineChartData
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    OptionalColorValue,
    OptionalEventCallable,
    OptionalNumber,
)


@dataclass
class LineChartEventSpot:
    bar_index: int
    """
    The line's index or `-1` if no line was hovered.
    """

    spot_index: int
    """
    The line's point index or `-1` if no point was hovered.
    """


@dataclass
class LineChartEvent(ControlEvent):
    type: str
    """
    An event type such as `PointerHoverEvent`, `PointerExitEvent`, etc.
    """

    spots: list[LineChartEventSpot]
    """
    TBD
    """


@control("LineChart")
class LineChart(ConstrainedControl):
    """
    Draws a line chart.
    """

    data_series: list[LineChartData] = field(default_factory=list)
    """
    A list of [`LineChartData`](https://flet.dev/docs/reference/types/linechartdata)
    controls drawn as separate lines on a chart.
    """

    animate: Optional[AnimationValue] = None
    """
    Controls chart implicit animation.

    Value is of type [`AnimationValue`](https://flet.dev/docs/reference/types/animationvalue).
    """

    interactive: Optional[bool] = None
    """
    Enables automatic tooltips and points highlighting when hovering over the chart.
    """

    point_line_start: OptionalNumber = None
    """
    The start of the vertical line drawn under the selected point.

    Defaults to chart's bottom edge.
    """

    point_line_end: OptionalNumber = None
    """
    The end of the vertical line drawn at selected point position.

    Defaults to data point's `y` value.
    """

    bgcolor: OptionalColorValue = None
    """
    Background [color](https://flet.dev/docs/reference/colors) of the chart.
    """

    tooltip_bgcolor: OptionalColorValue = None
    """
    Background [color](https://flet.dev/docs/reference/colors) of tooltips.
    """

    border: Optional[Border] = None
    """
    The border around the chart.

    Value is of type [`Border`](https://flet.dev/docs/reference/types/border).
    """

    horizontal_grid_lines: Optional[ChartGridLines] = None
    """
    Controls drawing of chart's horizontal lines.

    Value is of type [`ChartGridLines`](https://flet.dev/docs/reference/types/chartgridlines).
    """

    vertical_grid_lines: Optional[ChartGridLines] = None
    """
    Controls drawing of chart's vertical lines.

    Value is of type [`ChartGridLines`](https://flet.dev/docs/reference/types/chartgridlines).
    """

    left_axis: Optional[ChartAxis] = None
    """
    Defines the appearance of the left axis, its title and labels.

    Value is of type [`ChartAxis`](https://flet.dev/docs/reference/types/chartaxis) 
    class.
    """

    top_axis: Optional[ChartAxis] = None
    """
    Defines the appearance of the top axis, its title and labels.

    Value is of type [`ChartAxis`](https://flet.dev/docs/reference/types/chartaxis).
    """

    right_axis: Optional[ChartAxis] = None
    """
    Defines the appearance of the right axis, its title and labels.

    Value is of type [`ChartAxis`](https://flet.dev/docs/reference/types/chartaxis) 
    class.
    """

    bottom_axis: Optional[ChartAxis] = None
    """
    Defines the appearance of the bottom axis, its title and labels.

    Value is of type [`ChartAxis`](https://flet.dev/docs/reference/types/chartaxis).
    """

    baseline_x: OptionalNumber = None
    """
    Baseline value for X axis.

    Defaults to `0`.
    """

    min_x: OptionalNumber = None
    """
    Defines the minimum displayed value for X axis.
    """

    max_x: OptionalNumber = None
    """
    Defines the maximum displayed value for X axis.
    """

    baseline_y: OptionalNumber = None
    """
    Baseline value for Y axis.

    Defaults to `0`.
    """

    min_y: OptionalNumber = None
    """
    Defines the minimum displayed value for Y axis.
    """

    max_y: OptionalNumber = None
    """
    Defines the maximum displayed value for Y axis.
    """

    tooltip_rounded_radius: OptionalNumber = None
    """
    Sets a rounded radius for the tooltip.
    """

    tooltip_margin: OptionalNumber = None
    """
    Applies a bottom margin for showing tooltip on top of rods.
    """

    tooltip_padding: OptionalPaddingValue = None
    """
    Applies a padding for showing contents inside the tooltip.

    Value is of type [`PaddingValue`](https://flet.dev/docs/reference/types/aliases#paddingvalue).
    """

    tooltip_max_content_width: OptionalNumber = None
    """
    Restricts the tooltip's width.
    """

    tooltip_rotate_angle: OptionalNumber = None
    """
    The rotation angle of the tooltip.
    """

    tooltip_horizontal_offset: OptionalNumber = None
    """
    Applies horizontal offset for showing tooltip.
    """

    tooltip_border_side: Optional[BorderSide] = None
    """
    The tooltip border side.
    """

    tooltip_fit_inside_horizontally: Optional[bool] = None
    """
    Forces the tooltip to shift horizontally inside the chart, if overflow happens.

    Value is of type `bool`.
    """

    tooltip_fit_inside_vertically: Optional[bool] = None
    """
    Forces the tooltip to shift vertically inside the chart, if overflow happens.

    Value is of type `bool`.
    """

    tooltip_show_on_top_of_chart_box_area: Optional[bool] = None
    """
    Whether to force the tooltip container to the top of the line.

    Value is of type `bool` and defaults to `False`.
    """

    _skip_inherited_notifier: Optional[bool] = None
    """
    TBD
    """

    on_chart_event: OptionalEventCallable[LineChartEvent] = None
    """
    Fires when a chart line is hovered or clicked.

    Value is of type [`LineChartEvent`](https://flet.dev/docs/reference/types/linechartevent).
    """

    def init(self):
        super().init()
        self._skip_inherited_notifier = True
