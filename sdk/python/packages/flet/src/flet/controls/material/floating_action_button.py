from typing import Optional

from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import control
from flet.controls.types import (
    ClipBehavior,
    IconValueOrControl,
    MouseCursor,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    StrOrControl,
    UrlTarget,
)

__all__ = ["FloatingActionButton"]

from flet.utils import deprecated_warning


@control("FloatingActionButton")
class FloatingActionButton(ConstrainedControl):
    """
    A floating action button is a circular icon button that hovers over content to promote a primary action in the application. Floating action button is usually set to `page.floating_action_button`, but can also be added as a regular control at any place on a page.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Floating Action Button"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.auto_scroll = True
        page.scroll = ft.ScrollMode.HIDDEN
        page.appbar = ft.AppBar(
            title=ft.Text(
                "Floating Action Button", weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87
            ),
            bgcolor=ft.colors.BLUE,
            center_title=True,
            actions=[
                ft.IconButton(ft.icons.MENU, tooltip="Menu", icon_color=ft.colors.BLACK87)
            ],
            color=ft.colors.WHITE,
        )

        # keeps track of the number of tiles already added
        page.count = 0

        def fab_pressed(e):
            page.add(ft.ListTile(title=ft.Text(f"Tile {page.count}")))
            page.show_snack_bar(
                ft.SnackBar(ft.Text("Tile was added successfully!"), open=True)
            )
            page.count += 1

        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=fab_pressed, bgcolor=ft.colors.LIME_300
        )
        page.add(ft.Text("Press the FAB to add a tile!"))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/floatingactionbutton
    """

    def __setattr__(self, name, value):
        if name == "text" and value is not None:
            deprecated_warning(
                name="text",
                reason="Use 'content' instead.",
                version="0.70.0",
                delete_version="0.70.3",
            )
        super().__setattr__(name, value)

    content: Optional[StrOrControl] = None
    icon: Optional[IconValueOrControl] = None
    bgcolor: OptionalColorValue = None
    shape: Optional[OutlinedBorder] = None
    autofocus: bool = False
    mini: bool = False
    foreground_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    clip_behavior: Optional[ClipBehavior] = None
    elevation: OptionalNumber = None
    disabled_elevation: OptionalNumber = None
    focus_elevation: OptionalNumber = None
    highlight_elevation: OptionalNumber = None
    hover_elevation: OptionalNumber = None
    enable_feedback: bool = True
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    mouse_cursor: Optional[MouseCursor] = None
    on_click: OptionalControlEventCallable = None
    text: Optional[str] = None  # todo(0.70.3): remove in favor of content

    def before_update(self):
        super().before_update()
        assert (
            self.text
            or self.icon
            or (self.content and self.content.visible)  # text to be removed in 0.70.3
        ), "at minimum, text, icon or a visible content must be provided"
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
        assert (
            self.disabled_elevation is None or self.disabled_elevation >= 0
        ), "disabled_elevation cannot be negative"
        assert (
            self.focus_elevation is None or self.focus_elevation >= 0
        ), "focus_elevation cannot be negative"
        assert (
            self.highlight_elevation is None or self.highlight_elevation >= 0
        ), "highlight_elevation cannot be negative"
        assert (
            self.hover_elevation is None or self.hover_elevation >= 0
        ), "hover_elevation cannot be negative"
