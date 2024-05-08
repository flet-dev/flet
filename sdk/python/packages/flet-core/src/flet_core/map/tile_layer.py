from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class TileLayer(Control):
    """
    The Map's main item.
    It displays square raster images in a continuous grid, sourced from the provided utl_template.

    -----

    Online docs: https://flet.dev/docs/controls/maptilelayer
    """

    def __init__(
        self,
        url_template: str = None,
        fallback_url: Optional[str] = None,
        tile_size: OptionalNumber = None,
        min_native_zoom: Optional[int] = None,
        max_native_zoom: Optional[int] = None,
        zoom_reverse: Optional[bool] = None,
        zoom_offset: OptionalNumber = None,
        keep_buffer: Optional[int] = None,
        pan_buffer: Optional[int] = None,
        enable_tms: Optional[bool] = None,
        keep_alive: Optional[bool] = None,
        max_zoom: OptionalNumber = None,
        min_zoom: OptionalNumber = None,
        error_image_src: Optional[str] = None,
        on_image_error=None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            visible=visible,
            data=data,
        )

        self.url_template = url_template
        self.fallback_url = fallback_url
        self.tile_size = tile_size
        self.min_native_zoom = min_native_zoom
        self.max_native_zoom = max_native_zoom
        self.zoom_reverse = zoom_reverse
        self.zoom_offset = zoom_offset
        self.keep_buffer = keep_buffer
        self.pan_buffer = pan_buffer
        self.enable_tms = enable_tms
        self.keep_alive = keep_alive
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.error_image_src = error_image_src
        self.on_image_error = on_image_error

    def _get_control_name(self):
        return "maptilelayer"

    # url_template
    @property
    def url_template(self) -> str:
        return self._get_attr("urlTemplate")

    @url_template.setter
    def url_template(self, value: str):
        self._set_attr("urlTemplate", value)

    # fallback_url
    @property
    def fallback_url(self) -> Optional[str]:
        return self._get_attr("fallbackUrl")

    @fallback_url.setter
    def fallback_url(self, value: Optional[str]):
        self._set_attr("fallbackUrl", value)

    # tile_size
    @property
    def tile_size(self) -> OptionalNumber:
        return self._get_attr("tileSize", data_type="float", def_value=256.0)

    @tile_size.setter
    def tile_size(self, value: OptionalNumber):
        self._set_attr("tileSize", value)

    # min_native_zoom
    @property
    def min_native_zoom(self) -> Optional[int]:
        return self._get_attr("minNativeZoom", data_type="int", def_value=0)

    @min_native_zoom.setter
    def min_native_zoom(self, value: Optional[int]):
        self._set_attr("minNativeZoom", value)

    # max_native_zoom
    @property
    def max_native_zoom(self) -> Optional[int]:
        return self._get_attr("maxNativeZoom", data_type="int", def_value=19)

    @max_native_zoom.setter
    def max_native_zoom(self, value: Optional[int]):
        self._set_attr("maxNativeZoom", value)

    # zoom_reverse
    @property
    def zoom_reverse(self) -> Optional[bool]:
        return self._get_attr("zoomReverse", data_type="bool", def_value=False)

    @zoom_reverse.setter
    def zoom_reverse(self, value: Optional[bool]):
        self._set_attr("zoomReverse", value)

    # zoom_offset
    @property
    def zoom_offset(self) -> OptionalNumber:
        return self._get_attr("zoomOffset", data_type="float", def_value=0.0)

    @zoom_offset.setter
    def zoom_offset(self, value: OptionalNumber):
        self._set_attr("zoomOffset", value)

    # keep_buffer
    @property
    def keep_buffer(self) -> Optional[int]:
        return self._get_attr("keepBuffer", data_type="int", def_value=2)

    @keep_buffer.setter
    def keep_buffer(self, value: Optional[int]):
        self._set_attr("keepBuffer", value)

    # pan_buffer
    @property
    def pan_buffer(self) -> Optional[int]:
        return self._get_attr("panBuffer", data_type="int", def_value=2)

    @pan_buffer.setter
    def pan_buffer(self, value: Optional[int]):
        self._set_attr("panBuffer", value)

    # enable_tms
    @property
    def enable_tms(self) -> Optional[bool]:
        return self._get_attr("enableTms", data_type="bool", def_value=False)

    @enable_tms.setter
    def enable_tms(self, value: Optional[bool]):
        self._set_attr("enableTms", value)

    # max_zoom
    @property
    def max_zoom(self) -> OptionalNumber:
        return self._get_attr("maxZoom", data_type="float", def_value=float("inf"))

    @max_zoom.setter
    def max_zoom(self, value: OptionalNumber):
        self._set_attr("maxZoom", value)

    # min_zoom
    @property
    def min_zoom(self) -> OptionalNumber:
        return self._get_attr("minZoom", data_type="float", def_value=0.0)

    @min_zoom.setter
    def min_zoom(self, value: OptionalNumber):
        self._set_attr("minZoom", value)

    # error_image_src
    @property
    def error_image_src(self) -> Optional[str]:
        return self._get_attr("errorImageSrc")

    @error_image_src.setter
    def error_image_src(self, value: Optional[str]):
        self._set_attr("errorImageSrc", value)

    # on_image_error
    @property
    def on_image_error(self):
        return self._get_event_handler("imageError")

    @on_image_error.setter
    def on_image_error(self, handler):
        self._add_event_handler("imageError", handler)
