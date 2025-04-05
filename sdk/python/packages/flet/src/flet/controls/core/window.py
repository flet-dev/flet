import asyncio
from dataclasses import dataclass
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.control import BaseControl, control
from flet.controls.control_event import ControlEvent
from flet.controls.types import (
    Number,
    OptionalColorValue,
    OptionalEventCallable,
    OptionalNumber,
    WindowEventType,
)

__all__ = ["Window", "WindowEvent"]


@control("Window")
class Window(BaseControl):
    bgcolor: OptionalColorValue = None
    width: OptionalNumber = None
    height: OptionalNumber = None
    top: OptionalNumber = None
    left: OptionalNumber = None
    max_width: OptionalNumber = None
    max_height: OptionalNumber = None
    min_width: OptionalNumber = None
    min_height: OptionalNumber = None
    opacity: Number = 1.0
    maximized: bool = False
    minimized: bool = False
    minimizable: bool = True
    maximizable: bool = True
    resizable: bool = True
    movable: bool = True
    full_screen: bool = False
    always_on_top: bool = False
    always_on_bottom: bool = False
    prevent_close: bool = False
    skip_task_bar: bool = False
    title_bar_hidden: bool = False
    title_bar_buttons_hidden: bool = False
    frameless: bool = False
    progress_bar: OptionalNumber = None
    focused: bool = True
    visible: bool = True
    shadow: bool = False
    alignment: Optional[Alignment] = None
    badge_label: Optional[str] = None
    icon: Optional[str] = None
    ignore_mouse_events: bool = False
    on_event: OptionalEventCallable["WindowEvent"] = None

    def __post_init__(self, ref) -> None:
        super().__post_init__(ref)
        self._i = 2

    async def wait_until_ready_to_show_async(self):
        await self._invoke_method_async("wait_until_ready_to_show")

    def wait_until_ready_to_show(self):
        asyncio.create_task(self.wait_until_ready_to_show_async())

    async def destroy_async(self):
        await self._invoke_method_async("destroy")

    def destroy(self):
        asyncio.create_task(self.destroy_async())

    async def center_async(self):
        await self._invoke_method_async("center")

    def center(self):
        asyncio.create_task(self.center_async())

    async def close_async(self):
        await self._invoke_method_async("close")

    def close(self):
        asyncio.create_task(self.close_async())

    async def to_front_async(self):
        await self._invoke_method_async("to_front")

    def to_front(self):
        asyncio.create_task(self.to_front_async())


@dataclass
class WindowEvent(ControlEvent):
    type: WindowEventType
