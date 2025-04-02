from dataclasses import field
from typing import List, Optional

from flet.core.control import Control, control
from flet.core.text_style import TextStyle
from flet.core.types import (
    ColorValue,
    MarginValue,
    Number,
    OptionalControlEventCallable,
    OptionalNumber,
    PaddingValue,
)

__all__ = ["Banner"]


@control("Banner")
class Banner(Control):
    """
    A banner displays an important, succinct message, and provides actions for users to address (or dismiss the banner). A user action is required for it to be dismissed.

    Banners are displayed at the top of the screen, below a top app bar. They are persistent and non-modal, allowing the user to either ignore them or interact with them at any time.

    Example:
    ```
    import flet as ft


    def main(page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def close_banner(e):
            page.close(banner)
            page.add(ft.Text("Action clicked: " + e.control.text))

        action_button_style = ft.ButtonStyle(color=ft.colors.BLUE)
        banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                value="Oops, there were some errors while trying to delete the file. What would you like me to do?",
                color=ft.colors.BLACK,
            ),
            actions=[
                ft.TextButton(text="Retry", style=action_button_style, on_click=close_banner),
                ft.TextButton(text="Ignore", style=action_button_style, on_click=close_banner),
                ft.TextButton(text="Cancel", style=action_button_style, on_click=close_banner),
            ],
        )

        page.add(ft.ElevatedButton("Show Banner", on_click=lambda e: page.open(banner)))


    ft.app(main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/banner
    """

    content: Control
    actions: List[Control] = field(default_factory=list)
    open: bool = False
    leading: Optional[Control] = None
    leading_padding: Optional[PaddingValue] = None
    content_padding: Optional[PaddingValue] = None
    force_actions_below: bool = field(default=False)
    bgcolor: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    divider_color: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    margin: Optional[MarginValue] = None
    content_text_style: Optional[TextStyle] = None
    min_action_bar_height: Number = field(default=52.0)
    on_visible: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
        assert self.content.visible, "content must be visible"
        assert any(
            a.visible for a in self.actions
        ), "actions must contain at minimum one visible action Control"
