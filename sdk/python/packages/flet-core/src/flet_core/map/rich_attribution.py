from enum import Enum
from typing import Any, Optional, List

from flet_core.border_radius import BorderRadius
from flet_core.control import OptionalNumber
from flet_core.map.map_layer import MapLayer
from flet_core.map.text_source_attribution import TextSourceAttribution
from flet_core.ref import Ref


class AttributionAlignment(Enum):
    BOTTOM_LEFT = "bottomLeft"
    BOTTOM_RIGHT = "bottomRight"


class RichAttribution(MapLayer):
    """
    An animated and interactive attribution layer that supports both logos/images and text
    (displayed in a popup controlled by an icon button adjacent to the logos).

    -----

    Online docs: https://flet.dev/docs/controls/maprichattribution
    """

    def __init__(
        self,
        attributions: List[TextSourceAttribution],
        alignment: Optional[AttributionAlignment] = None,
        popup_bgcolor: Optional[str] = None,
        popup_border_radius: Optional[BorderRadius] = None,
        popup_initial_display_duration: Optional[int] = None,
        permanent_height: OptionalNumber = None,
        show_flutter_map_attribution: Optional[bool] = None,
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

        self.attributions = attributions
        self.alignment = alignment
        self.popup_bgcolor = popup_bgcolor
        self.permanent_height = permanent_height
        self.show_flutter_map_attribution = show_flutter_map_attribution
        self.popup_border_radius = popup_border_radius
        self.popup_initial_display_duration = popup_initial_display_duration

    def _get_control_name(self):
        return "map_rich_attribution"

    def _get_children(self):
        return self.attributions

    def before_update(self):
        super().before_update()
        self._set_attr_json("popupBorderRadius", self.__popup_border_radius)

    # permanent_height
    @property
    def permanent_height(self) -> OptionalNumber:
        return self._get_attr("permanentHeight", data_type="float", def_value=24.0)

    @permanent_height.setter
    def permanent_height(self, value: OptionalNumber):
        assert value is None or value >= 0, "permanent_height cannot be negative"
        self._set_attr("permanentHeight", value)

    # popup_initial_display_duration
    @property
    def popup_initial_display_duration(self) -> Optional[int]:
        return self._get_attr(
            "popupInitialDisplayDuration", data_type="int", def_value=0
        )

    @popup_initial_display_duration.setter
    def popup_initial_display_duration(self, value: Optional[int]):
        assert (
            value is None or value >= 0
        ), "popup_initial_display_duration cannot be negative"
        self._set_attr("popupInitialDisplayDuration", value)

    # popup_border_radius
    @property
    def popup_border_radius(self) -> Optional[BorderRadius]:
        return self.__popup_border_radius

    @popup_border_radius.setter
    def popup_border_radius(self, value: Optional[BorderRadius]):
        self.__popup_border_radius = value

    # alignment
    @property
    def alignment(self) -> Optional[AttributionAlignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[AttributionAlignment]):
        self.__alignment = value
        self._set_enum_attr("alignment", value, AttributionAlignment)

    # show_flutter_map_attribution
    @property
    def show_flutter_map_attribution(self) -> Optional[bool]:
        return self._get_attr(
            "showFlutterMapAttribution", data_type="bool", def_value=True
        )

    @show_flutter_map_attribution.setter
    def show_flutter_map_attribution(self, value: Optional[bool]):
        self._set_attr("showFlutterMapAttribution", value)

    # popup_bgcolor
    @property
    def popup_bgcolor(self) -> Optional[str]:
        return self._get_attr("popupBgcolor")

    @popup_bgcolor.setter
    def popup_bgcolor(self, value: Optional[str]):
        self._set_attr("popupBgcolor", value)

    # attributions
    @property
    def attributions(self) -> List[TextSourceAttribution]:
        return self.__attributions

    @attributions.setter
    def attributions(self, value: List[TextSourceAttribution]):
        self.__attributions = value
