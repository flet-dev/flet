from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.control import Control
from flet.controls.core.charts.bar_chart_rod_stack_item import BarChartRodStackItem
from flet.controls.gradients import Gradient
from flet.controls.text_style import TextStyle
from flet.controls.types import OptionalColorValue, OptionalNumber, TextAlign


@control("r", kw_only=True)
class BarChartRod(Control):
    rod_stack_items: list[BarChartRodStackItem] = field(default_factory=list)
    """
    Optional list of [`BarChartRodStackItem`](https://flet.dev/docs/reference/types/
    barchartrodstackitem) objects to draw a stacked bar.
    """

    from_y: OptionalNumber = None
    """
    Specifies a starting position of this rod on Y axis.

    Defaults to `0`.
    """

    to_y: OptionalNumber = None
    """
    Specifies an ending position of this rod on Y axis.
    """

    width: OptionalNumber = None
    """
    The width of this rod.

    Defaults to `8`.
    """

    color: OptionalColorValue = None
    """
    Rod [color](https://flet.dev/docs/reference/colors).

    Defaults to `Colors.CYAN`.
    """

    gradient: Optional[Gradient] = None
    """
    Gradient to draw rod's background.

    Value is of type [`Gradient`](https://flet.dev/docs/reference/types/gradient).
    """

    border_radius: OptionalBorderRadiusValue = None
    """
    Border radius of a bar rod.

    Defaults to `4`.
    """

    border_side: Optional[BorderSide] = None
    """
    Border to draw around rod.

    Value is of type [`BorderSide`](https://flet.dev/docs/reference/types/borderside)
    class.
    """

    bg_from_y: OptionalNumber = None
    """
    An optional starting position of a background behind this rod.
    """

    bg_to_y: OptionalNumber = None
    """
    An optional ending position of a background behind this rod.
    """

    bg_color: OptionalColorValue = None
    """
    An optional [color](https://flet.dev/docs/reference/colors) of a background behind
    this rod.
    """

    bg_gradient: Optional[Gradient] = None
    """
    An optional gradient to draw a background with.
    """

    selected: Optional[bool] = None
    """
    If set to `True` a tooltip is always shown on top of the bar when
    `BarChart.interactive` is set to `False`.
    """

    show_tooltip: bool = True
    """
    Whether a tooltip should be shown on top of hovered bar.

    Defaults to `True`.
    """

    tooltip: Optional[str] = None
    """
    A custom tooltip value.

    Defaults to `to_y`.
    """

    tooltip_style: Optional[TextStyle] = None
    """
    A text style to display tooltip with.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    tooltip_align: Optional[TextAlign] = None
    """
    An align for the tooltip.

    Value is of type [`TextAlign`](https://flet.dev/docs/reference/types/textalign).
    """

