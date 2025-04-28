from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.text_style import TextStyle
from flet.controls.types import OptionalControlEventCallable, StrOrControl

__all__ = ["CupertinoDialogAction"]


@control("CupertinoDialogAction")
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
                    content="Yes",
                    destructive=True,
                    on_click=handle_action_click,
                ),
                ft.CupertinoDialogAction(
                    content="No",
                    default=True,
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

    content: StrOrControl
    default: bool = False
    destructive: bool = False
    text_style: Optional[TextStyle] = None
    on_click: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            isinstance(self.content, str) or self.content.visible
        ), "content must be a string or a visible Control"
