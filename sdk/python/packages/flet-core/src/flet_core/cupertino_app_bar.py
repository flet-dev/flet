from typing import Optional

from flet_core.border import Border
from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.types import PaddingValue


class CupertinoAppBar(Control):
    """
    An iOS-styled application bar.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.theme_mode = ft.ThemeMode.LIGHT

        page.appbar = ft.CupertinoAppBar(
            leading=ft.Icon(ft.icons.PALETTE),
            bgcolor=ft.colors.SURFACE_VARIANT,
            trailing=ft.Icon(ft.icons.WB_SUNNY_OUTLINED),
            middle=ft.Text("AppBar Example"),
        )
        page.add(ft.Text("Body!"))


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoappbar
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        leading: Optional[Control] = None,
        middle: Optional[Control] = None,
        automatically_imply_leading: Optional[bool] = None,
        automatically_imply_middle: Optional[bool] = None,
        border: Optional[Border] = None,
        padding: PaddingValue = None,
        trailing: Optional[Control] = None,
        transition_between_routes: Optional[bool] = None,
        previous_page_title: Optional[str] = None,
        bgcolor: Optional[str] = None,
    ):
        Control.__init__(self, ref=ref)

        self.__leading: Optional[Control] = None
        self.__middle: Optional[Control] = None
        self.__trailing: Optional[Control] = None

        self.leading = leading
        self.middle = middle
        self.automatically_imply_leading = automatically_imply_leading
        self.automatically_imply_middle = automatically_imply_middle
        self.border = border
        self.padding = padding
        self.trailing = trailing
        self.transition_between_routes = transition_between_routes
        self.previous_page_title = previous_page_title
        self.bgcolor = bgcolor

    def _get_control_name(self):
        return "cupertinoappbar"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("border", self.__border)
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__middle:
            self.__middle._set_attr_internal("n", "middle")
            children.append(self.__middle)
        if self.__trailing:
            self.__trailing._set_attr_internal("n", "trailing")
            children.append(self.__trailing)
        return children

    # leading
    @property
    def leading(self) -> Optional[Control]:
        return self.__leading

    @leading.setter
    def leading(self, value: Optional[Control]):
        """
        A Control to display before the toolbar's title.

        Typically the leading control is an Icon or an IconButton.
        """
        self.__leading = value

    # middle
    @property
    def middle(self) -> Optional[Control]:
        return self.__middle

    @middle.setter
    def middle(self, value: Optional[Control]):
        self.__middle = value

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # automatically_imply_leading
    @property
    def automatically_imply_leading(self) -> Optional[bool]:
        return self._get_attr(
            "automaticallyImplyLeading", data_type="bool", def_value=True
        )

    @automatically_imply_leading.setter
    def automatically_imply_leading(self, value: Optional[bool]):
        self._set_attr("automaticallyImplyLeading", value)

    # automatically_imply_middle
    @property
    def automatically_imply_middle(self) -> Optional[bool]:
        return self._get_attr(
            "automaticallyImplyMiddle", data_type="bool", def_value=True
        )

    @automatically_imply_middle.setter
    def automatically_imply_middle(self, value: Optional[bool]):
        self._set_attr("automaticallyImplyMiddle", value)

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    def border(self, value: Optional[Border]):
        self.__border = value

    # trailing
    @property
    def trailing(self) -> Optional[Control]:
        return self.__trailing

    @trailing.setter
    def trailing(self, value: Optional[Control]):
        self.__trailing = value

    # transition_between_routes
    @property
    def transition_between_routes(self) -> Optional[bool]:
        return self._get_attr(
            "transitionBetweenRoutes", data_type="bool", def_value=True
        )

    @transition_between_routes.setter
    def transition_between_routes(self, value: Optional[bool]):
        self._set_attr("transitionBetweenRoutes", value)

    # previous_page_title
    @property
    def previous_page_title(self):
        return self._get_attr("previousPageTitle")

    @previous_page_title.setter
    def previous_page_title(self, value):
        self._set_attr("previousPageTitle", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)
