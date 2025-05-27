from typing import Any

from flet.controls.control import Control
from flet.controls.core.gesture_detector import (
    DragStartEvent,
    GestureDetector,
    TapEvent,
)
from flet.controls.types import OptionalEventCallable


class WindowDragArea(GestureDetector):
    """
    A control for drag to move, maximize and restore application window.

    When you have hidden the title bar with `page.window_title_bar_hidden`, you can add 
    this control to move the window position.

    Online docs: https://flet.dev/docs/controls/windowdragarea
    """

    def __init__(
        self,
        content: Control,
        maximizable: bool = True,
        on_double_tap: OptionalEventCallable["TapEvent"] = None,
        on_pan_start: OptionalEventCallable["DragStartEvent"] = None,
        **kwargs: Any,
    ):
        GestureDetector.__init__(
            self,
            content=content,
            on_double_tap=self.handle_double_tap,
            on_pan_start=self.handle_pan_start,
            **kwargs,
        )

        self.maximizable = maximizable
        self.on_double_tap = on_double_tap
        self.on_pan_start = on_pan_start

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"

    def handle_double_tap(self, e: TapEvent):
        if self.maximizable and self.page.window.maximizable:
            if not self.page.window.maximized:
                self.page.window.maximized = True
            else:
                self.page.window.maximized = False
            self.page.update()

        if self.on_double_tap is not None and self.page.window.maximized:
            self.on_double_tap(e)

    def handle_pan_start(self, e: DragStartEvent):
        self.page.window.start_dragging()
        if self.on_pan_start is not None:
            self.on_pan_start(e)
