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
                        bgcolor=ft.Colors.AMBER,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                    ft.Divider(),
                    ft.Container(bgcolor=ft.Colors.PINK, alignment=ft.alignment.center, expand=True),
                    ft.Divider(height=1, color="white"),
                    ft.Container(
                        bgcolor=ft.Colors.BLUE_300,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                    ft.Divider(height=9, thickness=3),
                    ft.Container(
                        bgcolor=ft.Colors.DEEP_PURPLE_200,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
        )

    ft.app(main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/divider
    """

    color: Optional[ColorValue] = None
    """The color to use when painting the line."""

    height: OptionalNumber = field(default=16.0)
    """
    The divider's height extent. The divider itself is always drawn as a horizontal line that is centered
    within the height specified by this value.

    Defaults to `16.0`.
    """

    leading_indent: OptionalNumber = field(default=0.0)
    """
    The amount of empty space to the leading edge of the divider.

    Defaults to `0.0`.
    """

    thickness: OptionalNumber = field(default=0.0)
    """
    The thickness of the line drawn within the divider. A divider with a thickness of `0.0` is always drawn
    as a line with a height of exactly one device pixel.

    Defaults to `0.0`.
    """

    trailing_indent: OptionalNumber = field(default=0.0)
    """
    The amount of empty space to the trailing edge of the divider.

    Defaults to `0.0`.
    """

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
