from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V

__all__ = ["GaugeCirclePointer", "GaugeNeedlePointer", "GaugePointer"]


@ft.control(kw_only=True)
class GaugePointer(ft.BaseControl):
    """
    Base class for the pointers of a :class:`~flet_charts.GaugeChart`.

    Pointers are drawn on top of the rings, ticks and markers. Each one points at
    its own :attr:`value`; to move a pointer together with a ring, give both the
    same value.

    See usable subclasses:

    * :class:`~flet_charts.GaugeNeedlePointer`
    * :class:`~flet_charts.GaugeCirclePointer`
    """

    value: ft.Number
    """
    The value on the gauge's scale this pointer points at.

    A value outside :attr:`flet_charts.GaugeChart.min_value` and
    :attr:`flet_charts.GaugeChart.max_value` points past the ends of the arc.
    """


@ft.control("GaugeNeedlePointer")
class GaugeNeedlePointer(GaugePointer):
    """
    A needle that starts at the center of the gauge and narrows to a tip.
    """

    length: Annotated[ft.Number, V.gt(0)] = 60.0
    """
    The distance from the center of the gauge to the tip of the needle, in logical
    pixels.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    width: Annotated[ft.Number, V.gt(0)] = 8.0
    """
    The width of the needle at the center of the gauge, in logical pixels.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    tail_length: Annotated[ft.Number, V.ge(0)] = 0.0
    """
    The length of the tail extending behind the center of the gauge, opposite the
    tip, in logical pixels.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    color: Optional[ft.ColorValue] = None
    """
    The fill color of the needle.

    Defaults to :attr:`flet.ColorScheme.on_surface`.
    """


@ft.control("GaugeCirclePointer")
class GaugeCirclePointer(GaugePointer):
    """
    A filled circle placed at :attr:`anchor_radius` from the center of the gauge,
    with an optional outline.

    With the default :attr:`anchor_radius` of `0`, it sits at the center of the
    gauge, where it can be used as a cap over the pivot of a
    :class:`~flet_charts.GaugeNeedlePointer` listed before it.
    """

    radius: Annotated[ft.Number, V.gt(0)] = 6.0
    """
    The radius of the circle, in logical pixels.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    anchor_radius: Annotated[ft.Number, V.ge(0)] = 0.0
    """
    The distance from the center of the gauge to the center of the circle, in
    logical pixels.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    color: Optional[ft.ColorValue] = None
    """
    The fill color of the circle.

    Defaults to :attr:`flet.ColorScheme.on_surface`.
    """

    stroke_width: Annotated[ft.Number, V.ge(0)] = 0.0
    """
    The width of the outline drawn around the circle.

    If `0`, no outline is drawn.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    stroke_color: Optional[ft.ColorValue] = None
    """
    The color of the outline drawn around the circle.

    Defaults to :attr:`flet.ColorScheme.on_surface`.
    """
