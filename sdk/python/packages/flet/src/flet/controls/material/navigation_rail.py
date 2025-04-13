from dataclasses import field
from enum import Enum
from typing import List, Optional

from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    IconValueOrControl,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    StrOrControl,
)
from flet.utils import deprecated_warning

__all__ = ["NavigationRail", "NavigationRailDestination", "NavigationRailLabelType"]


class NavigationRailLabelType(Enum):
    NONE = "none"
    ALL = "all"
    SELECTED = "selected"


@control("NavigationRailDestination")
class NavigationRailDestination(Control):
    def __setattr__(self, name, value):
        if name == "label_content" and value is not None:
            deprecated_warning(
                name="label_content",
                reason="Use label instead.",
                version="0.70.0",
                delete_version="0.73.0",
            )
        super().__setattr__(name, value)

    icon: Optional[IconValueOrControl] = None
    selected_icon: Optional[IconValueOrControl] = None
    label: Optional[StrOrControl] = None
    label_content: Optional[Control] = None  # todo(0.70.3): remove in favor of label
    padding: OptionalPaddingValue = None
    indicator_color: OptionalColorValue = None
    indicator_shape: Optional[OutlinedBorder] = None


@control("NavigationRail")
class NavigationRail(ConstrainedControl):
    """
    A material widget that is meant to be displayed at the left or right of an app to navigate between a small number of views, typically between three and five.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):

        rail = ft.NavigationRail(
            selected_index=1,
            label_type=ft.NavigationRailLabelType.ALL,
            # extended=True,
            min_width=100,
            min_extended_width=400,
            leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.FAVORITE_BORDER, selected_icon=ft.icons.FAVORITE, label="First"
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label="Second",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("Settings"),
                ),
            ],
            on_change=lambda e: print("Selected destination:", e.control.selected_index),
        )

        page.add(
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Column([ ft.Text("Body!")], alignment=ft.MainAxisAlignment.START, expand=True),
                ],
                expand=True,
            )
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/navigationrail
    """

    destinations: List[NavigationRailDestination] = field(default_factory=list)
    elevation: OptionalNumber = None
    selected_index: int = 0
    extended: bool = False
    label_type: Optional[NavigationRailLabelType] = None
    bgcolor: OptionalColorValue = None
    indicator_color: OptionalColorValue = None
    indicator_shape: Optional[OutlinedBorder] = None
    leading: Optional[Control] = None
    trailing: Optional[Control] = None
    min_width: OptionalNumber = None
    min_extended_width: OptionalNumber = None
    group_alignment: OptionalNumber = None
    selected_label_text_style: Optional[TextStyle] = None
    unselected_label_text_style: Optional[TextStyle] = None
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        if self.elevation is not None:
            assert self.elevation >= 0, "elevation cannot be negative"
        if self.min_width is not None:
            assert self.min_width >= 0, "min_width cannot be negative"
        if self.min_extended_width is not None:
            assert self.min_extended_width >= 0, "min_extended_width cannot be negative"
