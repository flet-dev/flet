from typing import Any, List, Optional

from flet.core.alignment import Alignment
from flet.core.control import Control, OptionalNumber
from flet.core.map.map import MapLatitudeLongitude
from flet.core.map.map_layer import MapLayer
from flet.core.ref import Ref


class Marker(Control):
    """
    A marker displayed on the Map at the specified location through the MarkerLayer.

    -----

    Online docs: https://flet.dev/docs/controls/mapmarker
    """

    def __init__(
        self,
        content: Control,
        coordinates: MapLatitudeLongitude,
        rotate: Optional[bool] = None,
        height: OptionalNumber = None,
        width: OptionalNumber = None,
        alignment: Optional[Alignment] = None,
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

        self.content = content
        self.coordinates = coordinates
        self.rotate = rotate
        self.height = height
        self.width = width
        self.alignment = alignment

    def _get_control_name(self):
        return "map_marker"

    def _get_children(self):
        return [self.__content]

    def before_update(self):
        super().before_update()
        self._set_attr_json("alignment", self.__alignment)
        self._set_attr_json("coordinates", self.__coordinates)

    # content
    @property
    def content(self) -> Optional[Alignment]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Alignment]):
        self.__content = value

    # rotate
    @property
    def rotate(self) -> bool:
        return self._get_attr("rotate", data_type="bool", def_value=False)

    @rotate.setter
    def rotate(self, value: Optional[bool]):
        self._set_attr("rotate", value)

    # height
    @property
    def height(self) -> float:
        return self._get_attr("height", data_type="float", def_value=30.0)

    @height.setter
    def height(self, value: OptionalNumber):
        assert value is None or value >= 0, "height cannot be negative"
        self._set_attr("height", value)

    # width
    @property
    def width(self) -> float:
        return self._get_attr("width", data_type="float", def_value=30.0)

    @width.setter
    def width(self, value: OptionalNumber):
        assert value is None or value >= 0, "width cannot be negative"
        self._set_attr("width", value)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # coordinates
    @property
    def coordinates(self) -> MapLatitudeLongitude:
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, value: MapLatitudeLongitude):
        self.__coordinates = value


class MarkerLayer(MapLayer):
    """
    A layer to display Markers.

    -----

    Online docs: https://flet.dev/docs/controls/mapmarkerlayer
    """

    def __init__(
        self,
        markers: List[Marker],
        alignment: Optional[Alignment] = None,
        rotate: Optional[bool] = None,
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

        self.markers = markers
        self.alignment = alignment
        self.rotate = rotate

    def _get_control_name(self):
        return "map_marker_layer"

    def _get_children(self):
        return self.__markers

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

    # markers
    @property
    def markers(self) -> List[Marker]:
        return self.__markers

    @markers.setter
    def markers(self, value: List[Marker]):
        self.__markers = value

    # rotate
    @property
    def rotate(self) -> bool:
        return self._get_attr("rotate", data_type="bool", def_value=False)

    @rotate.setter
    def rotate(self, value: Optional[bool]):
        self._set_attr("rotate", value)
