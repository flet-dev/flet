import json
from typing import Any, Optional

from beartype import beartype

from flet.control import Control
from flet.control_event import ControlEvent
from flet.event_handler import EventHandler
from flet.ref import Ref


class GestureDetector(Control):
    def __init__(
        self,
        content: Control,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        on_tap=None,
        on_tap_down=None,
        on_tap_up=None,
        on_secondary_tap=None,
        on_secondary_tap_down=None,
        on_secondary_tap_up=None,
        on_long_press_start=None,
        on_long_press_end=None,
        on_secondary_long_press_start=None,
        on_secondary_long_press_end=None,
        on_double_tap=None,
        on_double_tap_down=None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.__on_tap_down = EventHandler(lambda e: TapEvent(**json.loads(e.data)))
        self._add_event_handler("tap_down", self.__on_tap_down.handler)

        self.__on_tap_up = EventHandler(lambda e: TapEvent(**json.loads(e.data)))
        self._add_event_handler("tap_up", self.__on_tap_up.handler)

        self.__on_secondary_tap_down = EventHandler(
            lambda e: TapEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "secondary_tap_down", self.__on_secondary_tap_down.handler
        )

        self.__on_secondary_tap_up = EventHandler(
            lambda e: TapEvent(**json.loads(e.data))
        )
        self._add_event_handler("secondary_tap_up", self.__on_secondary_tap_up.handler)

        self.__on_long_press_start = EventHandler(
            lambda e: LongPressStartEvent(**json.loads(e.data))
        )
        self._add_event_handler("long_press_start", self.__on_long_press_start.handler)

        self.__on_long_press_end = EventHandler(
            lambda e: LongPressEndEvent(**json.loads(e.data))
        )
        self._add_event_handler("long_press_end", self.__on_long_press_end.handler)

        self.__on_secondary_long_press_start = EventHandler(
            lambda e: LongPressStartEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "secondary_long_press_start", self.__on_secondary_long_press_start.handler
        )

        self.__on_secondary_long_press_end = EventHandler(
            lambda e: LongPressEndEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "secondary_long_press_end", self.__on_secondary_long_press_end.handler
        )
        self.__on_double_tap_down = EventHandler(
            lambda e: TapEvent(**json.loads(e.data))
        )
        self._add_event_handler("double_tap_down", self.__on_double_tap_down.handler)

        self.content = content
        self.on_tap = on_tap
        self.on_tap_down = on_tap_down
        self.on_tap_up = on_tap_up
        self.on_secondary_tap = on_secondary_tap
        self.on_secondary_tap_down = on_secondary_tap_down
        self.on_secondary_tap_up = on_secondary_tap_up
        self.on_long_press_start = on_long_press_start
        self.on_long_press_end = on_long_press_end
        self.on_secondary_long_press_start = on_secondary_long_press_start
        self.on_secondary_long_press_end = on_secondary_long_press_end
        self.on_double_tap = on_double_tap
        self.on_double_tap_down = on_double_tap_down

    def _get_control_name(self):
        return "gesturedetector"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Control):
        self.__content = value

    # on_tap
    @property
    def on_tap(self):
        return self._get_event_handler("tap")

    @on_tap.setter
    def on_tap(self, handler):
        self._add_event_handler("tap", handler)
        self._set_attr("onTap", True if handler is not None else None)

    # on_tap_down
    @property
    def on_tap_down(self):
        return self.__on_tap_down

    @on_tap_down.setter
    def on_tap_down(self, handler):
        self.__on_tap_down.subscribe(handler)
        self._set_attr("onTapDown", True if handler is not None else None)

    # on_tap_up
    @property
    def on_tap_up(self):
        return self.__on_tap_up

    @on_tap_up.setter
    def on_tap_up(self, handler):
        self.__on_tap_up.subscribe(handler)
        self._set_attr("onTapUp", True if handler is not None else None)

    # on_secondary_tap
    @property
    def on_secondary_tap(self):
        return self._get_event_handler("secondary_tap")

    @on_secondary_tap.setter
    def on_secondary_tap(self, handler):
        self._add_event_handler("secondary_tap", handler)
        self._set_attr("onSecondaryTap", True if handler is not None else None)

    # on_tap_down
    @property
    def on_secondary_tap_down(self):
        return self.__on_secondary_tap_down

    @on_secondary_tap_down.setter
    def on_secondary_tap_down(self, handler):
        self.__on_secondary_tap_down.subscribe(handler)
        self._set_attr("onSecondaryTapDown", True if handler is not None else None)

    # on_secondary_tap_up
    @property
    def on_secondary_tap_up(self):
        return self.__on_secondary_tap_up

    @on_secondary_tap_up.setter
    def on_secondary_tap_up(self, handler):
        self.__on_secondary_tap_up.subscribe(handler)
        self._set_attr("onSecondaryTapUp", True if handler is not None else None)

    # on_long_press_start
    @property
    def on_long_press_start(self):
        return self.__on_long_press_start

    @on_long_press_start.setter
    def on_long_press_start(self, handler):
        self.__on_long_press_start.subscribe(handler)
        self._set_attr("onLongPressStart", True if handler is not None else None)

    # on_long_press_end
    @property
    def on_long_press_end(self):
        return self.__on_long_press_end

    @on_long_press_end.setter
    def on_long_press_end(self, handler):
        self.__on_long_press_end.subscribe(handler)
        self._set_attr("onLongPressEnd", True if handler is not None else None)

    # on_secondary_long_press_start
    @property
    def on_secondary_long_press_start(self):
        return self.__on_secondary_long_press_start

    @on_secondary_long_press_start.setter
    def on_secondary_long_press_start(self, handler):
        self.__on_secondary_long_press_start.subscribe(handler)
        self._set_attr(
            "onSecondaryLongPressStart", True if handler is not None else None
        )

    # on_secondary_long_press_end
    @property
    def on_secondary_long_press_end(self):
        return self.__on_secondary_long_press_end

    @on_secondary_long_press_end.setter
    def on_secondary_long_press_end(self, handler):
        self.__on_secondary_long_press_end.subscribe(handler)
        self._set_attr("onSecondaryLongPressEnd", True if handler is not None else None)

    # on_double_tap
    @property
    def on_double_tap(self):
        return self._get_event_handler("double_tap")

    @on_double_tap.setter
    def on_double_tap(self, handler):
        self._add_event_handler("double_tap", handler)
        self._set_attr("onDoubleTap", True if handler is not None else None)

    # on_double_tap_down
    @property
    def on_double_tap_down(self):
        return self.__on_double_tap_down

    @on_double_tap_down.setter
    def on_double_tap_down(self, handler):
        self.__on_double_tap_down.subscribe(handler)
        self._set_attr("onDoubleTapDown", True if handler is not None else None)


class TapEvent(ControlEvent):
    def __init__(self, lx, ly, gx, gy, kind) -> None:
        self.local_x: float = lx
        self.local_y: float = ly
        self.global_x: float = gx
        self.global_y: float = gy
        self.kind: str = kind


class LongPressStartEvent(ControlEvent):
    def __init__(self, lx, ly, gx, gy) -> None:
        self.local_x: float = lx
        self.local_y: float = ly
        self.global_x: float = gx
        self.global_y: float = gy


class LongPressEndEvent(ControlEvent):
    def __init__(self, lx, ly, gx, gy, vx, vy) -> None:
        self.local_x: float = lx
        self.local_y: float = ly
        self.global_x: float = gx
        self.global_y: float = gy
        self.velocity_x: float = vx
        self.velocity_y: float = vy
