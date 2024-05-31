from typing import Any, Optional, List

from flet_core.control import Control, OptionalNumber
from flet_core.map import MapLatitudeLongitude
from flet_core.map.map_layer import MapLayer
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import StrokeCap, StrokeJoin


class PolygonMarker(Control):
    """
    A marker for the PolygonLayer.

    -----

    Online docs: https://flet.dev/docs/controls/mappolygonmarker
    """

    def __init__(
        self,
        coordinates: List[MapLatitudeLongitude],
        label: Optional[str] = None,
        label_text_style: Optional[TextStyle] = None,
        border_color: Optional[str] = None,
        color: Optional[str] = None,
        border_stroke_width: OptionalNumber = None,
        dotted: Optional[bool] = None,
        disable_holes_border: Optional[bool] = None,
        rotate_label: Optional[bool] = None,
        stroke_cap: Optional[StrokeCap] = None,
        stroke_join: Optional[StrokeJoin] = None,
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
        self.label = label
        self.label_text_style = label_text_style
        self.border_color = border_color
        self.color = color
        self.border_stroke_width = border_stroke_width
        self.dotted = dotted
        self.disable_holes_border = disable_holes_border
        self.rotate_label = rotate_label
        self.stroke_cap = stroke_cap
        self.stroke_join = stroke_join

    def _get_control_name(self):
        return "map_polygon_marker"

    def before_update(self):
        super().before_update()
        if isinstance(self.__coordinates, list):
            self._set_attr_json("coordinates", self.__coordinates)
        if isinstance(self.__label_text_style, TextStyle):
            self._set_attr_json("labelTextStyle", self.__label_text_style)

    # stroke_cap
    @property
    def stroke_cap(self) -> Optional[StrokeCap]:
        return self.__stroke_cap

    @stroke_cap.setter
    def stroke_cap(self, value: Optional[StrokeCap]):
        self.__stroke_cap = value
        self._set_enum_attr("strokeCap", value, StrokeCap)

    # stroke_join
    @property
    def stroke_join(self) -> Optional[StrokeJoin]:
        return self.__stroke_join

    @stroke_join.setter
    def stroke_join(self, value: Optional[StrokeJoin]):
        self.__stroke_join = value
        self._set_enum_attr("strokeJoin", value, StrokeJoin)

    # label_text_style
    @property
    def label_text_style(self) -> Optional[TextStyle]:
        return self.__label_text_style

    @label_text_style.setter
    def label_text_style(self, value: Optional[TextStyle]):
        self.__label_text_style = value

    # rotate_label
    @property
    def rotate_label(self) -> Optional[bool]:
        return self._get_attr("rotateLabel", data_type="bool", def_value=False)

    @rotate_label.setter
    def rotate_label(self, value: Optional[bool]):
        self._set_attr("rotateLabel", value)

    # label
    @property
    def label(self) -> Optional[str]:
        return self._get_attr("label")

    @label.setter
    def label(self, value: Optional[str]):
        self._set_attr("label", value)

    # disable_holes_border
    @property
    def disable_holes_border(self) -> Optional[bool]:
        return self._get_attr("disableHolesBorder", data_type="bool", def_value=False)

    @disable_holes_border.setter
    def disable_holes_border(self, value: Optional[bool]):
        self._set_attr("disableHolesBorder", value)

    # dotted
    @property
    def dotted(self) -> Optional[bool]:
        return self._get_attr("dotted", data_type="bool", def_value=False)

    @dotted.setter
    def dotted(self, value: Optional[bool]):
        self._set_attr("dotted", value)

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

    # border_stroke_width
    @property
    def border_stroke_width(self) -> OptionalNumber:
        return self._get_attr("borderStrokeWidth", data_type="float", def_value=0)

    @border_stroke_width.setter
    def border_stroke_width(self, value: OptionalNumber):
        assert value is None or value >= 0, "border_stroke_width cannot be negative"
        self._set_attr("borderStrokeWidth", value)

    # coordinates
    @property
    def coordinates(self) -> Optional[List[MapLatitudeLongitude]]:
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, value: Optional[List[MapLatitudeLongitude]]):
        self.__coordinates = value


class PolygonLayer(MapLayer):
    """
    A layer to display PolygonMarkers.

    -----

    Online docs: https://flet.dev/docs/controls/mappolygonlayer
    """

    def __init__(
        self,
        polygons: List[PolygonMarker],
        polygon_culling: Optional[bool] = None,
        polygon_labels: Optional[bool] = None,
        draw_labels_last: Optional[bool] = None,
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

        self.polygons = polygons
        self.polygon_culling = polygon_culling
        self.polygon_labels = polygon_labels
        self.draw_labels_last = draw_labels_last

    def _get_control_name(self):
        return "map_polygon_layer"

    def _get_children(self):
        return self.__polygons

    # polygons
    @property
    def polygons(self) -> List[PolygonMarker]:
        return self.__polygons

    @polygons.setter
    def polygons(self, value: List[PolygonMarker]):
        self.__polygons = value

    # polygon_culling
    @property
    def polygon_culling(self) -> Optional[bool]:
        return self._get_attr("polygonCulling", data_type="bool", def_value=False)

    @polygon_culling.setter
    def polygon_culling(self, value: Optional[bool]):
        self._set_attr("polygonCulling", value)

    # polygon_labels
    @property
    def polygon_labels(self) -> Optional[bool]:
        return self._get_attr("polygonLabels", data_type="bool", def_value=True)

    @polygon_labels.setter
    def polygon_labels(self, value: Optional[bool]):
        self._set_attr("polygonLabels", value)

    # draw_labels_last
    @property
    def draw_labels_last(self) -> Optional[bool]:
        return self._get_attr("drawLabelsLast", data_type="bool", def_value=False)

    @draw_labels_last.setter
    def draw_labels_last(self, value: Optional[bool]):
        self._set_attr("drawLabelsLast", value)
