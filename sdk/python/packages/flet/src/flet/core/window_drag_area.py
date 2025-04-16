from typing import Any

from flet.core.control import Control
from flet.core.gesture_detector import DragStartEvent, GestureDetector, TapEvent
from flet.core.types import OptionalEventCallable


class WindowDragArea(GestureDetector):
    """
    A control for drag to move, maximize and restore application window.

    When you have hidden the title bar with `page.window_title_bar_hidden`, you can add this control to move the window position.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.window_title_bar_hidden = True
        page.window_title_bar_buttons_hidden = True

        page.add(
            ft.Row(
                [
                    ft.WindowDragArea(ft.Container(ft.Text("Drag this area to move, maximize and restore application window."), bgcolor=ft.colors.AMBER_300, padding=10), expand=True),
                    ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close())
                ]
            )
        )

    ft.app(target=main)
    ```

    -----

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
