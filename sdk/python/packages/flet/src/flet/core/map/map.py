import json
from dataclasses import dataclass
from enum import Enum, IntFlag
from typing import Any, List, Optional, Tuple, Union

from flet.core.animation import AnimationCurve, AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.event_handler import EventHandler
from flet.core.map.map_layer import MapLayer
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.transform import Offset
from flet.core.types import (
    ColorEnums,
    ColorValue,
    ControlEvent,
    DurationValue,
    Number,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    PointerDeviceType,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)
from flet.utils import deprecated


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
    enable_multi_finger_gesture_race: Optional[bool] = None
    pinch_move_threshold: OptionalNumber = None
    scroll_wheel_velocity: OptionalNumber = None
    pinch_zoom_threshold: OptionalNumber = None
    rotation_threshold: OptionalNumber = None
    flags: Optional[MapInteractiveFlag] = None
    rotation_win_gestures: Optional[MapMultiFingerGesture] = None
    pinch_move_win_gestures: Optional[MapMultiFingerGesture] = None
    pinch_zoom_win_gestures: Optional[MapMultiFingerGesture] = None


@deprecated(
    reason="Map control has been moved to a separate Python package: https://pypi.org/project/flet-map. "
    + "Read more about this change in Flet blog: https://flet.dev/blog/flet-v-0-26-release-announcement",
    version="0.26.0",
    delete_version="0.29.0",
)
class Map(ConstrainedControl):
    """
    Map Control.

    -----

    Online docs: https://flet.dev/docs/controls/map
    """

    def __init__(
        self,
        layers: List[MapLayer],
        initial_center: Optional[MapLatitudeLongitude] = None,
        initial_rotation: OptionalNumber = None,
        initial_zoom: OptionalNumber = None,
        interaction_configuration: Optional[MapInteractionConfiguration] = None,
        bgcolor: Optional[ColorValue] = None,
        keep_alive: Optional[bool] = None,
        max_zoom: OptionalNumber = None,
        min_zoom: OptionalNumber = None,
        animation_curve: Optional[AnimationCurve] = None,
        animation_duration: Optional[DurationValue] = None,
        on_init: OptionalControlEventCallable = None,
        on_tap: OptionalEventCallable["MapTapEvent"] = None,
        on_hover: OptionalEventCallable["MapHoverEvent"] = None,
        on_secondary_tap: OptionalEventCallable["MapTapEvent"] = None,
        on_long_press: OptionalEventCallable["MapTapEvent"] = None,
        on_event: OptionalEventCallable["MapEvent"] = None,
        on_position_change: OptionalEventCallable["MapPositionChangeEvent"] = None,
        on_pointer_down: OptionalEventCallable["MapPointerEvent"] = None,
        on_pointer_cancel: OptionalEventCallable["MapPointerEvent"] = None,
        on_pointer_up: OptionalEventCallable["MapPointerEvent"] = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.__on_tap = EventHandler(lambda e: MapTapEvent(e))
        self._add_event_handler("tap", self.__on_tap.get_handler())

        self.__on_hover = EventHandler(lambda e: MapHoverEvent(e))
        self._add_event_handler("hover", self.__on_hover.get_handler())

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

        self.layers = layers
        self.initial_center = initial_center
        self.initial_rotation = initial_rotation
        self.initial_zoom = initial_zoom
        self.interaction_configuration = interaction_configuration
        self.bgcolor = bgcolor
        self.keep_alive = keep_alive
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.animation_curve = animation_curve
        self.animation_duration = animation_duration
        self.on_tap = on_tap
        self.on_hover = on_hover
        self.on_secondary_tap = on_secondary_tap
        self.on_init = on_init
        self.on_long_press = on_long_press
        self.on_event = on_event
        self.on_position_change = on_position_change
        self.on_pointer_down = on_pointer_down
        self.on_pointer_cancel = on_pointer_cancel
        self.on_pointer_up = on_pointer_up

    def before_update(self):
        self._set_attr_json("initialCenter", self.__initial_center)
        self._set_attr_json("animationDuration", self.__animation_duration)
        self._set_attr_json(
            "interactionConfiguration", self.__interaction_configuration
        )

    def rotate_from(
        self,
        degree: Number,
        animation_curve: Optional[AnimationCurve] = None,
    ):
        self.invoke_method(
            "rotate_from",
            arguments={
                "degree": degree,
                "curve": animation_curve.value if animation_curve else None,
            },
        )

    def reset_rotation(
        self,
        animation_curve: Optional[AnimationCurve] = None,
        animation_duration: Optional[DurationValue] = None,
    ):
        self.invoke_method(
            "reset_rotation",
            arguments={
                "curve": animation_curve.value if animation_curve else None,
                "duration": self._convert_attr_json(animation_duration),
            },
        )

    def zoom_in(
        self,
        animation_curve: Optional[AnimationCurve] = None,
        animation_duration: Optional[DurationValue] = None,
    ):
        self.invoke_method(
            "zoom_in",
            arguments={
                "curve": animation_curve.value if animation_curve else None,
                "duration": self._convert_attr_json(animation_duration),
            },
        )

    def zoom_out(
        self,
        animation_curve: Optional[AnimationCurve] = None,
        animation_duration: Optional[DurationValue] = None,
    ):
        self.invoke_method(
            "zoom_out",
            arguments={
                "curve": animation_curve.value if animation_curve else None,
                "duration": self._convert_attr_json(animation_duration),
            },
        )

    def zoom_to(
        self,
        zoom: Number,
        animation_curve: Optional[AnimationCurve] = None,
        animation_duration: Optional[DurationValue] = None,
    ):
        self.invoke_method(
            "zoom_to",
            arguments={
                "zoom": zoom,
                "curve": animation_curve.value if animation_curve else None,
                "duration": self._convert_attr_json(animation_duration),
            },
        )

    def move_to(
        self,
        destination: Optional[MapLatitudeLongitude] = None,
        zoom: OptionalNumber = None,
        rotation: OptionalNumber = None,
        animation_curve: Optional[AnimationCurve] = None,
        animation_duration: Optional[DurationValue] = None,
        offset: Optional[Union[Offset, Tuple[Union[Number], Union[Number]]]] = None,
    ):
        if isinstance(offset, tuple):
            offset = Offset(offset[0], offset[1])
        self.invoke_method(
            "move_to",
            arguments={
                "lat": str(destination.latitude) if destination else None,
                "long": str(destination.longitude) if destination else None,
                "zoom": zoom,
                "ox": str(offset.x) if offset else None,
                "oy": str(offset.y) if offset else None,
                "rot": rotation,
                "curve": animation_curve.value if animation_curve else None,
                "duration": self._convert_attr_json(animation_duration),
            },
        )

    def center_on(
        self,
        point: Optional[MapLatitudeLongitude],
        zoom: OptionalNumber,
        animation_curve: Optional[AnimationCurve] = None,
        animation_duration: Optional[DurationValue] = None,
    ):
        self.invoke_method(
            "center_on",
            arguments={
                "lat": str(point.latitude) if point else None,
                "long": str(point.longitude) if point else None,
                "zoom": zoom,
                "curve": animation_curve.value if animation_curve else None,
                "duration": self._convert_attr_json(animation_duration),
            },
        )

    def _get_control_name(self):
        return "map"

    def _get_children(self):
        return self.__layers

    # layers
    @property
    def layers(self) -> List[MapLayer]:
        return self.__layers

    @layers.setter
    def layers(self, value: List[MapLayer]):
        self.__layers = value

    # initial_center
    @property
    def initial_center(self) -> Optional[MapLatitudeLongitude]:
        return self.__initial_center

    @initial_center.setter
    def initial_center(self, value: Optional[MapLatitudeLongitude]):
        self.__initial_center = value

    # initial_rotation
    @property
    def initial_rotation(self) -> OptionalNumber:
        return self._get_attr("initialRotation", data_type="float")

    @initial_rotation.setter
    def initial_rotation(self, value: OptionalNumber):
        self._set_attr("initialRotation", value)

    # initial_zoom
    @property
    def initial_zoom(self) -> OptionalNumber:
        return self._get_attr("initialZoom", data_type="float")

    @initial_zoom.setter
    def initial_zoom(self, value: OptionalNumber):
        self._set_attr("initialZoom", value)

    # interaction_configuration
    @property
    def interaction_configuration(self) -> Optional[MapInteractionConfiguration]:
        return self.__interaction_configuration

    @interaction_configuration.setter
    def interaction_configuration(self, value: Optional[MapInteractionConfiguration]):
        self.__interaction_configuration = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)

    # keep_alive
    @property
    def keep_alive(self) -> Optional[bool]:
        return self._get_attr("keepAlive", data_type="bool")

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

    # animation_curve
    @property
    def animation_curve(self) -> Optional[AnimationCurve]:
        return self.__animation_curve

    @animation_curve.setter
    def animation_curve(self, value: Optional[AnimationCurve]):
        self.__animation_curve = value
        self._set_enum_attr("animationCurve", value, AnimationCurve)

    # animation_duration
    @property
    def animation_duration(self) -> Optional[DurationValue]:
        return self.__animation_duration

    @animation_duration.setter
    def animation_duration(self, value: Optional[DurationValue]):
        self.__animation_duration = value

    # on_tap
    @property
    def on_tap(self) -> OptionalEventCallable["MapTapEvent"]:
        return self.__on_tap.handler

    @on_tap.setter
    def on_tap(self, handler: OptionalEventCallable["MapTapEvent"]):
        self.__on_tap.handler = handler
        self._set_attr("onTap", True if handler is not None else None)

    # on_hover
    @property
    def on_hover(self) -> OptionalEventCallable["MapHoverEvent"]:
        return self.__on_hover.handler

    @on_hover.setter
    def on_hover(self, handler: OptionalEventCallable["MapHoverEvent"]):
        self.__on_hover.handler = handler
        self._set_attr("onHover", True if handler is not None else None)

    # on_secondary_tap
    @property
    def on_secondary_tap(self) -> OptionalEventCallable["MapTapEvent"]:
        return self.__on_secondary_tap.handler

    @on_secondary_tap.setter
    def on_secondary_tap(self, handler: OptionalEventCallable["MapTapEvent"]):
        self.__on_secondary_tap.handler = handler
        self._set_attr("onSecondaryTap", True if handler is not None else None)

    # on_long_press
    @property
    def on_long_press(self) -> OptionalEventCallable["MapTapEvent"]:
        return self.__on_long_press.handler

    @on_long_press.setter
    def on_long_press(self, handler: OptionalEventCallable["MapTapEvent"]):
        self.__on_long_press.handler = handler
        self._set_attr("onLongPress", True if handler is not None else None)

    # on_event
    @property
    def on_event(self) -> OptionalEventCallable["MapEvent"]:
        return self.__on_event.handler

    @on_event.setter
    def on_event(self, handler: OptionalEventCallable["MapEvent"]):
        self.__on_event.handler = handler
        self._set_attr("onEvent", True if handler is not None else None)

    # on_init
    @property
    def on_init(self) -> OptionalControlEventCallable:
        return self._get_event_handler("init")

    @on_init.setter
    def on_init(self, handler: OptionalControlEventCallable):
        self._add_event_handler("init", handler)
        self._set_attr("onInit", True if handler is not None else None)

    # on_position_change
    @property
    def on_position_change(self) -> OptionalEventCallable["MapPositionChangeEvent"]:
        return self.__on_position_change.handler

    @on_position_change.setter
    def on_position_change(
        self, handler: OptionalEventCallable["MapPositionChangeEvent"]
    ):
        self.__on_position_change.handler = handler
        self._set_attr("onPositionChange", True if handler is not None else None)

    # on_pointer_down
    @property
    def on_pointer_down(self) -> OptionalEventCallable["MapPointerEvent"]:
        return self.__on_pointer_down.handler

    @on_pointer_down.setter
    def on_pointer_down(self, handler: OptionalEventCallable["MapPointerEvent"]):
        self.__on_pointer_down.handler = handler
        self._set_attr("onPointerDown", True if handler is not None else None)

    # on_pointer_cancel
    @property
    def on_pointer_cancel(self) -> OptionalEventCallable["MapPointerEvent"]:
        return self.__on_pointer_cancel.handler

    @on_pointer_cancel.setter
    def on_pointer_cancel(self, handler: OptionalEventCallable["MapPointerEvent"]):
        self.__on_pointer_cancel.handler = handler
        self._set_attr("onPointerCancel", True if handler is not None else None)

    # on_pointer_up
    @property
    def on_pointer_up(self) -> OptionalEventCallable["MapPointerEvent"]:
        return self.__on_pointer_up.handler

    @on_pointer_up.setter
    def on_pointer_up(self, handler: OptionalEventCallable["MapPointerEvent"]):
        self.__on_pointer_up.handler = handler
        self._set_attr("onPointerUp", True if handler is not None else None)


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


