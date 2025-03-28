from dataclasses import dataclass, field
from typing import Optional

from flet.core.alignment import Alignment
from flet.core.control import Control, control
from flet.core.control_event import ControlEvent
from flet.core.types import (
    ColorValue,
    OptionalEventCallable,
    OptionalNumber,
    WindowEventType,
)


@control("Window")
class Window(Control):
    bgcolor: Optional[ColorValue] = None
    width: OptionalNumber = None
    height: OptionalNumber = None
    top: OptionalNumber = None
    left: OptionalNumber = None
    max_width: OptionalNumber = None
    max_height: OptionalNumber = None
    min_width: OptionalNumber = None
    min_height: OptionalNumber = None
    opacity: OptionalNumber = None
    maximized: Optional[bool] = None
    minimized: Optional[bool] = None
    minimizable: Optional[bool] = None
    maximizable: Optional[bool] = None
    resizable: Optional[bool] = None
    movable: Optional[bool] = None
    full_screen: Optional[bool] = None
    always_on_top: Optional[bool] = None
    always_on_bottom: Optional[bool] = None
    prevent_close: Optional[bool] = None
    skip_task_bar: Optional[bool] = None
    title_bar_hidden: Optional[bool] = None
    title_bar_buttons_hidden: Optional[bool] = None
    frameless: Optional[bool] = None
    progress_bar: OptionalNumber = None
    focused: Optional[bool] = None
    visible: Optional[bool] = None
    shadow: Optional[bool] = None
    alignment: Optional[Alignment] = None
    badge_label: Optional[str] = None
    icon: Optional[str] = None
    ignore_mouse_events: Optional[bool] = None
    on_event: OptionalEventCallable["WindowEvent"] = None

    def __post_init__(self, ref) -> None:
        self._i = 2

    def wait_until_ready_to_show(self):
        self.invoke_method("wait_until_ready_to_show")

    def destroy(self):
        self.invoke_method("destroy")

    def center(self):
        self.invoke_method("center")

    def close(self):
        self.invoke_method("close")

    def to_front(self):
        self.invoke_method("to_front")


@dataclass
class WindowEvent(ControlEvent):
    type: WindowEventType
