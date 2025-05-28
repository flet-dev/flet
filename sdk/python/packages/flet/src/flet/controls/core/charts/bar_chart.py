from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.animation import AnimationValue
from flet.controls.base_control import control
from flet.controls.border import Border, BorderSide
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEvent
from flet.controls.core.charts.bar_chart_group import BarChartGroup
from flet.controls.core.charts.chart_axis import ChartAxis
from flet.controls.core.charts.chart_grid_lines import ChartGridLines
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    OptionalColorValue,
    OptionalEventCallable,
    OptionalNumber,
)


class TooltipDirection(Enum):
    AUTO = "auto"
    TOP = "top"
    BOTTOM = "bottom"


@dataclass
class BarChartEvent(ControlEvent):
    type: str
    group_index: Optional[int] = None
    rod_index: Optional[int] = None
    stack_item_index: Optional[int] = None


@control("BarChart")
class BarChart(ConstrainedControl):
    """
    Draws a bar chart.
    """

    bar_groups: list[BarChartGroup] = field(default_factory=list)
    """
    The list of [`BarChartGroup`](https://flet.dev/docs/reference/types/barchartgroup)
    to draw.
    """

    groups_space: OptionalNumber = None
    """
    A gap between bar groups.
    """

    animate: Optional[AnimationValue] = None
    """
    Controls chart implicit animation.

    Value is of [`AnimationValue`](https://flet.dev/docs/reference/types/animationvalue)
    type.
    """

    interactive: Optional[bool] = None
    """
    Enables automatic tooltips when hovering chart bars.
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

    Value is of type
    [`ChartGridLines`](https://flet.dev/docs/reference/types/chartgridlines).
    """

    vertical_grid_lines: Optional[ChartGridLines] = None
    """
    Controls drawing of chart's vertical lines.

    Value is of type
    [`ChartGridLines`](https://flet.dev/docs/reference/types/chartgridlines).
    """

    left_axis: Optional[ChartAxis] = None
    """
    Configures the appearance of the left axis, its title and labels.

    Value is of type [`ChartAxis`](https://flet.dev/docs/reference/types/chartaxis).
    """

    top_axis: Optional[ChartAxis] = None
    """
    Configures the appearance of the top axis, its title and labels.

    Value is of type [`ChartAxis`](https://flet.dev/docs/reference/types/chartaxis).
    """

    right_axis: Optional[ChartAxis] = None
    """
    Configures the appearance of the right axis, its title and labels.

    Value is of type [`ChartAxis`](https://flet.dev/docs/reference/types/chartaxis).
    """

    bottom_axis: Optional[ChartAxis] = None
    """
    Configures the appearance of the bottom axis, its title and labels.

    Value is of type [`ChartAxis`](https://flet.dev/docs/reference/types/chartaxis).
    """

    baseline_y: OptionalNumber = None
    """
    Baseline value for Y axis.

    Defaults to `0`.
    """

    min_y: OptionalNumber = None
    """
    Configures the minimum displayed value for Y axis.
    """

    max_y: OptionalNumber = None
    """
    Configures the maximum displayed value for Y axis.
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
    """

    tooltip_max_content_width: OptionalNumber = None
    """
    Restricts the tooltip's width.
    """

    tooltip_rotate_angle: OptionalNumber = None
    """
    The rotation angle of the tooltip.
    """

    tooltip_tooltip_horizontal_offset: OptionalNumber = None
    """
    Applies horizontal offset for showing tooltip.

    Defaults to `0`.
    """

    tooltip_tooltip_border_side: Optional[BorderSide] = None
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

    tooltip_direction: Optional[TooltipDirection] = None
    """
    Controls showing tooltip on top or bottom, default is auto.
    """

    on_chart_event: OptionalEventCallable["BarChartEvent"] = None
    """
    Fires when a bar is hovered or clicked.

    Event handler receives an instance of
    [`BarChartEvent`](https://flet.dev/docs/reference/types/barchartevent).
    """

