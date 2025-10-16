from typing import Optional

import flet as ft
from flet_map.map_layer import MapLayer
from flet_map.types import MapLatitudeLongitude

__all__ = ["PolygonLayer", "PolygonMarker"]


@ft.control("PolygonMarker")
class PolygonMarker(ft.Control):
    """
    A marker for the [`PolygonLayer`][(p).].
    """

    coordinates: list[MapLatitudeLongitude]
    """
    The points for the outline of this polygon.
    """

    label: Optional[str] = None
    """
    An optional label for this polygon.

    Note:
        Specifying a label will reduce performance, as the internal
        canvas must be drawn to and 'saved' more frequently to ensure the proper
        stacking order is maintained. This can be avoided, potentially at the
        expense of appearance, by setting [`PolygonLayer.draw_labels_last`][(p).].
    """

    label_text_style: Optional[ft.TextStyle] = None
    """
    The text style for the label.
    """

    border_color: ft.ColorValue = ft.Colors.GREEN
    """
    The color of the border outline.
    """

    color: ft.ColorValue = ft.Colors.GREEN
    """
    The color of the polygon.
    """

    border_stroke_width: ft.Number = 0.0
    """
    The width of the border outline.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    disable_holes_border: bool = False
    """
    Whether holes should have borders.
    """

    rotate_label: bool = False
    """
    Whether to rotate the label counter to the camera's rotation,
    to ensure it remains upright.
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


@ft.control("PolygonLayer")
class PolygonLayer(MapLayer):
    """
    A layer to display PolygonMarkers.
    """

    polygons: list[PolygonMarker]
    """
    A list of [`PolygonMarker`][(p).]s to display.
    """

    polygon_culling: bool = True
    """
    Whether to cull polygons and polygon sections that are outside of the viewport.
    """

    polygon_labels: bool = True
    """
    Whether to draw per-polygon labels.
    """

    draw_labels_last: bool = False
    """
    Whether to draw labels last and thus over all the polygons.
    """

    simplification_tolerance: ft.Number = 0.3
    """
    The tolerance value used to simplify polygon outlines before rendering.

    Higher values will result in polygons with fewer points, which can improve
    rendering performance at the cost of reduced geometric accuracy. Lower values
    preserve more detail but may decrease performance, especially with complex polygons.

    Set to 0 to disable simplification.
    """

    use_alternative_rendering: bool = False
    """
    Whether to use an alternative rendering pathway to draw polygons onto the
    underlying `Canvas`, which can be more performant in 'some' circumstances.

    This will not always improve performance, and there are other important
    considerations before enabling it. It is intended for use when prior
    profiling indicates more performance is required after other methods are
    already in use. For example, it may worsen performance when there are a
    huge number of polygons to triangulate - and so this is best used in
    conjunction with simplification, not as a replacement.
    """
