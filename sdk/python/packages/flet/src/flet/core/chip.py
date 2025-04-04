from typing import Optional

from flet.core.animation import AnimationStyle
from flet.core.border import BorderSide
from flet.core.box import BoxConstraints
from flet.core.buttons import OutlinedBorder
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.padding import OptionalPaddingValue
from flet.core.text_style import TextStyle
from flet.core.types import (
    ClipBehavior,
    ColorValue,
    ControlStateValue,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    VisualDensity,
)

__all__ = ["Chip"]


@control("Chip")
class Chip(ConstrainedControl):
    """
    Chips are compact elements that represent an attribute, text, entity, or action.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        def save_to_favorites_clicked(e):
            e.control.label.value = "Saved to favorites"
            e.control.leading = ft.Icon(ft.icons.FAVORITE_OUTLINED)
            e.control.disabled = True
            page.update()

        def open_google_maps(e):
            page.launch_url("https://maps.google.com")
            page.update()

        save_to_favourites = ft.Chip(
            label=ft.Text("Save to favourites"),
            leading=ft.Icon(ft.icons.FAVORITE_BORDER_OUTLINED),
            bgcolor=ft.colors.GREEN_200,
            disabled_color=ft.colors.GREEN_100,
            autofocus=True,
            on_click=save_to_favorites_clicked,
        )

        open_in_maps = ft.Chip(
            label=ft.Text("9 min walk"),
            leading=ft.Icon(ft.icons.MAP_SHARP),
            bgcolor=ft.colors.GREEN_200,
            on_click=open_google_maps,
        )

        page.add(ft.Row([save_to_favourites, open_in_maps]))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/chip
    """

    label: Control
    leading: Optional[Control] = None
    selected: Optional[bool] = False
    selected_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    bgcolor: OptionalColorValue = None
    show_checkmark: Optional[bool] = None
    check_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    shape: Optional[OutlinedBorder] = None
    padding: OptionalPaddingValue = None
    delete_icon: Optional[Control] = None
    delete_icon_tooltip: Optional[str] = None
    delete_icon_color: OptionalColorValue = None
    disabled_color: OptionalColorValue = None
    label_padding: OptionalPaddingValue = None
    label_style: Optional[TextStyle] = None
    selected_shadow_color: OptionalColorValue = None
    autofocus: Optional[bool] = None
    surface_tint_color: OptionalColorValue = None
    color: ControlStateValue[ColorValue] = None
    click_elevation: OptionalNumber = None
    clip_behavior: Optional[ClipBehavior] = None
    visual_density: Optional[VisualDensity] = None
    border_side: Optional[BorderSide] = None
    leading_size_constraints: Optional[BoxConstraints] = None
    delete_icon_size_constraints: Optional[BoxConstraints] = None
    enable_animation_style: Optional[AnimationStyle] = None
    select_animation_style: Optional[AnimationStyle] = None
    leading_drawer_animation_style: Optional[AnimationStyle] = None
    delete_drawer_animation_style: Optional[AnimationStyle] = None
    on_click: OptionalControlEventCallable = None
    on_delete: OptionalControlEventCallable = None
    on_select: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
