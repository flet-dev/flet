import json
from dataclasses import dataclass, field
from enum import Enum, IntFlag
from typing import Optional, Union, Callable

from flet_core.control import OptionalNumber, Control
from flet_core.event_handler import EventHandler
from flet_core.types import ControlEvent, OptionalEventCallable


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


class MapPointerDeviceType(Enum):
    TOUCH = "touch"
    MOUSE = "mouse"
    STYLUS = "stylus"
    INVERTED_STYLUS = "invertedStylus"
    TRACKPAD = "trackpad"
    UNKNOWN = "unknown"


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
        on_init: OptionalEventCallable = None,
        on_tap: Optional[Callable[["MapTapEvent"], None]] = None,
        on_secondary_tap: Optional[Callable[["MapTapEvent"], None]] = None,
        on_long_press: Optional[Callable[["MapTapEvent"], None]] = None,
        on_event: Optional[Callable[["MapEvent"], None]] = None,
        on_position_change: Optional[Callable[["MapPositionChangeEvent"], None]] = None,
        on_pointer_down: Optional[Callable[["MapPointerEvent"], None]] = None,
        on_pointer_cancel: Optional[Callable[["MapPointerEvent"], None]] = None,
        on_pointer_up: Optional[Callable[["MapPointerEvent"], None]] = None,
    ):
        Control.__init__(self)
        self.__on_tap = EventHandler(lambda e: MapTapEvent(e))
        self._add_event_handler("tap", self.__on_tap.get_handler())

        self.__on_secondary_tap = EventHandler(lambda e: MapTapEvent(e))
        self._add_event_handler("secondary_tap", self.__on_secondary_tap.get_handler())

        self.__on_long_press = EventHandler(lambda e: MapTapEvent(e))
        self._add_event_handler("long_press", self.__on_long_press.get_handler())

        self.__on_event = EventHandler(lambda e: MapEvent(e))
        self._add_event_handler("event", self.__on_event.get_handler())

        self.__on_position_change = EventHandler(lambda e: MapPositionChangeEvent(e))
        self._add_event_handler(
            "position_change", self.__on_position_change.get_handler()
        )

        self.__on_pointer_down = EventHandler(lambda e: MapPointerEvent(e))
        self._add_event_handler("pointer_down", self.__on_pointer_down.get_handler())

        self.__on_pointer_cancel = EventHandler(lambda e: MapPointerEvent(e))
        self._add_event_handler(
            "pointer_cancel", self.__on_pointer_cancel.get_handler()
        )

        self.__on_pointer_up = EventHandler(lambda e: MapPointerEvent(e))
        self._add_event_handler("pointer_up", self.__on_pointer_up.get_handler())

        self.bgcolor = bgcolor
        self.initial_center = initial_center
        self.initial_rotation = initial_rotation
        self.initial_zoom = initial_zoom
        self.interaction_configuration = interaction_configuration
        self.keep_alive = keep_alive
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.on_tap = on_tap
        self.on_secondary_tap = on_secondary_tap
        self.on_init = on_init
        self.on_long_press = on_long_press
        self.on_event = on_event
        self.on_position_change = on_position_change
        self.on_pointer_down = on_pointer_down
        self.on_pointer_cancel = on_pointer_cancel
        self.on_pointer_up = on_pointer_up

    def _get_control_name(self):
        return "map_configuration"

    def before_update(self):
        super().before_update()
        if isinstance(self.__initial_center, MapLatitudeLongitude):
            self._set_attr_json("initialCenter", self.__initial_center)
        if isinstance(self.__interaction_configuration, MapInteractionConfiguration):
            self._set_attr_json(
                "interactionConfiguration", self.__interaction_configuration
            )

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
    def initial_rotation(self) -> OptionalNumber:
        return self._get_attr("initialRotation", data_type="float", def_value=0.0)

    @initial_rotation.setter
    def initial_rotation(self, value: OptionalNumber):
        self._set_attr("initialRotation", value)

    # initial_zoom
    @property
    def initial_zoom(self) -> OptionalNumber:
        return self._get_attr("initialZoom", data_type="float", def_value=13.0)

    @initial_zoom.setter
    def initial_zoom(self, value: OptionalNumber):
        self._set_attr("initialZoom", value)

    # keep_alive
    @property
    def keep_alive(self) -> Optional[bool]:
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

    # on_tap
    @property
    def on_tap(self):
        return self.__on_tap

    @on_tap.setter
    def on_tap(self, handler: Optional[Callable[["MapTapEvent"], None]]):
        self.__on_tap.subscribe(handler)
        self._set_attr("onTap", True if handler is not None else None)

    # on_secondary_tap
    @property
    def on_secondary_tap(self):
        return self.__on_secondary_tap

    @on_secondary_tap.setter
    def on_secondary_tap(self, handler: Optional[Callable[["MapTapEvent"], None]]):
        self.__on_secondary_tap.subscribe(handler)
        self._set_attr("onSecondaryTap", True if handler is not None else None)

    # on_long_press
    @property
    def on_long_press(self):
        return self.__on_long_press

    @on_long_press.setter
    def on_long_press(self, handler: Optional[Callable[["MapTapEvent"], None]]):
        self.__on_long_press.subscribe(handler)
        self._set_attr("onLongPress", True if handler is not None else None)

    # on_event
    @property
    def on_event(self):
        return self.__on_event

    @on_event.setter
    def on_event(self, handler: Optional[Callable[["MapEvent"], None]]):
        self.__on_event.subscribe(handler)
        self._set_attr("onEvent", True if handler is not None else None)

    # on_init
    @property
    def on_init(self) -> OptionalEventCallable:
        return self._get_event_handler("init")

    @on_init.setter
    def on_init(self, handler: OptionalEventCallable):
        self._add_event_handler("init", handler)
        self._set_attr("onInit", True if handler is not None else None)

    # on_position_change
    @property
    def on_position_change(self):
        return self.__on_position_change

    @on_position_change.setter
    def on_position_change(
        self, handler: Optional[Callable[["MapPositionChangeEvent"], None]]
    ):
        self.__on_position_change.subscribe(handler)
        self._set_attr("onPositionChange", True if handler is not None else None)

    # on_pointer_down
    @property
    def on_pointer_down(self):
        return self.__on_pointer_down

    @on_pointer_down.setter
    def on_pointer_down(self, handler: Optional[Callable[["MapPointerEvent"], None]]):
        self.__on_pointer_down.subscribe(handler)
        self._set_attr("onPointerDown", True if handler is not None else None)

    # on_pointer_cancel
    @property
    def on_pointer_cancel(self):
        return self.__on_pointer_cancel

    @on_pointer_cancel.setter
    def on_pointer_cancel(self, handler: Optional[Callable[["MapPointerEvent"], None]]):
        self.__on_pointer_cancel.subscribe(handler)
        self._set_attr("onPointerCancel", True if handler is not None else None)

    # on_pointer_up
    @property
    def on_pointer_up(self):
        return self.__on_pointer_up

    @on_pointer_up.setter
    def on_pointer_up(self, handler: Optional[Callable[["MapPointerEvent"], None]]):
        self.__on_pointer_up.subscribe(handler)
        self._set_attr("onPointerUp", True if handler is not None else None)


