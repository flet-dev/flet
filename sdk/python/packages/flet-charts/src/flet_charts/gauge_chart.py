from dataclasses import dataclass, field
from enum import Enum
from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V, ValidationRules
from flet_charts.gauge_marker import GaugeMarker
from flet_charts.gauge_pointer import GaugePointer
from flet_charts.gauge_ring import GaugeProgressRing, GaugeRing, GaugeZonesRing
from flet_charts.gauge_ticks import GaugeTicks
from flet_charts.types import ChartEventType

__all__ = ["GaugeChart", "GaugeChartEvent", "GaugeDirection"]


class GaugeDirection(Enum):
    """
    The direction in which the arc of a :class:`~flet_charts.GaugeChart` travels
    from its start.
    """

    CLOCKWISE = "clockwise"
    """
    The arc travels clockwise.
    """

    COUNTER_CLOCKWISE = "counterClockwise"
    """
    The arc travels counter-clockwise.
    """


@dataclass
class GaugeChartEvent(ft.Event["GaugeChart"]):
    """
    Event raised for interactions with a :class:`~flet_charts.GaugeChart`.
    """

    type: ChartEventType
    """
    The touch or pointer event that occurred.
    """

    ring_index: Optional[int] = None
    """
    The index of the touched ring in :attr:`flet_charts.GaugeChart.rings`.

    `None` if the touch is outside the arc, between rings or outside every ring.
    """

    zone_index: Optional[int] = None
    """
    The index of the touched zone in :attr:`flet_charts.GaugeZonesRing.zones`.

    `None` if the touched ring isn't a :class:`~flet_charts.GaugeZonesRing`, or if
    the touch is between zones.
    """

    value: Optional[float] = None
    """
    The value on the gauge's scale at the angle of the touch.

    It is set whenever the touch is within the angle of the arc, even between or
    outside the rings. `None` if the touch is outside the arc.
    """

    angle: Optional[float] = None
    """
    The angle of the touch around the center of the gauge, in degrees.

    `0` points right and angles increase clockwise, as in
    :attr:`flet_charts.GaugeChart.start_degree_offset`. `None` if the touch is
    outside the arc.
    """

    radius: Optional[float] = None
    """
    The distance from the center of the gauge to the touch, in logical pixels.

    `None` if the touch is outside the arc.
    """

    on_value: bool = False
    """
    Whether the touch is on the filled part of a
    :class:`~flet_charts.GaugeProgressRing`.
    """


def _progress_ring_values_in_range(chart: "GaugeChart") -> bool:
    return all(
        chart.min_value <= ring.value <= chart.max_value
        for ring in chart.rings
        if isinstance(ring, GaugeProgressRing)
    )


def _zones_in_range(chart: "GaugeChart") -> bool:
    return all(
        zone.start >= chart.min_value and zone.end <= chart.max_value
        for ring in chart.rings
        if isinstance(ring, GaugeZonesRing)
        for zone in ring.zones
    )


@ft.control("GaugeChart")
class GaugeChart(ft.LayoutControl):
    """
    A gauge made of one or more rings bent along an arc, with optional ticks,
    markers and pointers.

    It can be drawn as a progress indicator, an activity-style set of concentric
    rings, or a speedometer with colored zones and a needle.

    ```python
    fch.GaugeChart(
        min_value=0,
        max_value=100,
        rings=[fch.GaugeProgressRing(value=72, bgcolor=ft.Colors.BLACK_12)],
        pointers=[fch.GaugeNeedlePointer(value=72)],
    )
    ```

    To show content in the middle of the gauge, such as the current value, place
    the chart and the content in an :class:`~flet.Stack`.
    """

    rings: list[GaugeRing] = field(default_factory=list)
    """
    The rings of this gauge, from the innermost to the outermost.

    Each ring is either a :class:`~flet_charts.GaugeProgressRing` or a
    :class:`~flet_charts.GaugeZonesRing`. All rings share the scale between
    :attr:`min_value` and :attr:`max_value`.

    Raises:
        ValueError: If the :attr:`~flet_charts.GaugeProgressRing.value` of a
            :class:`~flet_charts.GaugeProgressRing` is not between :attr:`min_value`
            and :attr:`max_value`, inclusive.
        ValueError: If a :class:`~flet_charts.GaugeZone` of a
            :class:`~flet_charts.GaugeZonesRing` starts before :attr:`min_value` or
            ends after :attr:`max_value`.
    """

    min_value: ft.Number = 0.0
    """
    The lowest value of the gauge's scale, at the start of the arc.
    """

    max_value: Annotated[ft.Number, V.gt_field("min_value")] = 1.0
    """
    The highest value of the gauge's scale, at the end of the arc.

    Raises:
        ValueError: If it is not strictly greater than :attr:`min_value`.
    """

    start_degree_offset: ft.Number = -225.0
    """
    The angle at which the arc starts, in degrees.

    `0` points right and angles increase clockwise, so the default of `-225`,
    together with the default :attr:`sweep_angle`, draws an arc open at the
    bottom.
    """

    sweep_angle: Annotated[ft.Number, V.gt(0), V.le(360)] = 270.0
    """
    The length of the arc, in degrees.

    Raises:
        ValueError: If it is not strictly greater than `0`.
        ValueError: If it is not less than or equal to `360`.
    """

    direction: GaugeDirection = GaugeDirection.CLOCKWISE
    """
    The direction in which the arc travels from :attr:`start_degree_offset`.
    """

    default_ring_width: ft.Number = 10.0
    """
    The width of the rings whose :attr:`~flet_charts.GaugeRing.width` isn't set,
    in logical pixels.
    """

    rings_space: Annotated[ft.Number, V.ge(0)] = 0.0
    """
    The gap between adjacent rings, in logical pixels.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    ticks: Optional[GaugeTicks] = None
    """
    The tick marks drawn along the arc.

    Either a :class:`~flet_charts.GaugeLineTicks` or a
    :class:`~flet_charts.GaugeCircleTicks`. If `None`, no ticks are drawn.
    """

    markers: list[GaugeMarker] = field(default_factory=list)
    """
    The markers drawn along the arc, each at its own value.
    """

    pointers: list[GaugePointer] = field(default_factory=list)
    """
    The pointers drawn on top of the gauge, in order.

    Each pointer is either a :class:`~flet_charts.GaugeNeedlePointer` or a
    :class:`~flet_charts.GaugeCirclePointer`.
    """

    border: Optional[ft.Border] = None
    """
    The border drawn around this chart.
    """

    animation: ft.AnimationValue = field(
        default_factory=lambda: ft.Animation(
            duration=ft.Duration(milliseconds=150), curve=ft.AnimationCurve.LINEAR
        )
    )
    """
    Controls the implicit animation applied when updating this chart.
    """

    interactive: bool = True
    """
    Enables touch interactions and event notifications.
    """

    long_press_duration: Optional[ft.DurationValue] = None
    """
    The duration before a long-press event fires.
    """

    on_event: Optional[ft.EventHandler[GaugeChartEvent]] = None
    """
    Called when the chart is interacted with.
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            _progress_ring_values_in_range,
            message=(
                "the value of every GaugeProgressRing must be between min_value "
                "and max_value, inclusive"
            ),
        ),
        V.ensure(
            _zones_in_range,
            message=(
                "every GaugeZone must start and end between min_value and "
                "max_value, inclusive"
            ),
        ),
    )
