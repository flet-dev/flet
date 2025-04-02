from dataclasses import field
from typing import List, Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.buttons import OutlinedBorder
from flet.core.control import Control, control
from flet.core.text_style import TextStyle
from flet.core.types import (
    ClipBehavior,
    ColorValue,
    MainAxisAlignment,
    OptionalControlEventCallable,
    OptionalNumber,
    PaddingValue,
)

__all__ = ["AlertDialog"]


@control("AlertDialog")
class AlertDialog(AdaptiveControl):
    """
    An alert dialog informs the user about situations that require acknowledgement. An alert dialog has an optional title and an optional list of actions. The title is displayed above the content and the actions are displayed below the content.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.title = "AlertDialog examples"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        dlg = ft.AlertDialog(
            title=ft.Text("Hi, this is a non-modal dialog!"),
            on_dismiss=lambda e: page.add(ft.Text("Non-modal dialog dismissed")),
        )

        def handle_close(e):
            page.close(dlg_modal)
            page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete all those files?"),
            actions=[
                ft.TextButton("Yes", on_click=handle_close),
                ft.TextButton("No", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: page.add(
                ft.Text("Modal dialog dismissed"),
            ),
        )

        page.add(
            ft.ElevatedButton("Open dialog", on_click=lambda e: page.open(dlg)),
            ft.ElevatedButton("Open modal dialog", on_click=lambda e: page.open(dlg_modal)),
        )


    ft.app(target=main)
    ```
    -----

    Online docs: https://flet.dev/docs/controls/alertdialog
    """

    modal: bool = field(default=False)
    title: Optional[Control] = None
    content: Optional[Control] = None
    actions: List[Control] = field(default_factory=list)
    bgcolor: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    icon: Optional[Control] = None
    open: bool = field(default=False)
    title_padding: Optional[PaddingValue] = None
    content_padding: Optional[PaddingValue] = None
    actions_padding: Optional[PaddingValue] = None
    actions_alignment: Optional[MainAxisAlignment] = None
    shape: Optional[OutlinedBorder] = None
    inset_padding: Optional[PaddingValue] = None
    icon_padding: Optional[PaddingValue] = None
    action_button_padding: Optional[PaddingValue] = None
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    icon_color: Optional[ColorValue] = None
    scrollable: bool = field(default=False)
    actions_overflow_button_spacing: OptionalNumber = None
    alignment: Optional[Alignment] = None
    content_text_style: Optional[TextStyle] = None
    title_text_style: Optional[TextStyle] = None
    clip_behavior: Optional[ClipBehavior] = None
    semantics_label: Optional[str] = None
    barrier_color: Optional[ColorValue] = None
    on_dismiss: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.title or self.content or self.actions
        ), "AlertDialog has nothing to display. Provide at minimum one of the following: title, content, actions"
