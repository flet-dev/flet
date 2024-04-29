from typing import Any, Optional, List, Union

from flet_core.control import Control, OptionalNumber
from flet_core.map.map import MapLatitudeLongitude
from flet_core.ref import Ref


class Circle(Control):
    """
    TBA

    -----

    Online docs: https://flet.dev/docs/controls/mapcircle
    """

    def __init__(
        self,
        radius: Union[int, float],
        point: MapLatitudeLongitude,
        color: Optional[str] = None,
        border_color: Optional[str] = None,
        border_stroke_width: OptionalNumber = None,
        use_radius_in_meter: Optional[bool] = None,
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

        self.point = point
        self.color = color
        self.border_color = border_color
        self.border_stroke_width = border_stroke_width
        self.use_radius_in_meter = use_radius_in_meter
        self.radius = radius

    def _get_control_name(self):
        return "mapcircle"

    def before_update(self):
        super().before_update()
        self._set_attr_json("point", self.__point)

    # use_radius_in_meter
    @property
    def use_radius_in_meter(self) -> Optional[bool]:
        return self._get_attr("useRadiusInMeter", data_type="bool", def_value=False)

    @use_radius_in_meter.setter
    def use_radius_in_meter(self, value: Optional[bool]):
        self._set_attr("useRadiusInMeter", value)

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # border_color
    @property
    def border_color(self) -> Optional[str]:
        return self._get_attr("borderColor")

    @border_color.setter
    def border_color(self, value: Optional[str]):
        self._set_attr("borderColor", value)

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
        self._set_attr("borderStrokeWidth", value)

    # point
    @property
    def point(self) -> MapLatitudeLongitude:
        return self.__point

    @point.setter
    def point(self, value: MapLatitudeLongitude):
        self.__point = value


class CircleLayer(Control):
    """
    TBA


    -----

    Online docs: https://flet.dev/docs/controls/mapcirclelayer
    """

    def __init__(
        self,
        circles: List[Circle] = None,
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

        self.circles = circles

    def _get_control_name(self):
        return "mapcirclelayer"

    def _get_children(self):
        return self.__circles

    # circles
    @property
    def circles(self) -> List[Circle]:
        return self.__circles

    @circles.setter
    def circles(self, value: List[Circle]):
        self.__circles = value
