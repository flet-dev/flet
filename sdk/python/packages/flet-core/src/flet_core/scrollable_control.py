import json
import time
from typing import Optional, Callable

from flet_core.animation import AnimationCurve
from flet_core.control import Control, OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.event_handler import EventHandler
from flet_core.types import ScrollMode
from flet_core.utils import deprecated


class ScrollableControl(Control):
    def __init__(
        self,
        scroll: Optional[ScrollMode] = None,
        auto_scroll: Optional[bool] = None,
        reverse: Optional[bool] = None,
        on_scroll_interval: OptionalNumber = None,
        on_scroll: Optional[Callable[["OnScrollEvent"], None]] = None,
    ):
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

    @deprecated(
        reason="Use scroll_to() method instead.",
        version="0.21.0",
        delete_version="0.26.0",
    )
    async def scroll_to_async(
        self,
        offset: Optional[float] = None,
        delta: Optional[float] = None,
        key: Optional[str] = None,
        duration: Optional[int] = None,
        curve: Optional[AnimationCurve] = None,
    ):
        self.scroll_to(offset, delta, key, duration, curve)

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
    def auto_scroll(self) -> Optional[str]:
        return self._get_attr("autoScroll", data_type="bool", def_value=False)

    @auto_scroll.setter
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoScroll", value)

    # reverse
    @property
    def reverse(self) -> Optional[bool]:
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
    def on_scroll(self):
        return self.__on_scroll

    @on_scroll.setter
    def on_scroll(self, handler: Optional[Callable[["OnScrollEvent"], None]]):
        self.__on_scroll.subscribe(handler)
        self._set_attr("onScroll", True if handler is not None else None)


class OnScrollEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.event_type: str = d["t"]
        self.pixels: float = d["p"]
        self.min_scroll_extent: float = d["minse"]
        self.max_scroll_extent: float = d["maxse"]
        self.viewport_dimension: float = d["vd"]
        self.scroll_delta: Optional[float] = d["sd"]
        self.direction: Optional[str] = d["dir"]
        self.overscroll: Optional[float] = d["os"]
        self.velocity: Optional[float] = d["v"]

    def __str__(self):
        return f"{self.event_type}: pixels={self.pixels}, min_scroll_extent={self.min_scroll_extent}, max_scroll_extent={self.max_scroll_extent}, viewport_dimension={self.viewport_dimension}, scroll_delta={self.scroll_delta}, direction={self.direction}, overscroll={self.overscroll}, velocity={self.velocity}"
