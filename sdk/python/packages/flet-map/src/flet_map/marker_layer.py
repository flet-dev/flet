from dataclasses import field
from typing import Optional

import flet as ft
from flet_map.map_layer import MapLayer
from flet_map.types import MapLatitudeLongitude

__all__ = ["Marker", "MarkerLayer"]


@ft.control("Marker")
class Marker(ft.Control):
    """
    A marker displayed on the Map at the specified location
    through the [`MarkerLayer`][(p).].

    Raises:
        AssertionError: If the [`content`][(c).] is not visible, or
            if [`height`][(c).] or [`width`][(c).] are negative.
    """

    content: ft.Control
    """
    The content to be displayed at [`coordinates`][..].

    Note:
        Must be provided and visible.
    """

    coordinates: MapLatitudeLongitude
    """
    The coordinates of the marker.

    This will be the center of the marker,
    if [`alignment`][..] is [`Alignment.CENTER`][flet.Alignment.CENTER].
    """

    rotate: Optional[bool] = None
    """
    Whether to counter rotate this marker to the map's rotation,
    to keep a fixed orientation.
    So, when `True`, this marker will always appear upright and
    vertical from the user's perspective.

    If `None`, defaults to the value of the parent [`MarkerLayer.rotate`][(p).].

    Note:
        This is not used to apply a custom rotation in degrees to this marker.

    """

    height: ft.Number = 30.0
    """
    The height of the [`content`][..] Control.

    Note:
        Must be non-negative.
    """

    width: ft.Number = 30.0
    """
    The width of the [`content`][..] Control.

    Note:
        Must be non-negative.
    """

    alignment: Optional[ft.Alignment] = None
    """
    Alignment of the marker relative to the normal center at [`coordinates`][..].

    Defaults to the value of the parent [`MarkerLayer.alignment`][(p).].
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
        assert self.height >= 0, (
            f"height must be greater than or equal to 0, got {self.height}"
        )
        assert self.width >= 0, (
            f"width must be greater than or equal to 0, got {self.width}"
        )


@ft.control("MarkerLayer")
class MarkerLayer(MapLayer):
    """
    A layer to display Markers.
    """

    markers: list[Marker]
    """
    A list of [`Marker`][(m).]s to display.
    """

    alignment: Optional[ft.Alignment] = field(
        default_factory=lambda: ft.Alignment.CENTER
    )
    """
    The alignment of each marker relative to its normal center at
    [`Marker.coordinates`][(m).].
    """

    rotate: bool = False
    """
    Whether to counter-rotate `markers` to the map's rotation,
    to keep a fixed orientation.
    """
