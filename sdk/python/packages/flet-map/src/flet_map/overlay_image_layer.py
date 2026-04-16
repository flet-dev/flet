from typing import Annotated, Union

import flet as ft
from flet.utils.validation import V
from flet_map.map_layer import MapLayer
from flet_map.types import MapLatitudeLongitude, MapLatitudeLongitudeBounds

__all__ = [
    "BaseOverlayImage",
    "OverlayImage",
    "OverlayImageLayer",
    "RotatedOverlayImage",
]


@ft.control("BaseOverlayImage", kw_only=True)
class BaseOverlayImage(ft.BaseControl):
    """
    Abstract class for image overlays displayed through
    :class:`~flet_map.OverlayImageLayer`.

    The following overlay image types are available:

    - :class:`~flet_map.OverlayImage`
    - :class:`~flet_map.RotatedOverlayImage`
    """

    src: Union[str, bytes]
    """
    The image source.

    It can be one of the following:
    - A URL or local [asset file](https://flet.dev/docs/cookbook/assets) path;
    - A base64 string;
    - Raw bytes.
    """

    opacity: Annotated[
        ft.Number,
        V.between(0.0, 1.0),
    ] = 1.0
    """
    The opacity in which the image should get rendered on the map.

    Raises:
        ValueError: If it is not between `0.0` and `1.0`, inclusive.
    """

    gapless_playback: bool = False
    """
    Whether to continue showing the old image (`True`), or briefly show nothing
    (`False`), when the image provider changes.
    """

    filter_quality: ft.FilterQuality = ft.FilterQuality.MEDIUM
    """
    The rendering quality of the image.
    """


@ft.control("OverlayImage", kw_only=True)
class OverlayImage(BaseOverlayImage):
    """
    An unrotated image overlay that spans between a given bounding box.
    """

    bounds: MapLatitudeLongitudeBounds
    """
    The latitude and longitude bounds where this image will be displayed.
    """


@ft.control("RotatedOverlayImage", kw_only=True)
class RotatedOverlayImage(BaseOverlayImage):
    """
    An image overlay transformed across three corner points.

    The top-right corner is derived from :attr:`top_left_corner`,
    :attr:`bottom_left_corner`, and :attr:`bottom_right_corner`.
    """

    top_left_corner: MapLatitudeLongitude
    """
    The coordinates of the top-left corner of the image.
    """

    bottom_left_corner: MapLatitudeLongitude
    """
    The coordinates of the bottom-left corner of the image.
    """

    bottom_right_corner: MapLatitudeLongitude
    """
    The coordinates of the bottom-right corner of the image.
    """


@ft.control("OverlayImageLayer", kw_only=True)
class OverlayImageLayer(MapLayer):
    """
    A layer to display image overlays.

    Tip:
        Place this layer after every non-translucent layer that should appear
        below it. Layers rendered after this one may cover its overlay images.
    """

    overlay_images: list[BaseOverlayImage]
    """
    A list of image overlays to display.
    """
