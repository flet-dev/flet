from dataclasses import field
from typing import Optional

import flet as ft
from flet_map.map_layer import MapLayer
from flet_map.source_attribution import SourceAttribution
from flet_map.types import AttributionAlignment

__all__ = ["RichAttribution"]


@ft.control("RichAttribution")
class RichAttribution(MapLayer):
    """
    An animated and interactive attribution layer that supports both images and text
    (displayed in a popup controlled by an icon button adjacent to the images).
    """

    attributions: list[SourceAttribution]
    """
    List of attributions to display.

    [`TextSourceAttribution`][(p).]s are shown in a popup box,
    unlike [`ImageSourceAttribution`][(p).], which are visible permanently.
    """

    alignment: Optional[AttributionAlignment] = None
    """
    The position in which to anchor this attribution control.
    """

    popup_bgcolor: Optional[ft.ColorValue] = ft.Colors.SURFACE
    """
    The color to use as the popup box's background color.
    """

    popup_border_radius: Optional[ft.BorderRadiusValue] = None
    """
    The radius of the edges of the popup box.
    """

    popup_initial_display_duration: ft.DurationValue = field(
        default_factory=lambda: ft.Duration()
    )
    """
    The popup box will be open by default and be hidden this
    long after the map is initialised.

    This is useful with certain sources/tile servers that make immediate
    attribution mandatory and are not attributed with a permanently
    visible [`ImageSourceAttribution`][(p).].
    """

    permanent_height: ft.Number = 24.0
    """
    The height of the permanent row in which is found the popup menu toggle button.
    Also determines spacing between the items within the row.
    """

    show_flutter_map_attribution: bool = True
    """
    Whether to add an additional attribution logo and text
    for [`flutter-map`](https://docs.fleaflet.dev/),
    on which 'flet-map' package is based for map-renderings.
    """
