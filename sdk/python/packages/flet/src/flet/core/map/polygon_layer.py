from typing import Any, List, Optional

from flet.core.control import Control, OptionalNumber
from flet.core.map.map import MapLatitudeLongitude
from flet.core.map.map_layer import MapLayer
from flet.core.ref import Ref
from flet.core.text_style import TextStyle
from flet.core.types import ColorEnums, ColorValue, StrokeCap, StrokeJoin


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
        border_color: Optional[ColorValue] = None,
        color: Optional[ColorValue] = None,
        border_stroke_width: OptionalNumber = None,
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
        self.disable_holes_border = disable_holes_border
        self.rotate_label = rotate_label
        self.stroke_cap = stroke_cap
        self.stroke_join = stroke_join

    def _get_control_name(self):
        return "map_polygon_marker"

    def before_update(self):
        super().before_update()
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
    def rotate_label(self) -> bool:
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
    def disable_holes_border(self) -> bool:
        return self._get_attr("disableHolesBorder", data_type="bool", def_value=False)

    @disable_holes_border.setter
    def disable_holes_border(self, value: Optional[bool]):
        self._set_attr("disableHolesBorder", value)

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

    # border_stroke_width
    @property
    def border_stroke_width(self) -> float:
        return self._get_attr("borderStrokeWidth", data_type="float", def_value=0.0)

    @border_stroke_width.setter
    def border_stroke_width(self, value: OptionalNumber):
        assert value is None or value >= 0, "border_stroke_width cannot be negative"
        self._set_attr("borderStrokeWidth", value)

    # coordinates
    @property
    def coordinates(self) -> List[MapLatitudeLongitude]:
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, value: List[MapLatitudeLongitude]):
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
        simplification_tolerance: OptionalNumber = None,
        use_alternative_rendering: Optional[bool] = None,
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
        self.simplification_tolerance = simplification_tolerance
        self.use_alternative_rendering = use_alternative_rendering

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
    def polygon_culling(self) -> bool:
        return self._get_attr("polygonCulling", data_type="bool", def_value=False)

    @polygon_culling.setter
    def polygon_culling(self, value: Optional[bool]):
        self._set_attr("polygonCulling", value)

    # use_alternative_rendering
    @property
    def use_alternative_rendering(self) -> bool:
        return self._get_attr(
            "useAlternativeRendering", data_type="bool", def_value=False
        )

    @use_alternative_rendering.setter
    def use_alternative_rendering(self, value: Optional[bool]):
        self._set_attr("useAlternativeRendering", value)

    # polygon_labels
    @property
    def polygon_labels(self) -> bool:
        return self._get_attr("polygonLabels", data_type="bool", def_value=True)

    @polygon_labels.setter
    def polygon_labels(self, value: Optional[bool]):
        self._set_attr("polygonLabels", value)

    # simplification_tolerance
    @property
    def simplification_tolerance(self) -> float:
        return self._get_attr(
            "simplificationTolerance", data_type="float", def_value=0.5
        )

    @simplification_tolerance.setter
    def simplification_tolerance(self, value: OptionalNumber):
        self._set_attr("simplificationTolerance", value)

    # draw_labels_last
    @property
    def draw_labels_last(self) -> bool:
        return self._get_attr("drawLabelsLast", data_type="bool", def_value=False)

    @draw_labels_last.setter
    def draw_labels_last(self, value: Optional[bool]):
        self._set_attr("drawLabelsLast", value)