class MapTapEvent(ControlEvent):
    def __init__(self, e: ControlEvent) -> None:
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.local_x: Optional[float] = d["lx"]
        self.local_y: Optional[float] = d["ly"]
        self.global_x: float = d["gx"]
        self.global_y: float = d["gy"]
        self.coordinates: MapLatitudeLongitude = MapLatitudeLongitude(
            d["lat"], d["long"]
        )


class MapPositionChangeEvent(ControlEvent):
    def __init__(self, e: ControlEvent) -> None:
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.min_zoom: Optional[float] = d["min_zoom"]
        self.max_zoom: Optional[float] = d["max_zoom"]
        self.rot: float = d["rot"]
        self.coordinates: MapLatitudeLongitude = MapLatitudeLongitude(
            d["lat"], d["long"]
        )


class MapPointerEvent(ControlEvent):
    def __init__(self, e: ControlEvent) -> None:
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.device_type: MapPointerDeviceType = MapPointerDeviceType(d["kind"])
        self.global_y: float = d["gy"]
        self.global_x: float = d["gx"]
        self.coordinates: MapLatitudeLongitude = MapLatitudeLongitude(
            d["lat"], d["long"]
        )


class MapEventSource(Enum):
    MAP_CONTROLLER = "mapController"
    TAP = "tap"
    SECONDARY_TAP = "secondaryTap"
    LONG_PRESS = "longPress"
    DOUBLE_TAP = "doubleTap"
    DOUBLE_TAP_HOLD = "doubleTapHold"
    DRAG_START = "dragStart"
    ON_DRAG = "onDrag"
    DRAG_END = "dragEnd"
    MULTI_FINGER_GESTURE_START = "multiFingerGestureStart"
    ON_MULTI_FINGER = "onMultiFinger"
    MULTI_FINGER_GESTURE_END = "multiFingerEnd"
    FLING_ANIMATION_CONTROLLER = "flingAnimationController"
    DOUBLE_TAP_ZOOM_ANIMATION_CONTROLLER = "doubleTapZoomAnimationController"
    INTERACTIVE_FLAGS_CHANGED = "interactiveFlagsChanged"
    FIT_CAMERA = "fitCamera"
    CUSTOM = "custom"
    SCROLL_WHEEL = "scrollWheel"
    NON_ROTATED_SIZE_CHANGE = "nonRotatedSizeChange"
    CURSOR_KEYBOARD_ROTATION = "cursorKeyboardRotation"


class MapEvent(ControlEvent):
    def __init__(self, e: ControlEvent) -> None:
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.source: MapEventSource = MapEventSource(d["src"])
        self.center: MapLatitudeLongitude = MapLatitudeLongitude(
            d["c_lat"], d["c_long"]
        )
        self.zoom: float = d["zoom"]
        self.min_zoom: float = d["min_zoom"]
        self.max_zoom: float = d["max_zoom"]
        self.rotation: float = d["rot"]
