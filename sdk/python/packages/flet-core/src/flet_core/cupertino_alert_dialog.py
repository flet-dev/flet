from typing import Any, List, Optional

from flet_core.types import OptionalEventCallable
from flet_core.control import Control
from flet_core.ref import Ref


class CupertinoAlertDialog(Control):
    """
    An iOS-style alert dialog.
    An alert dialog informs the user about situations that require acknowledgement. An alert dialog has an optional title and an optional list of actions. The title is displayed above the content and the actions are displayed below the content.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.scroll = True

        def handle_action_click(e):
            page.add(ft.Text(f"Action clicked: {e.control.text}"))
            # e.control is the clicked action button, e.control.parent is the corresponding parent dialog of the button
            page.close(e.control.parent)

        cupertino_actions = [
            ft.CupertinoDialogAction(
                "Yes",
                is_destructive_action=True,
                on_click=handle_action_click,
            ),
            ft.CupertinoDialogAction(
                text="No",
                is_default_action=False,
                on_click=handle_action_click,
            ),
        ]

        material_actions = [
            ft.TextButton(text="Yes", on_click=handle_action_click),
            ft.TextButton(text="No", on_click=handle_action_click),
        ]

        page.add(
            ft.FilledButton(
                text="Open Material Dialog",
                on_click=lambda e: page.open(
                    ft.AlertDialog(
                        title=ft.Text("Material Alert Dialog"),
                        content=ft.Text("Do you want to delete this file?"),
                        actions=material_actions,
                    )
                ),
            ),
            ft.CupertinoFilledButton(
                text="Open Cupertino Dialog",
                on_click=lambda e: page.open(
                    ft.CupertinoAlertDialog(
                        title=ft.Text("Cupertino Alert Dialog"),
                        content=ft.Text("Do you want to delete this file?"),
                        actions=cupertino_actions,
                    )
                ),
            ),
            ft.FilledButton(
                text="Open Adaptive Dialog",
                adaptive=True,
                on_click=lambda e: page.open(
                    ft.AlertDialog(
                        adaptive=True,
                        title=ft.Text("Adaptive Alert Dialog"),
                        content=ft.Text("Do you want to delete this file?"),
                        actions=cupertino_actions if page.platform in [ft.PagePlatform.IOS, ft.PagePlatform.MACOS] else material_actions,
                    )
                ),
            ),
        )


    ft.app(target=main)
    ```
    -----

    Online docs: https://flet.dev/docs/controls/cupertinoalertdialog
    """

    def __init__(
        self,
        open: bool = False,
        modal: bool = False,
        title: Optional[Control] = None,
        content: Optional[Control] = None,
        actions: Optional[List[Control]] = None,
        on_dismiss: OptionalEventCallable = None,
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
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    def title(self, value: Optional[Control]):
        self.__title = value

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # actions
    @property
    def actions(self) -> List[Control]:
        return self.__actions

    @actions.setter
    def actions(self, value: Optional[List[Control]]):
        self.__actions = value if value is not None else []

    # on_dismiss
    @property
    def on_dismiss(self) -> OptionalEventCallable:
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler: OptionalEventCallable):
        self._add_event_handler("dismiss", handler)
