from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V

__all__ = ["GaugeProgressRing", "GaugeRing", "GaugeZone", "GaugeZonesRing"]


@ft.control(kw_only=True)
class GaugeRing(ft.BaseControl):
    """
    Base class for the rings of a :class:`~flet_charts.GaugeChart`.

    See usable subclasses:

    * :class:`~flet_charts.GaugeProgressRing`
    * :class:`~flet_charts.GaugeZonesRing`
    """

    width: Annotated[Optional[ft.Number], V.gt(0)] = None
    """
    The radial thickness of this ring, in logical pixels.

    Defaults to :attr:`flet_charts.GaugeChart.default_ring_width`.

    Raises:
        ValueError: If it is not strictly greater than `0`, when set.
    """


@ft.control("GaugeProgressRing")
class GaugeProgressRing(GaugeRing):
    """
    A ring filled from :attr:`flet_charts.GaugeChart.min_value` up to its
    :attr:`value`, like a progress bar bent along the gauge's arc.
    """

    value: ft.Number
    """
    The value the ring is filled up to.

    Must be between :attr:`flet_charts.GaugeChart.min_value` and
    :attr:`flet_charts.GaugeChart.max_value`, inclusive.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the filled part of this ring.

    Defaults to :attr:`flet.ColorScheme.primary`.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The color of the unfilled part of this ring.

    If `None`, the unfilled part is not drawn.
    """

    stroke_cap: ft.StrokeCap = ft.StrokeCap.BUTT
    """
    The shape of the ends of the filled part and of the background track.
    """


@ft.control("GaugeZone")
class GaugeZone(ft.BaseControl):
    """
    A colored band of a :class:`~flet_charts.GaugeZonesRing`, spanning the scale from
    :attr:`start` to :attr:`end`.
    """

    start: ft.Number
    """
    The value at which this zone starts.

    Must be greater than or equal to :attr:`flet_charts.GaugeChart.min_value`.
    """

    end: Annotated[ft.Number, V.ge_field("start")]
    """
    The value at which this zone ends.

    Must be less than or equal to :attr:`flet_charts.GaugeChart.max_value`.

    Raises:
        ValueError: If it is not greater than or equal to :attr:`start`.
    """

    color: ft.ColorValue
    """
    The color of this zone.
    """

    stroke_cap: ft.StrokeCap = ft.StrokeCap.BUTT
    """
    The shape of the ends of this zone.
    """


@ft.control("GaugeZonesRing")
class GaugeZonesRing(GaugeRing):
    """
    A ring made of colored zones, such as the red, amber and green bands of a
    speedometer.
    """

    zones: Annotated[list[GaugeZone], V.length_ge(1)]
    """
    The zones drawn on this ring.

    Zones may overlap; a later zone is drawn on top of an earlier one.

    Raises:
        ValueError: If its length is less than `1`.
    """

    zones_space: Annotated[ft.Number, V.ge(0)] = 0
    """
    The gap between adjacent zones, measured along the arc in logical pixels.

    Half of it is taken from each end of every zone. Round
    :attr:`flet_charts.GaugeZone.stroke_cap` ends extend half the ring
    :attr:`~flet_charts.GaugeRing.width` past each end, so the visible gap between
    rounded zones is about `zones_space - width`.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """
