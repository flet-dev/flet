from typing import Any, Optional

from flet_core.alignment import Alignment
from flet_core.map.map_layer import MapLayer
from flet_core.ref import Ref


class SimpleAttribution(MapLayer):
    """
    A simple attribution layer displayed on the Map.

    -----

    Online docs: https://flet.dev/docs/controls/mapsimpleattribution
    """

    def __init__(
        self,
        text: str,
        alignment: Optional[Alignment] = None,
        bgcolor: Optional[str] = None,
        on_click=None,
        #
        # MapLayer
        #
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        MapLayer.__init__(
            self,
            ref=ref,
            visible=visible,
            data=data,
        )

        self.text = text
        self.alignment = alignment
        self.bgcolor = bgcolor
        self.on_click = on_click

    def _get_control_name(self):
        return "map_simple_attribution"

    def before_update(self):
        super().before_update()
        self._set_attr_json("alignment", self.__alignment)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # text
    @property
    def text(self) -> str:
        return self._get_attr("text")

    @text.setter
    def text(self, value: str):
        self._set_attr("text", value)

    # on_click
    @property
    def on_change(self):
        return self._get_event_handler("click")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("click", handler)
