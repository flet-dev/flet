from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class MapTileLayer(Control):
    """
    TBA


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
        tms: Optional[bool] = None,
        initial_rotation: OptionalNumber = None,
        initial_zoom: OptionalNumber = None,
        keep_alive: Optional[bool] = None,
        max_zoom: OptionalNumber = None,
        min_zoom: OptionalNumber = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        opacity: OptionalNumber = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
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
        self.tms = tms
        self.initial_rotation = initial_rotation
        self.initial_zoom = initial_zoom
        self.keep_alive = keep_alive
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom

    def _get_control_name(self):
        return "maptilelayer"

    # height
    @property
    def height(self) -> OptionalNumber:
        return self._get_attr("height", data_type="float")

    @height.setter
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)

    # thickness
    @property
    def thickness(self) -> OptionalNumber:
        return self._get_attr("thickness", data_type="float")

    @thickness.setter
    def thickness(self, value: OptionalNumber):
        self._set_attr("thickness", value)

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # leading_indent
    @property
    def leading_indent(self) -> OptionalNumber:
        return self._get_attr("leadingIndent", data_type="float")

    @leading_indent.setter
    def leading_indent(self, value: OptionalNumber):
        self._set_attr("leadingIndent", value)

    # trailing_indent
    @property
    def trailing_indent(self) -> OptionalNumber:
        return self._get_attr("trailingIndent", data_type="float")

    @trailing_indent.setter
    def trailing_indent(self, value: OptionalNumber):
        self._set_attr("trailingIndent", value)
