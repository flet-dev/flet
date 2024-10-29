from typing import Any, Optional

from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.types import ColorEnums, ColorValue


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

    def __init__(
        self,
        width: OptionalNumber = None,
        thickness: OptionalNumber = None,
        color: Optional[ColorValue] = None,
        leading_indent: OptionalNumber = None,
        trailing_indent: OptionalNumber = None,
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

        self.width = width
        self.thickness = thickness
        self.color = color
        self.leading_indent = leading_indent
        self.trailing_indent = trailing_indent

    def _get_control_name(self):
        return "verticaldivider"

    # width
    @property
    def width(self) -> OptionalNumber:
        return self._get_attr("width", data_type="float")

    @width.setter
    def width(self, value: OptionalNumber):
        assert value is None or value >= 0, "width cannot be negative"
        self._set_attr("width", value)

    # thickness
    @property
    def thickness(self) -> OptionalNumber:
        return self._get_attr("thickness", data_type="float")

    @thickness.setter
    def thickness(self, value: OptionalNumber):
        assert value is None or value >= 0, "thickness cannot be negative"
        self._set_attr("thickness", value)

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # leading_indent
    @property
    def leading_indent(self) -> OptionalNumber:
        return self._get_attr("leadingIndent", data_type="float")

    @leading_indent.setter
    def leading_indent(self, value: OptionalNumber):
        assert value is None or value >= 0, "leading_indent cannot be negative"
        self._set_attr("leadingIndent", value)

    # trailing_indent
    @property
    def trailing_indent(self) -> OptionalNumber:
        return self._get_attr("trailingIndent", data_type="float")

    @trailing_indent.setter
    def trailing_indent(self, value: OptionalNumber):
        assert value is None or value >= 0, "trailing_indent cannot be negative"
        self._set_attr("trailingIndent", value)
