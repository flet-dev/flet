import asyncio
from dataclasses import dataclass, field
from typing import Optional

from flet.core.alignment import Alignment
from flet.core.control import BaseControl, control
from flet.core.control_event import ControlEvent
from flet.core.types import (
    ColorValue,
    Number,
    OptionalEventCallable,
    OptionalNumber,
    WindowEventType,
)

__all__ = ["Window", "WindowEvent"]


@control("Window")
class Window(BaseControl):
    bgcolor: Optional[ColorValue] = None
    width: OptionalNumber = None
    height: OptionalNumber = None
    top: OptionalNumber = None
    left: OptionalNumber = None
    max_width: OptionalNumber = None
    max_height: OptionalNumber = None
    min_width: OptionalNumber = None
    min_height: OptionalNumber = None
    opacity: Number = field(default=1.0)
    maximized: bool = field(default=False)
    minimized: bool = field(default=False)
    minimizable: bool = field(default=True)
    maximizable: bool = field(default=True)
    resizable: bool = field(default=True)
    movable: bool = field(default=True)
    full_screen: bool = field(default=False)
    always_on_top: bool = field(default=False)
    always_on_bottom: bool = field(default=False)
    prevent_close: bool = field(default=False)
    skip_task_bar: bool = field(default=False)
    title_bar_hidden: bool = field(default=False)
    title_bar_buttons_hidden: bool = field(default=False)
    frameless: bool = field(default=False)
    progress_bar: OptionalNumber = None
    focused: bool = field(default=True)
    visible: bool = field(default=True)
    shadow: bool = field(default=False)
    alignment: Optional[Alignment] = None
    badge_label: Optional[str] = None
    icon: Optional[str] = None
    ignore_mouse_events: bool = field(default=False)
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
