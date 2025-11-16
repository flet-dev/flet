from dataclasses import field
from typing import Optional

import flet as ft
from flet_map.map_layer import MapLayer
from flet_map.types import (
    FadeInTileDisplay,
    MapLatitudeLongitudeBounds,
    TileDisplay,
    TileLayerEvictErrorTileStrategy,
)

__all__ = ["TileLayer"]


@ft.control("TileLayer")
class TileLayer(MapLayer):
    """
    Displays square raster images in a continuous grid,
    sourced from the provided [`url_template`][(c).] and [`fallback_url`][(c).].

    Typically the first layer to be added to a [`Map`][(p).],
    as it provides the tiles on which
    other layers are displayed.
    """

    url_template: str
    """
    The URL template is a string that contains placeholders,
    which, when filled in, create a URL/URI to a specific tile.

    Examples: https://wiki.openstreetmap.org/wiki/Raster_tile_providers
    """

    fallback_url: Optional[str] = None
    """
    Fallback URL template, used if an error occurs when fetching tiles from
    the [`url_template`][(c).].

    Note that specifying this (non-none) will result in tiles not being cached
    in memory. This is to avoid issues where the [`url_template`][(c).] is flaky, to
    prevent different tilesets being displayed at the same time.

    It is expected that this follows the same retina support behaviour
    as [`url_template`][(c).].
    """

    subdomains: list[str] = field(default_factory=lambda: ["a", "b", "c"])
    """
    List of subdomains used in the URL template.

    For example, if [`subdomains`][(c).] is set to `["a", "b", "c"]` and the
    `url_template` is `"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"`,
    the resulting tile URLs will be:

    - `"https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"`
    - `"https://b.tile.openstreetmap.org/{z}/{x}/{y}.png"`
    - `"https://c.tile.openstreetmap.org/{z}/{x}/{y}.png"`
    """

    tile_bounds: Optional[MapLatitudeLongitudeBounds] = None
    """
    Defines the bounds of the map.
    Only tiles that fall within these bounds will be loaded.
    """

    tile_size: int = 256
    """
    The size in pixels of each tile image.
    Should be a positive power of 2.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    min_native_zoom: int = 0
    """
    Minimum zoom level supported by the tile source.

    Tiles from below this zoom level will not be displayed, instead tiles at
    this zoom level will be displayed and scaled.

    This should usually be 0 (as default), as most tile sources will support
    zoom levels onwards from this.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    max_native_zoom: int = 19
    """
    Maximum zoom number supported by the tile source has available.

    Tiles from above this zoom level will not be displayed, instead tiles at
    this zoom level will be displayed and scaled.

    Most tile servers support up to zoom level `19`, which is the default.
    Otherwise, this should be specified.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    zoom_reverse: bool = False
    """
    Whether the zoom number used in tile URLs will be reversed
    (`max_zoom - zoom` instead of `zoom`).
    """

    zoom_offset: ft.Number = 0.0
    """
    The zoom number used in tile URLs will be offset with this value.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    keep_buffer: int = 2
    """
    When panning the map, keep this many rows and columns of
    tiles before unloading them.
    """

    pan_buffer: int = 1
    """
    When loading tiles only visible tiles are loaded by default. This option
    increases the loaded tiles by the given number on both axis which can help
    prevent the user from seeing loading tiles whilst panning. Setting the
    pan buffer too high can impact performance, typically this is set to `0` or `1`.
    """

    enable_tms: bool = False
    """
    Whether to inverse Y-axis numbering for tiles.
    Turn this on for [TMS](https://en.wikipedia.org/wiki/Tile_Map_Service) services.
    """

    enable_retina_mode: bool = False
    """
    Whether to enable retina mode.
    Retina mode improves the resolution of map tiles, particularly on
    high density displays.
    """

    additional_options: dict[str, str] = field(default_factory=dict)
    """
    Static information that should replace placeholders in the [`url_template`][(c).].
    Applying API keys, for example, is a good usecase of this parameter.

    Example:
        ```python
        TileLayer(
            url_template="https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}{r}.png?access_token={accessToken}",
            additional_options={
                'accessToken': '<ACCESS_TOKEN_HERE>',
                'id': 'mapbox.streets',
            },
        )
        ```
    """

    max_zoom: ft.Number = float("inf")
    """
    The maximum zoom level up to which this layer will be displayed (inclusive).
    The main usage for this property is to display a different `TileLayer`
    when zoomed far in.

    Prefer [`max_native_zoom`][(c).] for setting the maximum zoom level supported by the
    tile source.

    Typically set to infinity so that there are tiles always displayed.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    min_zoom: ft.Number = 0.0
    """
    The minimum zoom level at which this layer is displayed (inclusive).

    Typically `0.0`.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    error_image_src: Optional[str] = None
    """
    The source of the tile image to show in place of the tile that failed to load.

    See [`on_image_error`][(c).] property for details on the error.
    """

    evict_error_tile_strategy: Optional[TileLayerEvictErrorTileStrategy] = (
        TileLayerEvictErrorTileStrategy.NONE
    )
    """
    If a tile was loaded with error,
    the tile provider will be asked to evict the image based on this strategy.
    """

    display_mode: TileDisplay = field(default_factory=lambda: FadeInTileDisplay())
    """

    Defines how tiles are displayed on the map.
    """

    user_agent_package_name: str = "unknown"
    """
    The package name of the user agent.
    """

    on_image_error: Optional[ft.ControlEventHandler["TileLayer"]] = None
    """
    Fires if an error occurs when fetching the tiles.

    Event handler argument [`data`][flet.Event.] property contains
    information about the error.
    """

    def before_update(self):
        super().before_update()
        if self.tile_size < 0:
            raise ValueError(
                f"tile_size must be greater than or equal to 0, got {self.tile_size}"
            )
        if self.min_native_zoom < 0:
            raise ValueError(
                "min_native_zoom must be greater than or equal to 0, "
                f"got {self.min_native_zoom}"
            )
        if self.max_native_zoom < 0:
            raise ValueError(
                "max_native_zoom must be greater than or equal to 0, "
                f"got {self.max_native_zoom}"
            )
        if self.zoom_offset < 0:
            raise ValueError(
                f"zoom_offset must be greater than or equal to 0, "
                f"got {self.zoom_offset}"
            )
        if self.max_zoom < 0:
            raise ValueError(
                f"max_zoom must be greater than or equal to 0, got {self.max_zoom}"
            )
        if self.min_zoom < 0:
            raise ValueError(
                f"min_zoom must be greater than or equal to 0, got {self.min_zoom}"
            )
