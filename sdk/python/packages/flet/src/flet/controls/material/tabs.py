from dataclasses import field
from typing import List, Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.border import BorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.margin import OptionalMarginValue
from flet.controls.material.form_field_control import IconValueOrControl
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    ControlStateValue,
    MouseCursor,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    TabAlignment,
)

__all__ = ["Tab", "Tabs"]


@control("Tab")
class Tab(AdaptiveControl):
    text: Optional[str] = None
    content: Optional[Control] = None
    tab_content: Optional[Control] = None
    icon: Optional[IconValueOrControl] = None
    height: OptionalNumber = None
    icon_margin: OptionalMarginValue = None


@control("Tabs")
class Tabs(ConstrainedControl, AdaptiveControl):
    """
    The Tabs control is used for navigating frequently accessed, distinct content categories. Tabs allow for navigation between two or more content views and relies on text headers to articulate the different sections of content.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):

        t = ft.Tabs(
            selected_index=1,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Tab 1",
                    content=ft.Container(
                        content=ft.Text("This is Tab 1"), alignment=ft.alignment.center
                    ),
                ),
                ft.Tab(
                    tab_content=ft.Icon(ft.icons.SEARCH),
                    content=ft.Text("This is Tab 2"),
                ),
                ft.Tab(
                    text="Tab 3",
                    icon=ft.icons.SETTINGS,
                    content=ft.Text("This is Tab 3"),
                ),
            ],
            expand=1,
        )

        page.add(t)


    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/tabs
    """

    tabs: List[Tab] = field(default_factory=list)
    selected_index: int = 0
    scrollable: bool = True
    tab_alignment: Optional[TabAlignment] = None
    animation_duration: Optional[int] = None
    divider_color: OptionalColorValue = None
    indicator_color: OptionalColorValue = None
    indicator_border_radius: OptionalBorderRadiusValue = None
    indicator_border_side: Optional[BorderSide] = None
    indicator_padding: OptionalPaddingValue = None
    indicator_tab_size: Optional[bool] = None
    is_secondary: Optional[bool] = None
    label_color: bool = False
    label_padding: OptionalPaddingValue = None
    label_text_style: Optional[TextStyle] = None
    unselected_label_color: OptionalColorValue = None
    unselected_label_text_style: Optional[TextStyle] = None
    overlay_color: ControlStateValue[ColorValue] = None
    divider_height: Number = 1.0
    indicator_thickness: Number = 2.0
    enable_feedback: Optional[str] = None
    mouse_cursor: Optional[MouseCursor] = None
    padding: OptionalPaddingValue = None
    splash_border_radius: OptionalBorderRadiusValue = None
    clip_behavior: Optional[ClipBehavior] = None
    on_click: OptionalControlEventCallable = None
    on_change: OptionalControlEventCallable = None

    # def before_update(self):
    #     super().before_update()
    #     self._set_attr_json("overlayColor", self.__overlay_color, wrap_attr_dict=True)

    def __contains__(self, item):
        return item in self.tabs
