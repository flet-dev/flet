from typing import Optional

from flet.core.animation import AnimationStyle
from flet.core.box import BoxConstraints
from flet.core.buttons import OutlinedBorder
from flet.core.control import Control, OptionalNumber, control
from flet.core.types import ClipBehavior, ColorValue, OptionalControlEventCallable


@control("BottomSheet")
class BottomSheet(Control):
    """
    A modal bottom sheet is an alternative to a menu or a dialog and prevents the user from interacting with the rest of the app.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def handle_dismissal(e):
            page.add(ft.Text("Bottom sheet dismissed"))
        bs = ft.BottomSheet(
            on_dismiss=handle_dismissal,
            content=ft.Container(
                padding=50,
                content=ft.Column(
                    tight=True,
                    controls=[
                        ft.Text("This is bottom sheet's content!"),
                        ft.ElevatedButton("Close bottom sheet", on_click=lambda _: page.close(bs)),
                    ],
                ),
            ),
        )
        page.add(ft.ElevatedButton("Display bottom sheet", on_click=lambda _: page.open(bs)))


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/bottomsheet
    """

    content: Control
    open: bool = False
    elevation: OptionalNumber = None
    bgcolor: Optional[ColorValue] = None
    dismissible: Optional[bool] = None
    enable_drag: Optional[bool] = None
    show_drag_handle: Optional[bool] = None
    use_safe_area: Optional[bool] = None
    is_scroll_controlled: Optional[bool] = None
    maintain_bottom_view_insets_padding: Optional[bool] = None
    animation_style: Optional[AnimationStyle] = None
    size_constraints: Optional[BoxConstraints] = None
    clip_behavior: Optional[ClipBehavior] = None
    shape: Optional[OutlinedBorder] = None
    on_dismiss: OptionalControlEventCallable = None

    def before_update(
        self,
    ):
        super().before_update()
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
