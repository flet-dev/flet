from typing import Any, Optional, List

from flet_core.control import Control, OptionalNumber
from flet_core.map import MapLatitudeLongitude
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
        points: List[MapLatitudeLongitude],
        label: Optional[str] = None,
        label_style: Optional[TextStyle] = None,
        border_color: Optional[str] = None,
        color: Optional[str] = None,
        border_stroke_width: OptionalNumber = None,
        dotted: Optional[bool] = None,
        filled: Optional[bool] = None,
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

        self.points = points
        self.label = label
        self.label_style = label_style
        self.border_color = border_color
        self.color = color
        self.border_stroke_width = border_stroke_width
        self.dotted = dotted
        self.filled = filled
        self.disable_holes_border = disable_holes_border
        self.rotate_label = rotate_label
        self.stroke_cap = stroke_cap
        self.stroke_join = stroke_join

    def _get_control_name(self):
        return "mappolygonmarker"

    def before_update(self):
        super().before_update()
        if isinstance(self.__points, list):
            self._set_attr_json("points", self.__points)
        if isinstance(self.__label_style, TextStyle):
            self._set_attr_json("labelStyle", self.__label_style)

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

    # label_style
    @property
    def label_style(self) -> Optional[TextStyle]:
        return self.__label_style

    @label_style.setter
    def label_style(self, value: Optional[TextStyle]):
        self.__label_style = value

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

    # filled
    @property
    def filled(self) -> Optional[bool]:
        return self._get_attr("filled", data_type="bool", def_value=False)

    @filled.setter
    def filled(self, value: Optional[bool]):
        self._set_attr("filled", value)

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
        self._set_attr("borderStrokeWidth", value)

    # points
    @property
    def points(self) -> Optional[List[MapLatitudeLongitude]]:
        return self.__points

    @points.setter
    def points(self, value: Optional[List[MapLatitudeLongitude]]):
        self.__points = value


class PolygonLayer(Control):
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

        self.polygons = polygons
        self.polygon_culling = polygon_culling
        self.polygon_labels = polygon_labels
        self.draw_labels_last = draw_labels_last

    def _get_control_name(self):
        return "mappolygonlayer"

    def _get_children(self):
        return self.__polygons

    def add(self, *marker: PolygonMarker):
        self.__polygons.extend(marker)
        self.update()

    def insert(self, at: int, *polygons: PolygonMarker) -> None:
        for i, marker in enumerate(polygons, start=at):
            self.__polygons.insert(i, marker)
        self.update()

    def remove(self, *polygons: PolygonMarker) -> None:
        for marker in polygons:
            self.__polygons.remove(marker)
        self.update()

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
