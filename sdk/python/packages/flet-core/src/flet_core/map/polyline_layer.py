from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, List, Union

from flet_core.control import Control, OptionalNumber
from flet_core.map import MapLatitudeLongitude
from flet_core.map.map_layer import MapLayer
from flet_core.ref import Ref
from flet_core.types import StrokeCap, StrokeJoin


class PatternFit(Enum):
    SCALE_DOWN = "scaleDown"
    SCALE_UP = "scaleUp"
    APPEND_DOT = "appendDot"
    EXTEND_FINAL_DASH = "extendFinalDash"


@dataclass
class StrokePattern:
    pass


@dataclass
class SolidStrokePattern(StrokePattern):
    def __post_init__(self):
        self.type = "solid"


@dataclass
class DashedStrokePattern(StrokePattern):
    segments: Optional[List[Union[float, int]]] = None
    pattern_fit: Optional[PatternFit] = PatternFit.SCALE_UP

    def __post_init__(self):
        self.type = "dashed"


@dataclass
class DottedStrokePattern(StrokePattern):
    spacing_factor: OptionalNumber = None
    pattern_fit: Optional[PatternFit] = PatternFit.SCALE_UP

    def __post_init__(self):
        self.type = "dotted"


class PolylineMarker(Control):
    """
    A marker for the PolylineLayer.

    -----

    Online docs: https://flet.dev/docs/controls/mappolylinemarker
    """

    def __init__(
        self,
        coordinates: List[MapLatitudeLongitude],
        colors_stop: Optional[List[Union[float, int]]] = None,
        gradient_colors: Optional[List[str]] = None,
        border_color: Optional[str] = None,
        color: Optional[str] = None,
        stroke_width: OptionalNumber = None,
        border_stroke_width: OptionalNumber = None,
        use_stroke_width_in_meter: Optional[bool] = None,
        stroke_pattern: Optional[StrokePattern] = None,
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
        self.border_color = border_color
        self.color = color
        self.border_stroke_width = border_stroke_width
        self.stroke_width = stroke_width
        self.stroke_cap = stroke_cap
        self.stroke_join = stroke_join
        self.colors_stop = colors_stop
        self.gradient_colors = gradient_colors
        self.use_stroke_width_in_meter = use_stroke_width_in_meter
        self.stroke_pattern = stroke_pattern

    def _get_control_name(self):
        return "map_polyline_marker"

    def before_update(self):
        super().before_update()
        if isinstance(self.__coordinates, list):
            self._set_attr_json("coordinates", self.__coordinates)
        if isinstance(self.__colors_stop, list):
            self._set_attr_json("colorsStop", self.__colors_stop)
        if isinstance(self.__gradient_colors, list):
            self._set_attr_json("gradientColors", self.__gradient_colors)
        self._set_attr_json("strokePattern", self.__stroke_pattern)

    # stroke_cap
    @property
    def stroke_cap(self) -> Optional[StrokeCap]:
        return self.__stroke_cap

    @stroke_cap.setter
    def stroke_cap(self, value: Optional[StrokeCap]):
        self.__stroke_cap = value
        self._set_enum_attr("strokeCap", value, StrokeCap)

    # gradient_colors
    @property
    def gradient_colors(self) -> Optional[List[str]]:
        return self.__gradient_colors

    @gradient_colors.setter
    def gradient_colors(self, value: Optional[List[str]]):
        self.__gradient_colors = value

    # stroke_pattern
    @property
    def stroke_pattern(self) -> Optional[StrokePattern]:
        return self.__stroke_pattern

    @stroke_pattern.setter
    def stroke_pattern(self, value: Optional[StrokePattern]):
        self.__stroke_pattern = value

    # colors_stop
    @property
    def colors_stop(self) -> Optional[List[Union[float, int]]]:
        return self.__colors_stop

    @colors_stop.setter
    def colors_stop(self, value: Optional[List[Union[float, int]]]):
        self.__colors_stop = value

    # stroke_join
    @property
    def stroke_join(self) -> Optional[StrokeJoin]:
        return self.__stroke_join

    @stroke_join.setter
    def stroke_join(self, value: Optional[StrokeJoin]):
        self.__stroke_join = value
        self._set_enum_attr("strokeJoin", value, StrokeJoin)

    # use_stroke_width_in_meter
    @property
    def use_stroke_width_in_meter(self) -> Optional[bool]:
        return self._get_attr(
            "useStrokeWidthInMeter", data_type="bool", def_value=False
        )

    @use_stroke_width_in_meter.setter
    def use_stroke_width_in_meter(self, value: Optional[bool]):
        self._set_attr("useStrokeWidthInMeter", value)

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

    # stroke_width
    @property
    def stroke_width(self) -> OptionalNumber:
        return self._get_attr("strokeWidth", data_type="float", def_value=1.0)

    @stroke_width.setter
    def stroke_width(self, value: OptionalNumber):
        assert value is None or value >= 0, "stroke_width cannot be negative"
        self._set_attr("strokeWidth", value)

    # coordinates
    @property
    def coordinates(self) -> Optional[List[MapLatitudeLongitude]]:
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, value: Optional[List[MapLatitudeLongitude]]):
        self.__coordinates = value


class PolylineLayer(MapLayer):
    """
    A layer to display PolylineMarkers.

    -----

    Online docs: https://flet.dev/docs/controls/mappolylinelayer
    """

    def __init__(
        self,
        polylines: List[PolylineMarker],
        culling_margin: OptionalNumber = None,
        min_hittable_radius: OptionalNumber = None,
        simplify_tolerance: OptionalNumber = None,
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

        self.polylines = polylines
        self.culling_margin = culling_margin
        self.min_hittable_radius = min_hittable_radius
        self.simplify_tolerance = simplify_tolerance

    def _get_control_name(self):
        return "map_polyline_layer"

    def _get_children(self):
        return self.__polylines

    # polylines
    @property
    def polylines(self) -> List[PolylineMarker]:
        return self.__polylines

    @polylines.setter
    def polylines(self, value: List[PolylineMarker]):
        self.__polylines = value

    # culling_margin
    @property
    def culling_margin(self) -> OptionalNumber:
        return self._get_attr("cullingMargin", data_type="float", def_value=10)

    @culling_margin.setter
    def culling_margin(self, value: OptionalNumber):
        self._set_attr("cullingMargin", value)

    # simplification_tolerance
    @property
    def simplification_tolerance(self) -> OptionalNumber:
        return self._get_attr(
            "simplificationTolerance", data_type="float", def_value=0.4
        )

    @simplification_tolerance.setter
    def simplification_tolerance(self, value: OptionalNumber):
        self._set_attr("simplificationTolerance", value)

    # min_hittable_radius
    @property
    def min_hittable_radius(self) -> OptionalNumber:
        return self._get_attr("minHittableRadius", data_type="float", def_value=10)

    @min_hittable_radius.setter
    def min_hittable_radius(self, value: OptionalNumber):
        self._set_attr("minHittableRadius", value)
