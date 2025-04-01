from typing import List, Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.buttons import OutlinedBorder
from flet.core.control import Control, control
from flet.core.text_style import TextStyle
from flet.core.types import ClipBehavior, ColorValue, OptionalNumber


@control("AppBar")
class AppBar(AdaptiveControl):
    """
    A material design app bar.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def check_item_clicked(e):
            e.control.checked = not e.control.checked
            page.update()

        page.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.PALETTE),
            leading_width=40,
            title=ft.Text("AppBar Example"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
                ft.IconButton(ft.icons.FILTER_3),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Item 1"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            text="Checked item", checked=False, on_click=check_item_clicked
                        ),
                    ]
                ),
            ],
        )
        page.add(ft.Text("Body!"))

    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/appbar
    """

    leading: Optional[Control] = None
    leading_width: OptionalNumber = None
    automatically_imply_leading: Optional[bool] = None
    title: Optional[Control] = None
    center_title: Optional[bool] = None
    toolbar_height: OptionalNumber = None
    color: Optional[ColorValue] = None
    bgcolor: Optional[ColorValue] = None
    elevation: OptionalNumber = None
    elevation_on_scroll: OptionalNumber = None
    shadow_color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    clip_behavior: Optional[ClipBehavior] = None
    force_material_transparency: Optional[bool] = None
    is_secondary: Optional[bool] = None
    title_spacing: OptionalNumber = None
    exclude_header_semantics: Optional[bool] = None
    actions: Optional[List[Control]] = None
    toolbar_opacity: OptionalNumber = None
    title_text_style: Optional[TextStyle] = None
    toolbar_text_style: Optional[TextStyle] = None
    shape: Optional[OutlinedBorder] = None

    def before_update(self):
        super().before_update()
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
        assert (
            self.elevation_on_scroll is None or self.elevation_on_scroll >= 0
        ), "elevation_on_scroll cannot be negative"
