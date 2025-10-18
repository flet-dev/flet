from dataclasses import dataclass
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import BaseControl, control
from flet.controls.control_event import Event, EventControlType, EventHandler
from flet.controls.types import (
    Brightness,
    ColorValue,
    Number,
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


# TODO: raise FletExceptions when a method cant be called on the running platform
@control("Window")
class Window(BaseControl):
    """
    Controls the app window.

    Limitation:
        This control is for Desktop platforms (macOS, Windows, Linux) only.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Sets background color of an application window.

    Tip:
        Can be used together with [`Page.bgcolor`][flet.] to make
        a window transparent.
    """

    width: Optional[Number] = None
    """
    Defines the width of the app window.
    """

    height: Optional[Number] = None
    """
    Defines the height of the app window.
    """

    top: Optional[Number] = None
    """
    Defines the vertical position of a native OS window - a distance in virtual
    pixels from the top edge of the screen.
    """

    left: Optional[Number] = None
    """
    Defines the horizontal position of the app window - a distance in virtual
    pixels from the left edge of the screen.
    """

    max_width: Optional[Number] = None
    """
    Defines the maximum width of the app window.
    """

    max_height: Optional[Number] = None
    """
    Defines the maximum height of the app window.
    """

    min_width: Optional[Number] = None
    """
    Defines the minimum width of the app window.
    """

    min_height: Optional[Number] = None
    """
    Defines the minimum height of the app window.
    """

    opacity: Number = 1.0
    """
    Defines the opacity of the app window.

    Raises:
        ValueError: If it is not between `0.0` and `1.0` inclusive.
    """

    aspect_ratio: Optional[Number] = None
    """
    Defines the aspect ratio of the app window.
    """

    brightness: Optional[Brightness] = None
    """
    The brightness of a app window.
    """

    maximized: bool = False
    """
    Whether the app window is maximized.

    Set to `True` to maximize programmatically.
    """

    minimized: bool = False
    """
    Whether the app window is minimized.

    Set to `True` to minimize programmatically.
    """

    minimizable: bool = True
    """
    Whether the app window can be minimized through the window's "Minimize" button.
    """

    maximizable: bool = True
    """
    Whether to hide/disable app window's "Maximize" button.
    """

    resizable: bool = True
    """
    Whether the app window can be resized.
    """

    movable: bool = True
    """
    Whether the app window can be moved.

    Limitation:
        Has effect on macOS only.
    """

    full_screen: bool = False
    """
    Whether to switch the app's window to fullscreen mode.
    """

    always_on_top: bool = False
    """
    Whether the app window should always be displayed on top of other windows/apps.
    """

    always_on_bottom: bool = False
    """
    Whether the app window should always be displayed below other windows.

    Limitation:
        Has effect on Linux and Windows only.
    """

    prevent_close: bool = False
    """
    Set to `True` to intercept the native close signal.

    Could be used to implement app exit confirmation logic.
    """

    skip_task_bar: bool = False
    """
    Whether the app window should be hidden from the Task Bar (on Windows)
    or Dock (on macOS).
    """

    title_bar_hidden: bool = False
    """
    Whether to hide the app window's title bar.
    """

    title_bar_buttons_hidden: bool = False
    """
    Whether to hide the app window's title bar buttons.

    Limitation:
        Has effect on macOS only.
    """

    frameless: bool = False
    """
    Whether the app window should be frameless.
    """

    progress_bar: Optional[Number] = None
    """
    The value from `0.0` to `1.0` to display a progress bar on Task Bar or Dock.
    """

    focused: bool = True
    """
    Whether the app window should be focused.

    Set to `True` to focus programmatically.
    """

    visible: bool = True
    """
    Whether to make the app window visible.

    Can be of use when the app starts as hidden.
    """

    shadow: bool = True
    """
    Whether to display a shadow around the app window.
    """

    alignment: Optional[Alignment] = None
    """
    Defines the alignment of the app window.
    """

    badge_label: Optional[str] = None
    """
    Sets a badge label on the app window.

    Limitation:
        Has effect on macOS only.
    """

    icon: Optional[str] = None
    """
    The icon of the app window.

    The file should have the `.ico` extension.

    Limitation:
        Has effect on Windows only.
    """

    ignore_mouse_events: bool = False
    """
    Whether the app window should ignore mouse events, passing them to the window
    below it. If this window has focus, it will still receive keyboard events.
    """

    on_event: Optional[EventHandler[WindowEvent]] = None
    """
    Called when app window changes its state.
    For example, when the window is maximized or minimized.
    """

    def __post_init__(self, ref) -> None:
        super().__post_init__(ref)
        self._i = 2
        if self.opacity < 0.0 or self.opacity > 1.0:
            raise ValueError(
                f"opacity must be between 0.0 and 1.0 inclusive, got {self.opacity}"
            )

    async def wait_until_ready_to_show(self):
        """
        Waits until the app window is ready to show.
        """
        await self._invoke_method("wait_until_ready_to_show")

    async def destroy(self):
        """
        Destroys the app window.
        """
        await self._invoke_method("destroy")

    async def center(self):
        """
        Centers the app window.
        """
        await self._invoke_method("center")

    async def close(self):
        await self._invoke_method("close")

    async def to_front(self):
        """
        Brings the app window to the front.
        """
        await self._invoke_method("to_front")

    async def start_dragging(self):
        """
        Starts dragging the app window.
        """
        await self._invoke_method("start_dragging")

    async def start_resizing(self, edge: WindowResizeEdge):
        """
        Starts resizing the app window.
        """
        await self._invoke_method("start_resizing", {"edge": edge})
