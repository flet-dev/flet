from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import EventHandler
from flet.controls.core.window import WindowEvent
from flet.controls.events import DragEndEvent, DragStartEvent
from flet.controls.layout_control import LayoutControl


@control("WindowDragArea")
class WindowDragArea(LayoutControl):
    """
    It mimics the behavior (drag, move, maximize, restore) of a native OS window
    title bar on the [`content`][(c).] control.
    """

    content: Control
    """
    The content of this drag area.

    Must be visible.

    Raises:
        ValueError: If [`content`][(c).] is not visible.
    """

    maximizable: bool = True
    """
    Whether double-clicking on the `WindowDragArea` should maximize/maximize the app's
    window.
    """

    on_double_tap: Optional[EventHandler[WindowEvent["WindowDragArea"]]] = None
    """
    Called when the `WindowDragArea` is double-tapped and `maximizable=True`.

    Info:
        When a double-tap event is fired, the [`type`][flet.WindowEvent.]
        property of the event handler argument can only be one of the following:
        `WindowEventType.MAXIMIZE`, `WindowEventType.UNMAXIMIZE`.
    """

    on_drag_start: Optional[EventHandler[DragStartEvent["WindowDragArea"]]] = None
    """
    Called when a pointer has contacted the screen and has begun to move/drag.
    """

    on_drag_end: Optional[EventHandler[DragEndEvent["WindowDragArea"]]] = None
    """
    Called when a pointer that was previously in contact with the screen and
    moving/dragging is no longer in contact with the screen.
    """

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
