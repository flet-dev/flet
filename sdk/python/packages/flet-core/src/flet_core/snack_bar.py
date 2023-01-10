from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref


class SnackBar(Control):
    """
    A lightweight message with an optional action which briefly displays at the bottom of the screen.

    Example:
    ```
    import flet as ft

    class Data:
        def __init__(self) -> None:
            self.counter = 0

    d = Data()

    def main(page):

        page.snack_bar = ft.SnackBar(
            content=ft.Text("Hello, world!"),
            action="Alright!",
        )
        page.snack_bar.open = True

        def on_click(e):
            page.snack_bar = ft.SnackBar(ft.Text(f"Hello {d.counter}"))
            page.snack_bar.open = True
            d.counter += 1
            page.update()

        page.add(ft.ElevatedButton("Open SnackBar", on_click=on_click))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/snackbar
    """

    def __init__(
        self,
        content: Control,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        open: bool = False,
        # remove_current_snackbar: bool = False,
        action: Optional[str] = None,
        action_color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        on_action=None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.open = open
        # self.remove_current_snackbar = remove_current_snackbar
        self.content = content
        self.action = action
        self.action_color = action_color
        self.bgcolor = bgcolor
        self.on_action = on_action

    def _get_control_name(self):
        return "snackbar"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # open
    @property
    def open(self) -> Optional[bool]:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # # remove_current_snackbar
    # @property
    # def remove_current_snackbar(self):
    #     return self._get_attr(
    #         "removeCurrentSnackBar", data_type="bool", def_value=False
    #     )

    # @remove_current_snackbar.setter
    #
    # def remove_current_snackbar(self, value: Optional[bool]):
    #     self._set_attr("removeCurrentSnackBar", value)

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # action
    @property
    def action(self):
        return self._get_attr("action")

    @action.setter
    def action(self, value):
        self._set_attr("action", value)

    # action_color
    @property
    def action_color(self):
        return self._get_attr("actionColor")

    @action_color.setter
    def action_color(self, value):
        self._set_attr("actionColor", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgColor", value)

    # on_action
    @property
    def on_action(self):
        return self._get_event_handler("action")

    @on_action.setter
    def on_action(self, handler):
        self._add_event_handler("action", handler)
