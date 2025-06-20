import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import BaseControl, control
from flet.controls.control_event import Event, EventControlType, OptionalEventHandler
from flet.controls.types import (
    Brightness,
    Number,
    OptionalColorValue,
    OptionalNumber,
)

__all__ = ["Window", "WindowEvent", "WindowEventType", "WindowResizeEdge"]


class WindowEventType(Enum):
    CLOSE = "close"
    FOCUS = "focus"
    BLUR = "blur"
    HIDE = "hide"
    SHOW = "show"
    MAXIMIZE = "maximize"
    UNMAXIMIZE = "unmaximize"
    MINIMIZE = "minimize"
    RESTORE = "restore"
    RESIZE = "resize"
    RESIZED = "resized"
    MOVE = "move"
    MOVED = "moved"
    LEAVE_FULL_SCREEN = "leave-full-screen"
    ENTER_FULL_SCREEN = "enter-full-screen"


class WindowResizeEdge(Enum):
    TOP = "top"
    LEFT = "left"
    RIGHT = "right"
    BOTTOM = "bottom"
    TOP_LEFT = "topLeft"
    BOTTOM_LEFT = "bottomLeft"
    TOP_RIGHT = "topRight"
    BOTTOM_RIGHT = "bottomRight"


@dataclass
class WindowEvent(Event[EventControlType]):
    type: WindowEventType


# todo: raise FletExceptions when a method cant be called on the running platform


@control("Window")
class Window(BaseControl):
    """
    All properties and methods of the `Window` class are available only on Desktop 🖥️
    platforms.
    """

    bgcolor: OptionalColorValue = None
    """
    Sets background https://flet.dev/docs/reference/colors of an application window.

    Use together with `page.bgcolor` to make a window transparent.
    """

    width: OptionalNumber = None
    """
    Defines the width of the app window.
    """

    height: OptionalNumber = None
    """
    Defines the height of the app window.
    """

    top: OptionalNumber = None
    """
    Defines the vertical position of a native OS window - a distance in virtual
    pixels from the top edge of the screen.
    """

    left: OptionalNumber = None
    """
    Defines the horizontal position of the app window - a distance in virtual
    pixels from the left edge of the screen.
    """

    max_width: OptionalNumber = None
    """
    Defines the maximum width of the app window.
    """

    max_height: OptionalNumber = None
    """
    Defines the maximum height of the app window.
    """

    min_width: OptionalNumber = None
    """
    Defines the minimum width of the app window.
    """

    min_height: OptionalNumber = None
    """
    Defines the minimum height of the app window.
    """

    opacity: Number = 1.0
    """
    Defines the opacity of a native OS window.

    Value must be between `0.0` and `1.0`.
    """

    aspect_ratio: OptionalNumber = None
    """
    TBD
    """

    brightness: Optional[Brightness] = None
    """
    TBD
    """

    maximized: bool = False
    """
    Whether the app window is maximized. Set to `True` to maximize programmatically.
    """

    minimized: bool = False
    """
    Whether the app window is minimized. Set to `True` to minimize programmatically.
    """

    minimizable: bool = True
    """
    Whether the app window can be minimized through the window's "Minimize" button.
    """

    maximizable: bool = True
    """
    Whether to hide/disable native OS window's "Maximize" button.
    """

    resizable: bool = True
    """
    Whether the app window can be resized.
    """

    movable: bool = True
    """
    Whether the app window can be moved.

    Has effect on macOS only.
    """

    full_screen: bool = False
    """
    Whether to switch app's native OS window to a fullscreen mode.
    """

    always_on_top: bool = False
    """
    Whether the app window should always be displayed on top of other windows.
    """

    always_on_bottom: bool = False
    """
    Whether the app window should always be displayed below other windows.

    Has effect on Linux and Windows only.
    """

    prevent_close: bool = False
    """
    Set to `True` to intercept the native close signal. Could be used to implement
    app exit confirmation logic.
    """

    skip_task_bar: bool = False
    """
    Set to `True` to hide application from the Task Bar (Windows) or Dock (macOS).
    """

    title_bar_hidden: bool = False
    """
    Whether to hide the app window's title bar.
    """

    title_bar_buttons_hidden: bool = False
    """
    Whether to hide the app window's title bar buttons.

    Has effect on macOS only.
    """

    frameless: bool = False
    """
    Whether the app window should be frameless.
    """

    progress_bar: OptionalNumber = None
    """
    The value from `0.0` to `1.0` to display a progress bar on Task Bar or Dock.
    """

    focused: bool = True
    """
    Set to `True` to focus a native OS window.
    """

    visible: bool = True
    """
    Whether to make the app window visible. Used when the app starts hidden.
    """

    shadow: bool = True
    """
    Whether to display a shadow around the app window.
    """

    alignment: Optional[Alignment] = None
    """
    Defines the alignment of the app window.

    Value is of type https://flet.dev/docs/reference/types/alignment.
    """

    badge_label: Optional[str] = None
    """
    Sets a badge label on the app window.

    Has effect on macOS only.
    """

    icon: Optional[str] = None
    """
    The icon of the app window.

    Has effect on Windows only.
    """

    ignore_mouse_events: bool = False
    """
    Whether the app window should ignore mouse events, passing them to the window
    below it. If this window has focus, it will still receive keyboard events.
    """

    on_event: OptionalEventHandler[WindowEvent] = None
    """
    Fires when app window changes its state: position, size, maximized, minimized, etc.
    """

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

    async def start_dragging_async(self):
        await self._invoke_method_async("start_dragging")

    def start_dragging(self):
        asyncio.create_task(self.start_dragging_async())

    async def start_resizing_async(self, edge: WindowResizeEdge):
        await self._invoke_method_async("start_resizing", {"edge": edge})

    def start_resizing(self, edge: WindowResizeEdge):
        asyncio.create_task(self.start_resizing_async(edge))
