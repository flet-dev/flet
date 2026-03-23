import flet as ft

__all__ = ["MapLayer"]


@ft.control("MapLayer")
class MapLayer(ft.Control):
    """
    Abstract class for all map layers.

    The following layers are available:

    - :class:`~flet_map.CircleLayer`
    - :class:`~flet_map.MarkerLayer`
    - :class:`~flet_map.PolygonLayer`
    - :class:`~flet_map.PolylineLayer`
    - :class:`~flet_map.RichAttribution`
    - :class:`~flet_map.SimpleAttribution`
    - :class:`~flet_map.TileLayer`
    """
