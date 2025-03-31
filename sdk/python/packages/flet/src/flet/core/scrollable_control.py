import json
import time
from typing import Optional

from flet.core.animation import AnimationCurve
from flet.core.control import Control, OptionalNumber, control
from flet.core.control_event import ControlEvent
from flet.core.types import OptionalEventCallable, ScrollMode


@control(kw_only=True)
class ScrollableControl(Control):
    scroll: Optional[ScrollMode] = None
    auto_scroll: Optional[bool] = None
    reverse: Optional[bool] = None
    on_scroll_interval: OptionalNumber = None
    on_scroll: OptionalEventCallable["OnScrollEvent"] = None

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


class OnScrollEvent(ControlEvent):
    event_type: str
    pixels: float
    min_scroll_extent: float
    max_scroll_extent: float
    viewport_dimension: float
    scroll_delta: Optional[float]
    direction: Optional[str]
    overscroll: Optional[float]
    velocity: Optional[float]
