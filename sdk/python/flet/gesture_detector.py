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
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.__on_tap_down = EventHandler(lambda e: TapDownEvent(**json.loads(e.data)))
        self._add_event_handler("tap_down", self.__on_tap_down.handler)

        self.content = content
        self.on_tap = on_tap
        self.on_tap_down = on_tap_down

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


class TapDownEvent(ControlEvent):
    def __init__(self, lx, ly, gx, gy, kind) -> None:
        self.local_x: float = lx
        self.local_y: float = ly
        self.global_x: float = gx
        self.global_y: float = gy
        self.kind: str = kind
