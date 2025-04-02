from dataclasses import field
from typing import Optional

from flet.core.control import Control, control
from flet.core.types import ColorValue, OptionalNumber

__all__ = ["Divider"]


@control("Divider")
class Divider(Control):
    """
    A thin horizontal line, with padding on either side.

    In the material design language, this represents a divider.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):

        page.add(
            ft.Column(
                [
                    ft.Container(
                        bgcolor=ft.colors.AMBER,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                    ft.Divider(),
                    ft.Container(
                        bgcolor=ft.colors.PINK, alignment=ft.alignment.center, expand=True
                    ),
                ],
                spacing=0,
                expand=True,
            ),
        )


    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/divider
    """

    height: OptionalNumber = field(default=16.0)
    thickness: OptionalNumber = field(default=0.0)
    color: Optional[ColorValue] = None
    leading_indent: OptionalNumber = field(default=0.0)
    trailing_indent: OptionalNumber = field(default=0.0)

    def before_update(self):
        super().before_update()
        assert self.height is None or self.height >= 0, "height cannot be negative"
        assert (
            self.thickness is None or self.thickness >= 0
        ), "thickness cannot be negative"
        assert (
            self.leading_indent is None or self.leading_indent >= 0
        ), "leading_indent cannot be negative"
        assert (
            self.trailing_indent is None or self.trailing_indent >= 0
        ), "trailing_indent cannot be negative"
