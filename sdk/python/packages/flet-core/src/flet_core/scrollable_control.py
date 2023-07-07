import json
import time
from typing import Any, Optional

from flet_core.animation import AnimationCurve
from flet_core.control import Control, OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.event_handler import EventHandler
from flet_core.types import ScrollMode, ScrollModeString


class ScrollableControl(Control):
    def __init__(
        self,
        scroll: Optional[ScrollMode] = None,
        auto_scroll: Optional[bool] = None,
        on_scroll_interval: OptionalNumber = None,
        on_scroll: Any = None,
    ):
        def convert_on_scroll_event_data(e):
            d = json.loads(e.data)
            return OnScrollEvent(**d)

        self.__on_scroll = EventHandler(convert_on_scroll_event_data)
        self._add_event_handler("onScroll", self.__on_scroll.get_handler())

        self.scroll = scroll
        self.auto_scroll = auto_scroll
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

    async def scroll_to_async(
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
        await self.update_async()

    # scroll
    @property
    def scroll(self) -> Optional[ScrollMode]:
        return self.__scroll

    @scroll.setter
    def scroll(self, value: Optional[ScrollMode]):
        self.__scroll = value
        if isinstance(value, ScrollMode):
            self._set_attr("scroll", value.value)
        else:
            self.__set_scroll(value)

    def __set_scroll(self, value: Optional[ScrollModeString]):
        if value is True:
            value = "auto"
        elif value is False:
            value = None
        self._set_attr("scroll", value)

    # auto_scroll
    @property
    def auto_scroll(self) -> Optional[bool]:
        return self._get_attr("autoScroll")

    @auto_scroll.setter
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoScroll", value)

    # on_scroll_interval
    @property
    def on_scroll_interval(self) -> OptionalNumber:
        return self._get_attr("onScrollInterval")

    @on_scroll_interval.setter
    def on_scroll_interval(self, value: OptionalNumber):
        self._set_attr("onScrollInterval", value)

    # on_scroll
    @property
    def on_scroll(self):
        return self.__on_scroll

    @on_scroll.setter
    def on_scroll(self, handler):
        self.__on_scroll.subscribe(handler)
        self._set_attr("onScroll", True if handler is not None else None)


class OnScrollEvent(ControlEvent):
    def __init__(
        self, t, p, minse, maxse, vd, sd=None, dir=None, os=None, v=None
    ) -> None:
        self.event_type: str = t
        self.pixels: float = p
        self.min_scroll_extent: float = minse
        self.max_scroll_extent: float = maxse
        self.viewport_dimension: float = vd
        self.scroll_delta: Optional[float] = sd
        self.direction: Optional[str] = dir
        self.overscroll: Optional[float] = os
        self.velocity: Optional[float] = v

    def __str__(self):
        attrs = {}
        return f"{self.event_type}: pixels={self.pixels}, min_scroll_extent={self.min_scroll_extent}, max_scroll_extent={self.max_scroll_extent}, viewport_dimension={self.viewport_dimension}, scroll_delta={self.scroll_delta}, direction={self.direction}, overscroll={self.overscroll}, velocity={self.velocity}"
