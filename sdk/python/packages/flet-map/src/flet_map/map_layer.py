import flet as ft

__all__ = ["MapLayer"]


@ft.control("MapLayer")
class MapLayer(ft.Control):
    """
    Abstract class for all map layers.

    The following layers are available:

    - [`CircleLayer`][(p).]
    - [`MarkerLayer`][(p).]
    - [`PolygonLayer`][(p).]
    - [`PolylineLayer`][(p).]
    - [`RichAttribution`][(p).]
    - [`SimpleAttribution`][(p).]
    - [`TileLayer`][(p).]
    """
