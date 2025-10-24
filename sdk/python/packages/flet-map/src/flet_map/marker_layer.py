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
    """

    content: ft.Control
    """
    The content to be displayed at [`coordinates`][(c).].

    Raises:
        ValueError: If it is not [`visible`][(c).].
    """

    coordinates: MapLatitudeLongitude
    """
    The coordinates of the marker.

    This will be the center of the marker,
    if [`alignment`][(c).] is [`Alignment.CENTER`][flet.].
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
    The height of the [`content`][(c).] Control.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    width: ft.Number = 30.0
    """
    The width of the [`content`][(c).] Control.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    alignment: Optional[ft.Alignment] = None
    """
    Alignment of the marker relative to the normal center at [`coordinates`][(c).].

    Defaults to the value of the parent [`MarkerLayer.alignment`][(p).].
    """

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
        if self.height < 0:
            raise ValueError(
                f"height must be greater than or equal to 0, got {self.height}"
            )
        if self.width < 0:
            raise ValueError(
                f"width must be greater than or equal to 0, got {self.width}"
            )


@ft.control("MarkerLayer")
class MarkerLayer(MapLayer):
    """
    A layer to display Markers.
    """

    markers: list[Marker]
    """
    A list of [`Marker`][(p).]s to display.
    """

    alignment: Optional[ft.Alignment] = field(
        default_factory=lambda: ft.Alignment.CENTER
    )
    """
    The alignment of each marker relative to its normal center at
    [`Marker.coordinates`][(p).].
    """

    rotate: bool = False
    """
    Whether to counter-rotate [`markers`][(c).] to the map's rotation,
    to keep a fixed orientation.
    """
