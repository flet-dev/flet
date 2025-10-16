from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import flet as ft
from flet_charts.radar_data_set import RadarDataSet
from flet_charts.types import ChartEventType

__all__ = ["RadarChart", "RadarChartEvent", "RadarChartTitle", "RadarShape"]


class RadarShape(Enum):
    """Shape of the radar grid and data polygons."""

    CIRCLE = "circle"
    """Draws radial circles for the grid and data outlines."""

    POLYGON = "polygon"
    """Draws straight-edged polygons for the grid and data outlines."""


@ft.control("RadarChartTitle")
class RadarChartTitle(ft.BaseControl):
    """
    Custom title configuration displayed around a [`RadarChart`][(p).].
    """

    text: str = ""
    """
    The text displayed for the title.
    """

    angle: ft.Number = 0
    """
    Rotation angle (in degrees) applied to the title.
    """

    position_percentage_offset: Optional[ft.Number] = None
    """
    Defines the relative distance of this title from the chart center.

    - `0` draws this title near the inside edge of each section.
    - `1` draws this title near the outside edge of each section.

    Must be between `0` and `1` (inclusive), if set.

    Note:
        If set, it takes precedence over the parent
        [`RadarChart.title_position_percentage_offset`][(p).] value.
    """

    text_spans: Optional[list[ft.TextSpan]] = None
    """
    Inline spans appended to the title.
    """


@dataclass
class RadarChartEvent(ft.Event["RadarChart"]):
    """
    Event raised for interactions with a [`RadarChart`][(p).].
    """

    type: ChartEventType
    """
    The touch or pointer event that occurred.
    """

    data_set_index: Optional[int] = None
    """
    The index of the touched data set, if any.
    """

    entry_index: Optional[int] = None
    """
    The index of the touched radar entry, if any.
    """

    entry_value: Optional[ft.Number] = None
    """
    The value of the touched radar entry, if any.
    """


@ft.control("RadarChart")
class RadarChart(ft.LayoutControl):
    """
    A radar chart made of multiple datasets.
    """

    data_sets: list[RadarDataSet] = field(default_factory=list)
    """
    A list of [`RadarDataSet`][(p).] controls rendered on the chart.
    """

    titles: list[RadarChartTitle] = field(default_factory=list)
    """
    The titles shown around this chart, matching the number of entries per set.
    """

    title_text_style: Optional[ft.TextStyle] = None
    """
    The text style applied to titles around this chart.
    """

    title_position_percentage_offset: ft.Number = 0.2
    """
    Defines the relative distance of titles from the chart center.

    - `0` draws titles near the inside edge of each section.
    - `1` draws titles near the outside edge of each section.

    Must be between `0` and `1` (inclusive).

    Raises:
        ValueError: If set to a value less than `0` or greater than `1`.
    """

    radar_bgcolor: ft.ColorValue = ft.Colors.TRANSPARENT
    """
    The background color of the radar area.
    """

    radar_border_side: ft.BorderSide = field(
        default_factory=lambda: ft.BorderSide(width=2.0)
    )
    """
    The outline drawn around the radar area.
    """

    radar_shape: RadarShape = RadarShape.POLYGON
    """
    The shape of the radar area.
    """

    border: Optional[ft.Border] = None
    """
    The border drawn around this chart.
    """

    center_min_value: bool = False
    """
    Whether minimum entry values should be positioned at the center of this chart.
    """

    tick_count: ft.Number = 1
    """
    Number of tick rings drawn from the centre to the edge.

    Must be greater than or equal to `1`.

    Raises:
        ValueError: If set to a value less than `1`.
    """

    ticks_text_style: Optional[ft.TextStyle] = None
    """
    The text style used to draw tick labels.
    """

    tick_border_side: ft.BorderSide = field(
        default_factory=lambda: ft.BorderSide(width=2.0)
    )
    """
    The style of the tick rings.
    """

    grid_border_side: ft.BorderSide = field(
        default_factory=lambda: ft.BorderSide(width=2.0)
    )
    """
    The style of the radar grid lines.
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

    touch_spot_threshold: ft.Number = 10
    """
    The radius (in logical pixels) used to detect nearby entries for touches.
    """

    on_event: Optional[ft.EventHandler[RadarChartEvent]] = None
    """
    Called when the chart is interacted with.
    """

    def init(self):
        super().init()
        entries_lengths = {len(ds.entries) for ds in self.data_sets}
        if len(entries_lengths) > 1:
            raise ValueError(
                "All data sets in the data_sets list must have equal number of entries"
            )
        if not (0 <= self.title_position_percentage_offset <= 1):
            raise ValueError("title_position_percentage_offset must be between 0 and 1")
        if self.tick_count is not None and self.tick_count < 1:
            raise ValueError("tick_count must be greater than or equal to 1")
