from typing import Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import (
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["CircleAvatar"]


@control("CircleAvatar")
class CircleAvatar(ConstrainedControl):
    """
    A circle that represents a user.

    If `foreground_image_src` fails then `background_image_src` is used. If `background_image_src` fails too,
    then `bgcolor` is used.

    Example:
    ```
    import flet as ft

    def main(page):
        # a "normal" avatar with background image
        a1 = ft.CircleAvatar(
            foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
            content=ft.Text("FF"),
        )
        # avatar with failing foreground image and fallback text
        a2 = ft.CircleAvatar(
            foreground_image_src="https://avatars.githubusercontent.com/u/_5041459?s=88&v=4",
            content=ft.Text("FF"),
        )
        # avatar with icon, aka icon with inverse background
        a3 = ft.CircleAvatar(
            content=ft.Icon(ft.icons.ABC),
        )
        # avatar with icon and custom colors
        a4 = ft.CircleAvatar(
            content=ft.Icon(ft.icons.WARNING_ROUNDED),
            color=ft.colors.YELLOW_200,
            bgcolor=ft.colors.AMBER_700,
        )
        # avatar with online status
        a5 = ft.Stack(
            [
                ft.CircleAvatar(
                    foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
                ),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.colors.GREEN, radius=5),
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=40,
            height=40,
        )
        page.add(a1, a2, a3, a4, a5)


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/circleavatar
    """

    content: Optional[Control] = None
    foreground_image_src: Optional[str] = None
    background_image_src: Optional[str] = None
    color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    radius: OptionalNumber = None
    min_radius: OptionalNumber = None
    max_radius: OptionalNumber = None
    on_image_error: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.min_radius is None or self.min_radius >= 0
        ), "min_radius cannot be negative"
        assert (
            self.max_radius is None or self.max_radius >= 0
        ), "max_radius cannot be negative"
