from dataclasses import field
from typing import List, Optional

from flet.controls.animation import Animation
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl

__all__ = ["CupertinoAlertDialog"]


@control("CupertinoAlertDialog")
class CupertinoAlertDialog(DialogControl):
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

    modal: bool = False
    title: Optional[Control] = None
    content: Optional[Control] = None
    actions: List[Control] = field(default_factory=list)
    inset_animation: Optional[Animation] = None
