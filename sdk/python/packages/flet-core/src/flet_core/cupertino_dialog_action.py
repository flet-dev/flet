from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle


class CupertinoDialogAction(Control):
    """
    A button typically used in a CupertinoAlertDialog.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        cupertino_alert_dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Cupertino Alert Dialog"),
            content=ft.Text("body"),
            on_dismiss=lambda e: print("Dismissed!"),
            actions=[
                ft.CupertinoDialogAction(
                    "OK",
                    is_destructive_action=True,
                ),
                ft.CupertinoDialogAction(text="Cancel", is_default_action=False),
            ],
        )

        page.add(
            ft.OutlinedButton("Open Cupertino Dialog", on_click=lambda e: page.show_dialog(cupertino_alert_dialog)),
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
        on_click=None,
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
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # is_default_action
    @property
    def is_default_action(self) -> Optional[bool]:
        return self._get_attr("isDefaultAction")

    @is_default_action.setter
    def is_default_action(self, value: Optional[bool]):
        self._set_attr("isDefaultAction", value)

    # is_destructive_action
    @property
    def is_destructive_action(self) -> Optional[bool]:
        return self._get_attr("isDestructiveAction")

    @is_destructive_action.setter
    def is_destructive_action(self, value: Optional[bool]):
        self._set_attr("isDestructiveAction", value)

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
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
    def text_style(self):
        return self.__text_style

    @text_style.setter
    def text_style(self, value: Optional[TextStyle]):
        self.__text_style = value
