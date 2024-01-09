from typing import Any, List, Optional

from flet_core.buttons import OutlinedBorder
from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.types import MainAxisAlignment, MainAxisAlignmentString, PaddingValue


class CupertinoAlertDialog(Control):
    """
    An alert dialog informs the user about situations that require acknowledgement. An alert dialog has an optional title and an optional list of actions. The title is displayed above the content and the actions are displayed below the content.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "AlertDialog examples"

        dlg = ft.AlertDialog(
            title=ft.Text("Hello, you!"), on_dismiss=lambda e: print("Dialog dismissed!")
        )

        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete all those files?"),
            actions=[
                ft.TextButton("Yes", on_click=close_dlg),
                ft.TextButton("No", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        def open_dlg(e):
            page.dialog = dlg
            dlg.open = True
            page.update()

        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        page.add(
            ft.ElevatedButton("Open dialog", on_click=open_dlg),
            ft.ElevatedButton("Open modal dialog", on_click=open_dlg_modal),
        )

    ft.app(target=main)
    ```
    -----

    Online docs: https://flet.dev/docs/controls/alertdialog
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        open: bool = False,
        modal: bool = False,
        title: Optional[Control] = None,
        content: Optional[Control] = None,
        actions: Optional[List[Control]] = None,
        on_dismiss=None,
    ):
        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.__title: Optional[Control] = None
        self.__content: Optional[Control] = None
        self.__actions: List[Control] = []

        self.open = open
        self.modal = modal
        self.title = title
        self.content = content
        self.actions = actions
        self.on_dismiss = on_dismiss

    def _get_control_name(self):
        return "cupertinoalertdialog"

    def _get_children(self):
        children = []
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
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

    # title
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # actions
    @property
    def actions(self):
        return self.__actions

    @actions.setter
    def actions(self, value):
        self.__actions = value if value is not None else []

    # on_dismiss
    @property
    def on_dismiss(self):
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler):
        self._add_event_handler("dismiss", handler)
