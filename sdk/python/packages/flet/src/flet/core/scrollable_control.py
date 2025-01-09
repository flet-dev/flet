import json
import time
from typing import Optional

from flet.core.animation import AnimationCurve
from flet.core.control import Control, OptionalNumber
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.types import OptionalEventCallable, ScrollMode


class ScrollableControl(Control):
    def __init__(
        self,
        scroll: Optional[ScrollMode] = None,
        auto_scroll: Optional[bool] = None,
        reverse: Optional[bool] = None,
        on_scroll_interval: OptionalNumber = None,
        on_scroll: OptionalEventCallable["OnScrollEvent"] = None,
    ):
        super().__init__()
        self.__on_scroll = EventHandler(lambda e: OnScrollEvent(e))
        self._add_event_handler("onScroll", self.__on_scroll.get_handler())

        self.scroll = scroll
        self.auto_scroll = auto_scroll
        self.reverse = reverse
        self.on_scroll_interval = on_scroll_interval
        self.on_scroll = on_scroll

    def scroll_to(
        self,
        offset: Optional[float] = None,
        delta: Optional[float] = None,
        key: Optional[str] = None,
        duration: Optional[int] = None,
        curve: Optional[AnimationCurve] = None,
    ):
        m = {
            "n": "scroll_to",
            "i": str(time.time()),
            "p": {
                "offset": offset,
                "delta": delta,
                "key": key,
                "duration": duration,
                "curve": curve.value if curve is not None else None,
            },
        }
        self._set_attr_json("method", m)
        self.update()

    # scroll
    @property
    def scroll(self) -> Optional[ScrollMode]:
        return self.__scroll

    @scroll.setter
    def scroll(self, value: Optional[ScrollMode]):
        self.__scroll = value
        self._set_attr(
            "scroll",
            value.value
            if isinstance(value, ScrollMode)
            else "auto"
            if value is True
            else None
            if value is False
            else value,
        )

    # auto_scroll
    @property
    def auto_scroll(self) -> bool:
        return self._get_attr("autoScroll", data_type="bool", def_value=False)

    @auto_scroll.setter
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoScroll", value)

    # reverse
    @property
    def reverse(self) -> bool:
        return self._get_attr("reverse", data_type="bool", def_value=False)

    @reverse.setter
    def reverse(self, value: Optional[bool]):
        self._set_attr("reverse", value)

    # on_scroll_interval
    @property
    def on_scroll_interval(self) -> OptionalNumber:
        return self._get_attr("onScrollInterval")

    @on_scroll_interval.setter
    def on_scroll_interval(self, value: OptionalNumber):
        self._set_attr("onScrollInterval", value)

    # on_scroll
    @property
    def on_scroll(self) -> OptionalEventCallable["OnScrollEvent"]:
        return self.__on_scroll.handler

    @on_scroll.setter
    def on_scroll(self, handler: OptionalEventCallable["OnScrollEvent"]):
        self.__on_scroll.handler = handler
        self._set_attr("onScroll", True if handler is not None else None)


class OnScrollEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.event_type: str = d.get("t")
        self.pixels: float = d.get("p")
        self.min_scroll_extent: float = d.get("minse")
        self.max_scroll_extent: float = d.get("maxse")
        self.viewport_dimension: float = d.get("vd")
        self.scroll_delta: Optional[float] = d.get("sd")
        self.direction: Optional[str] = d.get("dir")
        self.overscroll: Optional[float] = d.get("os")
        self.velocity: Optional[float] = d.get("v")
