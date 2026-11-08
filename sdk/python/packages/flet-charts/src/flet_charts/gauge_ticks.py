from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V, ValidationRules
from flet_charts.types import GaugeTickPosition

__all__ = ["GaugeCircleTicks", "GaugeLineTicks", "GaugeTicks"]


@ft.control(kw_only=True)
class GaugeTicks(ft.BaseControl):
    """
    Base class for the tick marks of a :class:`~flet_charts.GaugeChart`.

    Ticks are spaced evenly along the gauge's arc, with the first one at the start
    of the arc and the last one at its end. They are positioned relative to the
    whole stack of rings, not to a single ring.

    See usable subclasses:

    * :class:`~flet_charts.GaugeLineTicks`
    * :class:`~flet_charts.GaugeCircleTicks`
    """

    count: Annotated[int, V.ge(2)] = 3
    """
    The number of ticks, including the ones at both ends of the arc.

    Raises:
        ValueError: If it is not greater than or equal to `2`.
    """

    position: GaugeTickPosition = GaugeTickPosition.OUTER
    """
    Where the ticks sit relative to the rings.
    """

    offset: ft.Number = 0
    """
    The distance, in logical pixels, by which the ticks are moved from their
    :attr:`position`.

    It is measured away from the center for :attr:`flet_charts.GaugeTickPosition.OUTER`
    and :attr:`flet_charts.GaugeTickPosition.CENTER`, and toward the center for
    :attr:`flet_charts.GaugeTickPosition.INNER`. Negative values move the ticks the
    other way.
    """

    show_endpoints: bool = True
    """
    Whether the ticks at both ends of the arc, and their labels, are drawn.

    Hiding them helps when the ends of the rings already mark the extremes of the
    scale, for example with round zone ends.
    """

    labels: Optional[list[str]] = None
    """
    The labels drawn next to the ticks, one per tick, from the start of the arc to
    its end.

    An empty string keeps a tick without a label. If `None`, no labels are drawn.
    Labels stay upright whatever the angle of their tick.

    Raises:
        ValueError: If its length is not equal to :attr:`count`, when set.
    """

    label_style: Optional[ft.TextStyle] = None
    """
    The text style of the :attr:`labels`.
    """

    label_offset: ft.Number = 0
    """
    The distance, in logical pixels, between the far edge of a tick and its label.

    Negative values pull the label toward, or across, the tick.
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda ticks: ticks.labels is None or len(ticks.labels) == ticks.count,
            message="labels must contain exactly count items",
        ),
    )


@ft.control("GaugeLineTicks")
class GaugeLineTicks(GaugeTicks):
    """
    Draws each tick as a straight line pointing away from the gauge's rings.
    """

    length: Annotated[ft.Number, V.gt(0)] = 6.0
    """
    The length of each tick, in logical pixels.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    thickness: Annotated[ft.Number, V.gt(0)] = 2.0
    """
    The thickness of each tick, in logical pixels.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the ticks.

    Defaults to :attr:`flet.ColorScheme.on_surface`.
    """


@ft.control("GaugeCircleTicks")
class GaugeCircleTicks(GaugeTicks):
    """
    Draws each tick as a filled circle, with an optional outline.
    """

    radius: Annotated[ft.Number, V.gt(0)] = 3.0
    """
    The radius of each tick, in logical pixels.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    color: Optional[ft.ColorValue] = None
    """
    The fill color of the ticks.

    Defaults to :attr:`flet.ColorScheme.on_surface`.
    """

    stroke_width: ft.Number = 0
    """
    The width of the outline drawn around each tick.

    If `0`, no outline is drawn.
    """

    stroke_color: Optional[ft.ColorValue] = None
    """
    The color of the outline drawn around each tick.

    Defaults to :attr:`flet.ColorScheme.on_surface`.
    """
