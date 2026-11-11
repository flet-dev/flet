from enum import Enum
from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V
from flet_charts.types import GaugeTickPosition

__all__ = ["GaugeMarker", "GaugeMarkerAlignment", "GaugeMarkerLabelSide"]


class GaugeMarkerAlignment(Enum):
    """
    Where the line of a :class:`~flet_charts.GaugeMarker` sits relative to the
    point it marks on the arc.
    """

    CENTERED = "centered"
    """
    The line is centered on the marked point, crossing it.
    """

    OUTWARD = "outward"
    """
    The line starts at the marked point and extends in the marker's outward
    direction, like a tick.

    The outward direction points away from the center of the gauge for markers at
    :attr:`flet_charts.GaugeTickPosition.OUTER` and
    :attr:`flet_charts.GaugeTickPosition.CENTER`, and toward the center for
    markers at :attr:`flet_charts.GaugeTickPosition.INNER`.
    """


class GaugeMarkerLabelSide(Enum):
    """
    Which side of its line the label of a :class:`~flet_charts.GaugeMarker` sits on.

    Sides follow the marker's outward direction, which points away from the center
    of the gauge for markers at :attr:`flet_charts.GaugeTickPosition.OUTER` and
    :attr:`flet_charts.GaugeTickPosition.CENTER`, and toward the center for markers
    at :attr:`flet_charts.GaugeTickPosition.INNER`.
    """

    OUTWARD = "outward"
    """
    The label sits beyond the end of the line, in the marker's outward direction.
    """

    INWARD = "inward"
    """
    The label sits before the start of the line, opposite the marker's outward
    direction.
    """


@ft.value(kw_only=True)
class GaugeMarker:
    """
    A line, with an optional label, that marks a single value on the arc of a
    :class:`~flet_charts.GaugeChart`, such as a threshold or a target.

    Markers are positioned like ticks, but each one sits at its own :attr:`value`
    instead of being spaced evenly. They are drawn over the ticks and under the
    pointers.
    """

    value: ft.Number
    """
    The value on the gauge's scale this marker sits at.

    A value outside :attr:`flet_charts.GaugeChart.min_value` and
    :attr:`flet_charts.GaugeChart.max_value` places the marker past the ends of the
    arc.
    """

    position: GaugeTickPosition = GaugeTickPosition.OUTER
    """
    Where this marker sits relative to the rings.
    """

    offset: ft.Number = 0
    """
    The distance, in logical pixels, by which this marker is moved from its
    :attr:`position`.

    It follows the same rules as :attr:`flet_charts.GaugeTicks.offset`.
    """

    length: Annotated[ft.Number, V.gt(0)] = 10.0
    """
    The length of the line, in logical pixels.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    thickness: Annotated[ft.Number, V.gt(0)] = 2.0
    """
    The thickness of the line, in logical pixels.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the line.

    Defaults to :attr:`flet.ColorScheme.on_surface`.
    """

    stroke_cap: ft.StrokeCap = ft.StrokeCap.ROUND
    """
    The shape of the ends of the line.
    """

    alignment: GaugeMarkerAlignment = GaugeMarkerAlignment.CENTERED
    """
    Where the line sits relative to the point it marks on the arc.
    """

    label: Optional[str] = None
    """
    The text drawn next to the line.

    On the left half of the gauge, the label is turned by 180 degrees so that it
    stays upright.

    Note:
        Only the line is taken into account when the rings shrink to leave room
        for markers at :attr:`flet_charts.GaugeTickPosition.OUTER`. To keep an
        outward label from being clipped, increase :attr:`offset`.
    """

    label_style: Optional[ft.TextStyle] = None
    """
    The text style of the :attr:`label`.

    Defaults to 12-pixel text in the marker's :attr:`color`.
    """

    label_offset: Annotated[ft.Number, V.ge(0)] = 6.0
    """
    The distance, in logical pixels, between the end of the line and the
    :attr:`label`.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    label_side: GaugeMarkerLabelSide = GaugeMarkerLabelSide.OUTWARD
    """
    Which side of the line the :attr:`label` sits on.
    """
