from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


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

    def __init__(
        self,
        height: OptionalNumber = None,
        thickness: OptionalNumber = None,
        color: Optional[str] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        opacity: OptionalNumber = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
            visible=visible,
            data=data,
        )

        self.height = height
        self.thickness = thickness
        self.color = color

    def _get_control_name(self):
        return "divider"

    # height
    @property
    def height(self) -> OptionalNumber:
        return self._get_attr("height")

    @height.setter
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)

    # thickness
    @property
    def thickness(self) -> OptionalNumber:
        return self._get_attr("thickness")

    @thickness.setter
    def thickness(self, value: OptionalNumber):
        self._set_attr("thickness", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)
