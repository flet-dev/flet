from dataclasses import field
from typing import Optional

import flet as ft
from flet_map.map_layer import MapLayer
from flet_map.types import MapLatitudeLongitude, SolidStrokePattern, StrokePattern

__all__ = ["PolylineLayer", "PolylineMarker"]


@ft.control("PolylineMarker")
class PolylineMarker(ft.Control):
    """
    A marker for the [`PolylineLayer`][(p).].
    """

    coordinates: list[MapLatitudeLongitude]
    """
    The list of coordinates for the polyline.
    """

    colors_stop: Optional[list[ft.Number]] = None
    """
    The stops for the [`gradient_colors`][(c).].
    """

    gradient_colors: Optional[list[ft.ColorValue]] = None
    """
    The List of colors in case a gradient should get used.
    """

    border_color: ft.ColorValue = ft.Colors.YELLOW
    """
    The border's color.
    """

    color: ft.ColorValue = ft.Colors.YELLOW
    """
    The color of the line stroke.
    """

    stroke_width: ft.Number = 1.0
    """
    The width of the stroke.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    border_stroke_width: ft.Number = 0.0
    """
    The width of the stroke with of the line border.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    use_stroke_width_in_meter: bool = False
    """
    Whether the stroke's width should have meters as unit.
    """

    stroke_pattern: StrokePattern = field(default_factory=lambda: SolidStrokePattern())
    """
    Determines whether the line should be solid, dotted, or dashed, and the
    exact characteristics of each.
    """

    stroke_cap: ft.StrokeCap = ft.StrokeCap.ROUND
    """
    Style to use for line endings.
    """

    stroke_join: ft.StrokeJoin = ft.StrokeJoin.ROUND
    """
    Style to use for line segment joins.
    """

    def before_update(self):
        super().before_update()
        if self.border_stroke_width < 0:
            raise ValueError(
                "border_stroke_width must be greater than or equal to 0, "
                f"got {self.border_stroke_width}"
            )
        if self.stroke_width < 0:
            raise ValueError(
                f"stroke_width must be greater than or equal to 0, "
                f"got {self.stroke_width}"
            )


@ft.control("PolylineLayer")
class PolylineLayer(MapLayer):
    """
    A layer to display [`PolylineMarker`][(p).]s.
    """

    polylines: list[PolylineMarker]
    """
    List of [`PolylineMarker`][(p).]s to be drawn.
    """

    culling_margin: ft.Number = 10.0
    """
    Acceptable extent outside of viewport before culling polyline segments.
    """

    min_hittable_radius: ft.Number = 10.0
    """
    The minimum radius of the hittable area around each polyline in logical pixels.

    The entire visible area is always hittable, but if the visible area is
    smaller than this, then this will be the hittable area.
    """

    simplification_tolerance: ft.Number = 0.3
    """
    The tolerance (in map units) used to simplify polylines for rendering.

    Higher values result in more aggressive simplification,
    which can improve performance but may reduce the accuracy of
    the displayed polyline.
    """
