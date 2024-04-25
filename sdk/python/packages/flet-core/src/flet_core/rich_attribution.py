from enum import Enum
from typing import Any, Optional, List

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_source_attribution import TextSourceAttribution


class RichAttributionAlignment(Enum):
    BOTTOM_LEFT = "bottomLeft"
    BOTTOM_RIGHT = "bottomRight"


class RichAttribution(Control):
    """
    TBA

    -----

    Online docs: https://flet.dev/docs/controls/richattribution
    """

    def __init__(
        self,
        attributions: List[TextSourceAttribution] = None,
        alignment: Optional[RichAttributionAlignment] = None,
        popup_bgcolor: Optional[str] = None,
        permanent_height: OptionalNumber = None,
        show_flutter_map_attribution: Optional[bool] = None,
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

        self.attributions = attributions
        self.alignment = alignment
        self.popup_bgcolor = popup_bgcolor
        self.permanent_height = permanent_height
        self.show_flutter_map_attribution = show_flutter_map_attribution

    def _get_control_name(self):
        return "richattribution"

    def _get_children(self):
        return self.attributions

    # permanent_height
    @property
    def permanent_height(self) -> OptionalNumber:
        return self._get_attr("permanentHeight", data_type="float")

    @permanent_height.setter
    def permanent_height(self, value: OptionalNumber):
        self._set_attr("permanentHeight", value)

    # alignment
    @property
    def alignment(self) -> Optional[RichAttributionAlignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[RichAttributionAlignment]):
        self.__alignment = value
        self._set_enum_attr("alignment", value, RichAttributionAlignment)

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