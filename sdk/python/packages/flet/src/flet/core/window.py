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


@control("window")
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
    opacity: OptionalNumber = field(default=1.0)
    maximized: Optional[bool] = field(default=False)
    minimized: Optional[bool] = field(default=False)
    minimizable: Optional[bool] = field(default=True)
    maximizable: Optional[bool] = field(default=True)
    resizable: Optional[bool] = field(default=True)
    movable: Optional[bool] = field(default=True)
    full_screen: Optional[bool] = field(default=False)
    always_on_top: Optional[bool] = field(default=False)
    prevent_close: Optional[bool] = field(default=False)
    title_bar_hidden: Optional[bool] = field(default=False)
    title_bar_buttons_hidden: Optional[bool] = field(default=False)
    skip_task_bar: Optional[bool] = field(default=False)
    frameless: Optional[bool] = field(default=False)
    progress_bar: OptionalNumber = None
    focused: Optional[bool] = field(default=True)
    visible: Optional[bool] = field(default=True)
    always_on_bottom: Optional[bool] = field(default=False)
    shadow: Optional[bool] = field(default=False)
    alignment: Optional[Alignment] = None
    badge_label: Optional[str] = None
    icon: Optional[str] = None
    ignore_mouse_events: Optional[bool] = field(default=False)
    on_event: OptionalEventCallable["WindowEvent"] = None

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
