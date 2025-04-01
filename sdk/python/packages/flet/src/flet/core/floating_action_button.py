from dataclasses import field
from typing import Any, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.buttons import OutlinedBorder
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber, control
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ClipBehavior,
    ColorEnums,
    ColorValue,
    IconEnums,
    IconValue,
    MouseCursor,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    UrlTarget,
)


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

    text: Optional[str] = None
    icon: Optional[IconValue] = None
    bgcolor: Optional[ColorValue] = None
    content: Optional[Control] = None
    shape: Optional[OutlinedBorder] = None
    autofocus: Optional[bool] = field(default=False)
    mini: Optional[bool] = field(default=False)
    foreground_color: Optional[ColorValue] = None
    focus_color: Optional[ColorValue] = None
    clip_behavior: Optional[ClipBehavior] = None
    elevation: OptionalNumber = None
    disabled_elevation: OptionalNumber = None
    focus_elevation: OptionalNumber = None
    highlight_elevation: OptionalNumber = None
    hover_elevation: OptionalNumber = None
    enable_feedback: Optional[bool] = field(default=True)
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    mouse_cursor: Optional[MouseCursor] = None
    on_click: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.text or self.icon or (self.content and self.content.visible)
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
