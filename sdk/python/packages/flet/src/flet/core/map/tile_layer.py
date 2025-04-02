from dataclasses import field
from enum import Enum
from typing import Dict, List, Optional

from flet.core.control import control
from flet.core.map.map import MapLatitudeLongitudeBounds
from flet.core.map.map_layer import MapLayer
from flet.core.types import Number, OptionalControlEventCallable


class MapTileLayerEvictErrorTileStrategy(Enum):
    DISPOSE = "dispose"
    NOT_VISIBLE = "notVisible"
    NOT_VISIBLE_RESPECT_MARGIN = "notVisibleRespectMargin"


@control("TileLayer")
class TileLayer(MapLayer):
    """
    The Map's main layer.
    Displays square raster images in a continuous grid, sourced from the provided utl_template.

    -----

    Online docs: https://flet.dev/docs/controls/maptilelayer
    """

    url_template: str
    fallback_url: Optional[str] = None
    subdomains: Optional[List[str]] = None
    tile_bounds: Optional[MapLatitudeLongitudeBounds] = None
    tile_size: Number = field(default=256.0)
    min_native_zoom: int = field(default=0)
    max_native_zoom: int = field(default=19)
    zoom_reverse: bool = field(default=False)
    zoom_offset: int = field(default=0)
    keep_buffer: int = field(default=2)
    pan_buffer: int = field(default=2)
    enable_tms: bool = field(default=False)
    keep_alive: Optional[bool] = None
    enable_retina_mode: Optional[bool] = None
    additional_options: Optional[Dict[str, str]] = None
    max_zoom: Number = field(default=float("inf"))
    min_zoom: Number = field(default=0)
    error_image_src: Optional[str] = None
    evict_error_tile_strategy: Optional[MapTileLayerEvictErrorTileStrategy] = None
    on_image_error: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.url_template, "url_template is required"
        assert self.tile_size > 0, "tile_size must be greater than 0"
        assert (
            self.min_native_zoom >= 0
        ), "min_native_zoom must be greater than or equal to 0"
        assert (
            self.max_native_zoom >= 0
        ), "max_native_zoom must be greater than or equal to 0"
        assert self.zoom_offset >= 0, "zoom_offset must be greater than or equal to 0"
        assert self.min_zoom >= 0, "min_zoom must be greater than or equal to 0"
        assert self.max_zoom >= 0, "max_zoom must be greater than or equal to 0"
