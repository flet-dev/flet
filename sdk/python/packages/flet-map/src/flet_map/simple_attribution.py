from dataclasses import field
from typing import Optional, Union

import flet as ft
from flet_map.map_layer import MapLayer

__all__ = ["SimpleAttribution"]


@ft.control("SimpleAttribution")
class SimpleAttribution(MapLayer):
    """
    A simple attribution layer displayed on the Map.
    """

    text: Union[str, ft.Text]
    """
    The attribution message to be displayed.
    """

    alignment: ft.Alignment = field(default_factory=lambda: ft.Alignment.BOTTOM_RIGHT)
    """
    The alignment of this attribution on the map.
    """

    bgcolor: ft.ColorValue = ft.Colors.SURFACE
    """
    The color of the box containing the [`text`][(c).].
    """

    on_click: Optional[ft.ControlEventHandler["SimpleAttribution"]] = None
    """Fired when this attribution is clicked/pressed."""
