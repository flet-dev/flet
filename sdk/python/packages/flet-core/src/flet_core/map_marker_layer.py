from typing import Any, Optional, List

from flet_core.alignment import Alignment
from flet_core.control import Control, OptionalNumber
from flet_core.map import MapLatitudeLongitude
from flet_core.ref import Ref


class MapMarker(Control):
    """
    TBA


    -----

    Online docs: https://flet.dev/docs/controls/mapmarkerlayer
    """

    def __init__(
        self,
        content: Control,
        point: MapLatitudeLongitude,
        rotate: Optional[bool] = None,
        height: OptionalNumber = None,
        width: OptionalNumber = None,
        alignment: Optional[Alignment] = None,
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

        self.content = content
        self.point = point
        self.rotate = rotate
        self.height = height
        self.width = width
        self.alignment = alignment

    def _get_control_name(self):
        return "mapmarker"

    def _get_children(self):
        return [self.__content]

    def before_update(self):
        super().before_update()
        self._set_attr_json("alignment", self.__alignment)
        self._set_attr_json("point", self.__point)

    # content
    @property
    def content(self) -> Optional[Alignment]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Alignment]):
        self.__content = value

    # rotate
    @property
    def rotate(self) -> Optional[bool]:
        return self._get_attr("rotate", data_type="bool")

    @rotate.setter
    def rotate(self, value: Optional[bool]):
        self._set_attr("rotate", value)

    # height
    @property
    def height(self) -> OptionalNumber:
        return self._get_attr("height", data_type="float")

    @height.setter
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)

    # width
    @property
    def width(self) -> OptionalNumber:
        return self._get_attr("width", data_type="float")

    @width.setter
    def width(self, value: OptionalNumber):
        self._set_attr("width", value)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # point
    @property
    def point(self) -> MapLatitudeLongitude:
        return self.__point

    @point.setter
    def point(self, value: MapLatitudeLongitude):
        self.__point = value


class MapMarkerLayer(Control):
    """
    TBA


    -----

    Online docs: https://flet.dev/docs/controls/mapmarkerlayer
    """

    def __init__(
        self,
        markers: List[MapMarker] = None,
        alignment: Optional[Alignment] = None,
        rotate: Optional[bool] = None,
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

        self.markers = markers
        self.alignment = alignment
        self.rotate = rotate

    def _get_control_name(self):
        return "mapmarkerlayer"

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
    def markers(self) -> List[MapMarker]:
        return self.__markers

    @markers.setter
    def markers(self, value: List[MapMarker]):
        self.__markers = value

    # rotate
    @property
    def rotate(self) -> Optional[bool]:
        return self._get_attr("rotate", data_type="bool", def_value=False)

    @rotate.setter
    def rotate(self, value: Optional[bool]):
        self._set_attr("rotate", value)
