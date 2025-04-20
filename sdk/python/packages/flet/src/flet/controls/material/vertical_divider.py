from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.types import OptionalColorValue, OptionalNumber

__all__ = ["VerticalDivider"]


@control("VerticalDivider")
class VerticalDivider(Control):
    """
    A thin vertical line, with padding on either side.

    In the material design language, this represents a divider.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):

        page.add(
            ft.Row(
                [
                    ft.Container(
                        bgcolor=ft.colors.ORANGE_300,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                    ft.VerticalDivider(),
                    ft.Container(
                        bgcolor=ft.colors.BROWN_400,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/verticaldivider
    """

    width: OptionalNumber = None
    thickness: OptionalNumber = None
    color: OptionalColorValue = None
    leading_indent: OptionalNumber = None
    trailing_indent: OptionalNumber = None

    def before_update(self):
        super().before_update()
        assert (
            self.width is None or self.width >= 0
        ), "width must be greater than or equal to 0"
        assert (
            self.thickness is None or self.thickness >= 0
        ), "thickness must be greater than or equal to 0"
        assert (
            self.leading_indent is None or self.leading_indent >= 0
        ), "leading_indent must be greater than or equal to 0"
        assert (
            self.trailing_indent is None or self.trailing_indent >= 0
        ), "trailing_indent must be greater than or equal to 0"
