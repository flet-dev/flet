from dataclasses import dataclass, field
from dataclasses import dataclass, field
from enum import IntFlag
from typing import Optional, Union

from flet_core.animation import AnimationCurve
from flet_core.control import OptionalNumber, Control
from flet_core.types import (
    DurationValue,
)


@dataclass
class MapLatitudeLongitude:
    latitude: Union[float, int]
    longitude: Union[float, int]


@dataclass
class MapLatitudeLongitudeBounds:
    corner_1: MapLatitudeLongitude
    corner_2: MapLatitudeLongitude


class MapInteractiveFlag(IntFlag):
    NONE = 0
    DRAG = 1 << 0
    FLING_ANIMATION = 1 << 1
    PINCH_MOVE = 1 << 2
    PINCH_ZOOM = 1 << 3
    DOUBLE_TAP_ZOOM = 1 << 4
    DOUBLE_TAP_DRAG_ZOOM = 1 << 5
    SCROLL_WHEEL_ZOOM = 1 << 6
    ROTATE = 1 << 7
    ALL = (
        (1 << 0)
        | (1 << 1)
        | (1 << 2)
        | (1 << 3)
        | (1 << 4)
        | (1 << 5)
        | (1 << 6)
        | (1 << 7)
    )


class MapMultiFingerGesture(IntFlag):
    NONE = 0
    PINCH_MOVE = 1 << 0
    PINCH_ZOOM = 1 << 1
    ROTATE = 1 << 2
    ALL = (1 << 0) | (1 << 1) | (1 << 2)


@dataclass
class MapInteractionConfiguration:
    enable_multi_finger_gesture_race: Optional[bool] = field(default=None)
    pinch_move_threshold: OptionalNumber = field(default=None)
    scroll_wheel_velocity: OptionalNumber = field(default=None)
    pinch_zoom_threshold: OptionalNumber = field(default=None)
    rotation_threshold: OptionalNumber = field(default=None)
    flags: Optional[MapInteractiveFlag] = field(default=None)
    rotation_win_gestures: Optional[MapMultiFingerGesture] = field(default=None)
    pinch_move_win_gestures: Optional[MapMultiFingerGesture] = field(default=None)
    pinch_zoom_win_gestures: Optional[MapMultiFingerGesture] = field(default=None)


class MapConfiguration(Control):
    def __init__(
        self,
        initial_center: Optional[MapLatitudeLongitude] = None,
        initial_rotation: OptionalNumber = None,
        initial_zoom: OptionalNumber = None,
        interaction_configuration: Optional[MapInteractionConfiguration] = None,
        bgcolor: Optional[str] = None,
        keep_alive: Optional[bool] = None,
        max_zoom: OptionalNumber = None,
        min_zoom: OptionalNumber = None,
        animation_curve: Optional[AnimationCurve] = None,
        animation_duration: DurationValue = None,
    ):
        Control.__init__(self)

        self.bgcolor = bgcolor
        self.initial_center = initial_center
        self.initial_rotation = initial_rotation
        self.initial_zoom = initial_zoom
        self.interaction_configuration = interaction_configuration
        self.keep_alive = keep_alive
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.animation_curve = animation_curve
        self.animation_duration = animation_duration

    def _get_control_name(self):
        return "map_configuration"

    def before_update(self):
        super().before_update()
        self._set_attr_json("initialCenter", self.__initial_center)
        self._set_attr_json(
            "interactionConfiguration", self.__interaction_configuration
        )
        self._set_attr_json("animationDuration", self.__animation_duration)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # initial_center
    @property
    def initial_center(self) -> Optional[MapLatitudeLongitude]:
        return self.__initial_center

    @initial_center.setter
    def initial_center(self, value: Optional[MapLatitudeLongitude]):
        self.__initial_center = value

    # interaction_configuration
    @property
    def interaction_configuration(self) -> Optional[MapInteractionConfiguration]:
        return self.__interaction_configuration

    @interaction_configuration.setter
    def interaction_configuration(self, value: Optional[MapInteractionConfiguration]):
        self.__interaction_configuration = value

    # initial_rotation
    @property
    def initial_rotation(self) -> float:
        return self._get_attr("initialRotation", data_type="float", def_value=0.0)

    @initial_rotation.setter
    def initial_rotation(self, value: OptionalNumber):
        self._set_attr("initialRotation", value)

    # initial_zoom
    @property
    def initial_zoom(self) -> float:
        return self._get_attr("initialZoom", data_type="float", def_value=13.0)

    @initial_zoom.setter
    def initial_zoom(self, value: OptionalNumber):
        self._set_attr("initialZoom", value)

    # keep_alive
    @property
    def keep_alive(self) -> bool:
        return self._get_attr("keepAlive", data_type="bool", def_value=False)

    @keep_alive.setter
    def keep_alive(self, value: Optional[bool]):
        self._set_attr("keepAlive", value)

    # max_zoom
    @property
    def max_zoom(self) -> OptionalNumber:
        return self._get_attr("maxZoom", data_type="float")

    @max_zoom.setter
    def max_zoom(self, value: OptionalNumber):
        self._set_attr("maxZoom", value)

    # min_zoom
    @property
    def min_zoom(self) -> OptionalNumber:
        return self._get_attr("minZoom", data_type="float")

    @min_zoom.setter
    def min_zoom(self, value: OptionalNumber):
        self._set_attr("minZoom", value)

    # animation_duration
    @property
    def animation_duration(self) -> DurationValue:
        return self.__animation_duration

    @animation_duration.setter
    def animation_duration(self, value: DurationValue):
        self.__animation_duration = value

    # animation_curve
    @property
    def animation_curve(self) -> AnimationCurve:
        return self.__animation_curve

    @animation_curve.setter
    def animation_curve(self, value: AnimationCurve):
        self.__animation_curve = value
        self._set_enum_attr("animationCurve", value, AnimationCurve)
