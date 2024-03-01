from typing import Any, List, Optional

from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.types import PaddingValue


class Banner(Control):
    """
    A banner displays an important, succinct message, and provides actions for users to address (or dismiss the banner). A user action is required for it to be dismissed.

    Banners are displayed at the top of the screen, below a top app bar. They are persistent and non-modal, allowing the user to either ignore them or interact with them at any time.

    Example:
    ```
    import flet as ft

    def main(page):
        def close_banner(e):
            page.banner.open = False
            page.update()

        page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                "Oops, there were some errors while trying to delete the file. What would you like me to do?"
            ),
            actions=[
                ft.TextButton("Retry", on_click=close_banner),
                ft.TextButton("Ignore", on_click=close_banner),
                ft.TextButton("Cancel", on_click=close_banner),
            ],
        )

        def show_banner_click(e):
            page.banner.open = True
            page.update()

        page.add(ft.ElevatedButton("Show Banner", on_click=show_banner_click))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/banner
    """

    def __init__(
        self,
        open: bool = False,
        leading: Optional[Control] = None,
        leading_padding: Optional[PaddingValue] = None,
        content: Optional[Control] = None,
        content_padding: Optional[PaddingValue] = None,
        actions: Optional[List[Control]] = None,
        force_actions_below: Optional[bool] = None,
        bgcolor: Optional[str] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.__leading: Optional[Control] = None
        self.__content: Optional[Control] = None
        self.__actions = []

        self.open = open
        self.leading = leading
        self.leading_padding = leading_padding
        self.content = content
        self.content_padding = content_padding
        self.actions = actions
        self.force_actions_below = force_actions_below
        self.bgcolor = bgcolor

    def _get_control_name(self):
        return "banner"

    def before_update(self):
        super().before_update()
        self._set_attr_json("contentPadding", self.__content_padding)
        self._set_attr_json("leadingPadding", self.__leading_padding)

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        for action in self.__actions:
            action._set_attr_internal("n", "action")
            children.append(action)
        return children

    # open
    @property
    def open(self) -> Optional[bool]:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # modal
    @property
    def modal(self) -> Optional[bool]:
        return self._get_attr("modal", data_type="bool", def_value=False)

    @modal.setter
    def modal(self, value: Optional[bool]):
        self._set_attr("modal", value)

    # leading
    @property
    def leading(self):
        return self.__leading

    @leading.setter
    def leading(self, value):
        self.__leading = value

    # leading_padding
    @property
    def leading_padding(self) -> PaddingValue:
        return self.__leading_padding

    @leading_padding.setter
    def leading_padding(self, value: PaddingValue):
        self.__leading_padding = value

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # content_padding
    @property
    def content_padding(self) -> PaddingValue:
        return self.__content_padding

    @content_padding.setter
    def content_padding(self, value: PaddingValue):
        self.__content_padding = value

    # actions
    @property
    def actions(self):
        return self.__actions

    @actions.setter
    def actions(self, value):
        self.__actions = value if value is not None else []

    # force_actions_below
    @property
    def force_actions_below(self) -> Optional[bool]:
        return self._get_attr("forceActionsBelow", data_type="bool", def_value=False)

    @force_actions_below.setter
    def force_actions_below(self, value: Optional[bool]):
        self._set_attr("forceActionsBelow", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgColor", value)
