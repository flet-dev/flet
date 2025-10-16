from typing import Optional

import flet as ft
from flet_map.map_layer import MapLayer
from flet_map.types import MapLatitudeLongitude

__all__ = ["CircleLayer", "CircleMarker"]


@ft.control("CircleMarker")
class CircleMarker(ft.Control):
    """
    A circular marker displayed on the Map at the specified
    location through the [`CircleLayer`][(p).].
    """

    radius: ft.Number
    """The radius of the circle"""

    coordinates: MapLatitudeLongitude
    """The center coordinates of the circle"""

    color: Optional[ft.ColorValue] = None
    """The color of the circle area."""

    border_color: Optional[ft.ColorValue] = None
    """
    The color of the circle border line.

    Tip:
        [`border_stroke_width`][(c).] must be greater than
        `0.0` in order for this color to be visible.
    """

    border_stroke_width: ft.Number = 0.0
    """
    The stroke width for the circle border.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    use_radius_in_meter: bool = False
    """
    Whether the [`radius`][(c).] should use the unit meters.
    """

    def before_update(self):
        super().before_update()
        if self.border_stroke_width < 0:
            raise ValueError(
                "border_stroke_width must be greater than or equal to 0, "
                f"got {self.border_stroke_width}"
            )


@ft.control("CircleLayer")
class CircleLayer(MapLayer):
    """
    A layer to display [`CircleMarker`][(p).]s.
    """

    circles: list[CircleMarker]
    """A list of [`CircleMarker`][(p).]s to display."""
