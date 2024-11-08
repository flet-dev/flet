import json
from enum import Enum
from typing import Any, List, Optional, Tuple, Union

from flet.core.animation import AnimationCurve, AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.event_handler import EventHandler
from flet.core.map.map_configuration import MapConfiguration, MapLatitudeLongitude
from flet.core.map.map_layer import MapLayer
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.transform import Offset
from flet.core.types import (
    ControlEvent,
    DurationValue,
    Number,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
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
        configuration: MapConfiguration = MapConfiguration(),
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
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
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

        self.configuration = configuration
        self.layers = layers
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
        animation_duration: DurationValue = None,
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
        animation_duration: DurationValue = None,
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
        animation_duration: DurationValue = None,
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
        animation_duration: DurationValue = None,
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
        animation_duration: DurationValue = None,
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
        animation_duration: DurationValue = None,
    ):
        self.invoke_method(
            "animate_to",
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

    def before_update(self):
        self._set_attr_json("configuration", self.__configuration)

    def _get_children(self):
        return self.__layers

    # configuration
    @property
    def configuration(self) -> MapConfiguration:
        return self.__configuration

    @configuration.setter
    def configuration(self, value: MapConfiguration):
        self.__configuration = value

    # layers
    @property
    def layers(self) -> List[MapLayer]:
        return self.__layers

    @layers.setter
    def layers(self, value: List[MapLayer]):
        self.__layers = value

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


class MapPointerDeviceType(Enum):
    TOUCH = "touch"
    MOUSE = "mouse"
    STYLUS = "stylus"
    INVERTED_STYLUS = "invertedStylus"
    TRACKPAD = "trackpad"
    UNKNOWN = "unknown"


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
        self.device_type: MapPointerDeviceType = MapPointerDeviceType(d.get("kind"))
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
        self.device_type: MapPointerDeviceType = MapPointerDeviceType(d.get("kind"))
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
