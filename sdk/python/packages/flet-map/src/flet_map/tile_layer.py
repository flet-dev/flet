from dataclasses import field
from typing import Optional

import flet as ft
from flet_map.map_layer import MapLayer
from flet_map.types import (
    FadeInTileDisplay,
    MapLatitudeLongitudeBounds,
    TileDisplay,
    TileLayerEvictErrorTileStrategy,
    WMSTileLayerConfiguration,
)

__all__ = ["TileLayer"]


@ft.control("TileLayer")
class TileLayer(MapLayer):
    """
    Displays square raster images in a continuous grid,
    sourced from the provided [`url_template`][(c).] and [`fallback_url`][(c).].

    Typically, the first layer to be added to a [`Map`][(p).],
    as it provides the tiles on which other layers are displayed.

    Info: Caching
        This control supports basic map tile caching (for compatible tile providers).
        On non-web platforms, built-in caching is automatically enabled with a default
        soft limit of 1 GB. On web platforms, caching is typically handled by the browser.

        No guarantees are provided regarding the persistence or reliability of cached
        tiles. Cached data may become unavailable or be cleared at any time.
        For example, do not rely on this caching mechanism in scenarios where missing
        tiles could create risk or unsafe conditions (for example, offline or
        safety-critical mapping applications).

        It aims to:

        - Improve developer experience by:
            - Reducing the costs of using tile servers by reducing
                duplicate tile requests
            - Keep your app lightweight - the built-in cache doesn't ship any binaries
                or databases, just a couple extra libraries you probably already use
        - Improve user experience by:
            - Reducing tile loading durations, as fetching from the cache is very quick
            - Reducing network/Internet usage, which may be limited or metered/expensive (eg. mobile broadband)
        - Improve compliance with tile server requirements, by reducing the strain on them
        - Be extensible, customizable, and integrate with multiple tile providers

        But it comes at the expense of usage of on-device storage capacity.

    Info: Supported sources
        flet-map doesn't provide tiles, so you'll need to bring your own raster tiles.
        There are multiple different supported sources.

        - Slippy Map/CARTO (XYZ): This is the most common format for raster tiles,
            although many satellite tiles will instead use WMS.
            Typically, a URL with placeholders for X, Y, and Z values. Set the
            [`url_template`][(c).] to the template provided by the tile server -
            usually it can be copied directly from an account portal or documentation.
            Additional information, like API/access keys, can be passed in using the
            [`additional_options`][(c).] property. It's also possible to specify a
            [`fallback_url`][(c).] template, used if fetching a tile from the primary
            [`url_template`][(c).] fails.
        - Tile Map Service (TMS): This is also supported. Follow the instructions for
            the XYZ source above, then set the [`enable_tms`][(c).] property to `True`.
            Read more on WMS [here](https://en.wikipedia.org/wiki/Tile_Map_Service).
        - Web Map Services (WMS): This is also supported. Use [`wms_configuration`][(c).]
            to specify the necessary configuration for WMS tile servers.
            Read more on WMS [here](https://www.mngeo.state.mn.us/chouse/wms/index.html).

    Example:
    ```python
    ftm.TileLayer(
        url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        user_agent_package_name="MyTownMaps/1.4 (+https://example.org; contact: maps@example.org)",
    )
    ```
    """  # noqa: E501

    url_template: str
    """
    The URL template is a string that contains placeholders,
    which, when filled in, create a URL/URI to a specific tile.

    Provider Examples: https://wiki.openstreetmap.org/wiki/Raster_tile_providers

    Info: Placeholders
        As well as the standard XYZ placeholders in the template, the following
        placeholders may also be used:

        - `{s}`: see [`subdomains`][(c).] property
        - `{r}`: retina scaling factor (2 or 1)
        - `{d}`: reflects the [`tile_size`][(c).] property

        Additional placeholders can also be added freely to the template,
        and are filled in with the specified values in [`additional_options`][(c).].
        This can be used to easier add switchable styles or access tokens.

    Danger: Compliance with tile server requirements
        It is your own responsibility to comply with any appropriate restrictions and
        requirements set by your chosen tile server/provider. Always read their terms
        of service. Failure to do so may lead to any punishment,
        at the tile server's discretion.

        Production apps should be extremely cautious about using this tile server;
        other projects, libraries, and packages suggesting that OpenStreetMap provides
        free-to-use map tiles are incorrect.

        /// admonition | Case Example: OpenStreetMap (direct)
            type: example
        OpenStreetMap (OSM) is one of the most popular sources for map tiles and
        data. Their data is free for everyone to use (under
        [ODbL](https://opendatacommons.org/licenses/odbl/)), but their public
        [tile server](https://tile.openstreetmap.org) is not free for everyone to
        use. It is without cost (for users), but, "without cost" ≠
        "without restriction" ≠ "open". Due to excessive usage, the OSM Foundation
        (running OSM as a not-for-profit) has implemented some measures to prevent
        abuse and ensure the sustainability of their service.

        For example: on non-web platforms (ex: desktop), they require a proper
        [User-Agent](https://en.wikipedia.org/wiki/User-Agent_header) header
        to be set. See the [`user_agent_package_name`][(c).] property for
        details and recommended best practices. This does not apply to the web
        platform, because you cannot set a User-Agent header different to what is
        provided by the browser.

        Read more on their tile usage policy
        [here](https://operations.osmfoundation.org/policies/tiles/).
        ///
    """

    fallback_url: Optional[str] = None
    """
    Fallback URL template used if fetching tiles from [`url_template`][(c).] fails.

    The template must follow the same format and support the same placeholders
    as [`url_template`][(c).].

    Note:
        When this is specified, tiles will not be cached in memory, to prevent
        inconsistencies when [`url_template`][(c).] is unreliable, avoiding
        situations where tiles from different sources are displayed simultaneously.
        Disabling caching may negatively impact performance and efficiency, hence the
        recommendation to only specify a fallback URL when really necessary.
    """

    subdomains: list[str] = field(default_factory=lambda: ["a", "b", "c"])
    """
    List of subdomains used in the URL template.

    To use subdomains, add the `{s}` placeholder to the URL
    template ([`url_template`][(c).] and [`fallback_url`][(c).])

    Note:
        Subdomains are now usually considered redundant due to the usage of HTTP/2
        & HTTP/3 which don't have the same restrictions. Usage of subdomains will
        also hinder the ability to cache tiles, potentially leading to increased tile
        requests and costs. Hence, if the server supports HTTP/2 or HTTP/3
        ([how to check](https://stackoverflow.com/a/71288871/11846040)),
        avoid using subdomains.

    Example:
        If [`subdomains`][(c).] is set to `["a", "b", "c"]`
        and the [`url_template`][(c).] is
        `"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"`,
        the resulting tile URLs will be:

        - `"https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"`
        - `"https://b.tile.openstreetmap.org/{z}/{x}/{y}.png"`
        - `"https://c.tile.openstreetmap.org/{z}/{x}/{y}.png"`
    """

    user_agent_package_name: str = "unknown"
    """
    The package name of the user agent to use when fetching tiles from the tile server.

    This is used to identify your app to the tile server,
    and is important for compliance with tile server usage policies.

    Tip: OSM best practice recommendations
        OpenStreetMap (OSM) [recommends](https://operations.osmfoundation.org/policies/tiles/) the following:

        - Use a clear, unique [User-Agent](https://en.wikipedia.org/wiki/User-Agent_header)
            string that names your app and optionally includes a contact URL or email.
            - Good Example: `MyTownMaps/1.4 (+https://example.org; contact: maps@example.org)`
            - Bad Example: `com.example.app`
        - For web apps, the browsers will use the browser’s default `User-Agent` header.
        - Do not use a library default User-Agent, and never impersonate
            another app or a browser.
        - If your platform automatically sets an `X-Requested-With` header with an
            app ID, that is acceptable, but a proper `User-Agent` is still recommended.
        - Referer (web only): Browsers are expected to send a valid `Referer` header.
            Native apps usually do not have a referer, this is ok.
    """  # noqa: E501

    tile_bounds: Optional[MapLatitudeLongitudeBounds] = None
    """
    Defines the bounds of the map.
    Only tiles that fall within these bounds will be loaded.
    """

    tile_size: int = 256
    """
    The size in pixels of each tile image.
    Should be a positive power of `2`.

    Note:
        Some tile servers will use 512x512px tiles instead of 256x256px, such as
        Mapbox. Using these larger tiles can help reduce tile requests, and when
        ombined with Retina Mode, it can give the same resolution.

        To use these tiles, set `tile_size` to the actual dimensions of the tiles
        (otherwise they will appear to small), such as `512`. Also set
        [`zoom_offset`][(c).] to the result of `-((d/256) - 1)` - ie. `-1` for
        x512px tiles (otherwise they will appear at the wrong geographical locations).

        The `{d}` placeholder may also be used in the URL template
        ([`url_template`][(c).] and [`fallback_url`][(c).]) to pass through the
        value of `tile_size`.

    Raises:
        ValueError: If it is less than `0.0`.
    """

    min_native_zoom: int = 0
    """
    Minimum zoom level supported by the tile source.

    Tiles from below this zoom level will not be displayed, instead tiles at
    this zoom level will be displayed and scaled.

    This should usually be `0` (as default), as most tile sources will support
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

    You can also set [`max_zoom`][(c).], which is an absolute zoom limit for users.
    It is recommended to set it to a few levels greater than the maximum zoom level
    covered by any of your tile layers.

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
    When loading tiles only visible tiles are loaded by default.

    This option increases the loaded tiles by the given number on both axis which can
    help prevent the user from seeing loading tiles whilst panning. Setting the
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

    wms_configuration: Optional[WMSTileLayerConfiguration] = None
    """
    The configuration for [WMS](https://www.mngeo.state.mn.us/chouse/wms/index.html)
    tile servers.
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
