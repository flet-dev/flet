from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import OptionalControlEventCallable


class CupertinoDialogAction(Control):
    """
    A button typically used in a CupertinoAlertDialog.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def dialog_dismissed(e):
            page.add(ft.Text("Dialog dismissed"))

        def handle_action_click(e):
            page.add(ft.Text(f"Action clicked: {e.control.text}"))
            page.close(cupertino_alert_dialog)

        cupertino_alert_dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Cupertino Alert Dialog"),
            content=ft.Text("Do you want to delete this file?"),
            on_dismiss=dialog_dismissed,
            actions=[
                ft.CupertinoDialogAction(
                    text="Yes",
                    is_destructive_action=True,
                    on_click=handle_action_click,
                ),
                ft.CupertinoDialogAction(
                    text="No",
                    is_default_action=True,
                    on_click=handle_action_click
                ),
            ],
        )

        page.add(
            ft.CupertinoFilledButton(
                text="Open CupertinoAlertDialog",
                on_click=lambda e: page.open(cupertino_alert_dialog),
            )
        )


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/cupertinodialogaction
    """

    def __init__(
        self,
        text: Optional[str] = None,
        content: Optional[Control] = None,
        is_default_action: Optional[bool] = None,
        is_destructive_action: Optional[bool] = None,
        text_style: Optional[TextStyle] = None,
        on_click: OptionalControlEventCallable = None,
        #
        # Specific
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

        self.text = text
        self.content = content
        self.on_click = on_click
        self.is_default_action = is_default_action
        self.is_destructive_action = is_destructive_action
        self.text_style = text_style

    def _get_control_name(self):
        return "cupertinodialogaction"

    def before_update(self):
        super().before_update()
        self._set_attr_json("textStyle", self.__text_style)

    def _get_children(self):
        if self.__content is None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # text
    @property
    def text(self) -> Optional[str]:
        return self._get_attr("text")

    @text.setter
    def text(self, value: Optional[str]):
        self._set_attr("text", value)

    # is_default_action
    @property
    def is_default_action(self) -> bool:
        return self._get_attr("isDefaultAction", data_type="bool", def_value=False)

    @is_default_action.setter
    def is_default_action(self, value: Optional[bool]):
        self._set_attr("isDefaultAction", value)

    # is_destructive_action
    @property
    def is_destructive_action(self) -> bool:
        return self._get_attr("isDestructiveAction", data_type="bool", def_value=False)

    @is_destructive_action.setter
    def is_destructive_action(self, value: Optional[bool]):
        self._set_attr("isDestructiveAction", value)

    # on_click
    @property
    def on_click(self) -> OptionalControlEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalControlEventCallable):
        self._add_event_handler("click", handler)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # text_style
    @property
    def text_style(self) -> Optional[TextStyle]:
        return self.__text_style

    @text_style.setter
    def text_style(self, value: Optional[TextStyle]):
        self.__text_style = value
