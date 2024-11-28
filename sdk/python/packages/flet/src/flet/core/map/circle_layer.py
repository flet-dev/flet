from typing import Any, List, Optional, Union

from flet.core.control import Control, OptionalNumber
from flet.core.map.map import MapLatitudeLongitude
from flet.core.map.map_layer import MapLayer
from flet.core.ref import Ref
from flet.core.types import ColorEnums, ColorValue


class CircleMarker(Control):
    """
    A circular marker displayed on the Map at the specified location through the CircleLayer.

    -----

    Online docs: https://flet.dev/docs/controls/mapcirclemarker
    """

    def __init__(
        self,
        radius: Union[int, float],
        coordinates: MapLatitudeLongitude,
        color: Optional[ColorValue] = None,
        border_color: Optional[ColorValue] = None,
        border_stroke_width: OptionalNumber = None,
        use_radius_in_meter: Optional[bool] = None,
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

        self.coordinates = coordinates
        self.color = color
        self.border_color = border_color
        self.border_stroke_width = border_stroke_width
        self.use_radius_in_meter = use_radius_in_meter
        self.radius = radius

    def _get_control_name(self):
        return "map_circle_marker"

    def before_update(self):
        super().before_update()
        self._set_attr_json("coordinates", self.__coordinates)

    # use_radius_in_meter
    @property
    def use_radius_in_meter(self) -> bool:
        return self._get_attr("useRadiusInMeter", data_type="bool", def_value=False)

    @use_radius_in_meter.setter
    def use_radius_in_meter(self, value: Optional[bool]):
        self._set_attr("useRadiusInMeter", value)

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # border_color
    @property
    def border_color(self) -> Optional[ColorValue]:
        return self.__border_color

    @border_color.setter
    def border_color(self, value: Optional[ColorValue]):
        self.__border_color = value
        self._set_enum_attr("borderColor", value, ColorEnums)

    # radius
    @property
    def radius(self) -> Union[int, float]:
        return self._get_attr("radius", data_type="float")

    @radius.setter
    def radius(self, value: Union[int, float]):
        self._set_attr("radius", value)

    # border_stroke_width
    @property
    def border_stroke_width(self) -> OptionalNumber:
        return self._get_attr("borderStrokeWidth", data_type="float")

    @border_stroke_width.setter
    def border_stroke_width(self, value: OptionalNumber):
        assert value is None or value >= 0, "border_stroke_width cannot be negative"
        self._set_attr("borderStrokeWidth", value)

    # coordinates
    @property
    def coordinates(self) -> MapLatitudeLongitude:
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, value: MapLatitudeLongitude):
        self.__coordinates = value


class CircleLayer(MapLayer):
    """
    A layer to display CircleMarkers.

    -----

    Online docs: https://flet.dev/docs/controls/mapcirclelayer
    """

    def __init__(
        self,
        circles: List[CircleMarker],
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

        self.circles = circles

    def _get_control_name(self):
        return "map_circle_layer"

    def _get_children(self):
        return self.__circles

    # circles
    @property
    def circles(self) -> List[CircleMarker]:
        return self.__circles

    @circles.setter
    def circles(self, value: List[CircleMarker]):
        self.__circles = value