class MapTapEvent(ControlEvent):
    def __init__(self, e: ControlEvent) -> None:
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.local_x: Optional[float] = d.get("lx")
        self.local_y: Optional[float] = d.get("ly")
        self.global_x: float = d.get("gx")
        self.global_y: float = d.get("gy")
        self.coordinates: MapLatitudeLongitude = MapLatitudeLongitude(
            d.get("lat"), d.get("long")
        )


class MapHoverEvent(ControlEvent):
    def __init__(self, e: ControlEvent) -> None:
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.local_x: Optional[float] = d.get("lx")
        self.local_y: Optional[float] = d.get("ly")
        self.global_x: float = d.get("gx")
        self.global_y: float = d.get("gy")
        self.device_type: PointerDeviceType = PointerDeviceType(d.get("kind"))
        self.coordinates: MapLatitudeLongitude = MapLatitudeLongitude(
            d.get("lat"), d.get("long")
        )


class MapPositionChangeEvent(ControlEvent):
    def __init__(self, e: ControlEvent) -> None:
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.min_zoom: Optional[float] = d.get("min_zoom")
        self.max_zoom: Optional[float] = d.get("max_zoom")
        self.rotation: float = d.get("rot")
        self.coordinates: MapLatitudeLongitude = MapLatitudeLongitude(
            d.get("lat"), d.get("long")
        )


class MapPointerEvent(ControlEvent):
    def __init__(self, e: ControlEvent) -> None:
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.device_type: PointerDeviceType = PointerDeviceType(d.get("kind"))
        self.global_y: float = d.get("gy")
        self.global_x: float = d.get("gx")
        self.coordinates: MapLatitudeLongitude = MapLatitudeLongitude(
            d.get("lat"), d.get("long")
        )


class MapEvent(ControlEvent):
    def __init__(self, e: ControlEvent) -> None:
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.source: MapEventSource = MapEventSource(d.get("src"))
        self.center: MapLatitudeLongitude = MapLatitudeLongitude(
            d.get("c_lat"), d.get("c_long")
        )
        self.zoom: float = d.get("zoom")
        self.min_zoom: float = d.get("min_zoom")
        self.max_zoom: float = d.get("max_zoom")
        self.rotation: float = d.get("rot")
