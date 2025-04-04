from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control

__all__ = ["WindowDragArea"]


@control("WindowDragArea")
class WindowDragArea(ConstrainedControl):
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

    content: Control
    maximizable: bool = True

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
