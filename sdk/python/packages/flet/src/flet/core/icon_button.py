import time
from typing import Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.box import BoxConstraints
from flet.core.buttons import ButtonStyle
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import (
    ColorValue,
    IconValue,
    MouseCursor,
    OptionalControlEventCallable,
    OptionalNumber,
    PaddingValue,
    UrlTarget,
    VisualDensity,
)

__all__ = ["IconButton"]


@control("IconButton")
class IconButton(ConstrainedControl, AdaptiveControl):
    """
    An icon button is a round button with an icon in the middle that reacts to touches by filling with color (ink).

    Icon buttons are commonly used in the toolbars, but they can be used in many other places as well.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Icon buttons"
        page.add(
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.PAUSE_CIRCLE_FILLED_ROUNDED,
                        icon_color="blue400",
                        icon_size=20,
                        tooltip="Pause record",
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE_FOREVER_ROUNDED,
                        icon_color="pink600",
                        icon_size=40,
                        tooltip="Delete record",
                    ),
                ]
            ),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/iconbutton
    """

    icon: Optional[IconValue] = None
    icon_color: Optional[ColorValue] = None
    icon_size: OptionalNumber = None
    selected: bool = False
    selected_icon: Optional[IconValue] = None
    selected_icon_color: Optional[ColorValue] = None
    bgcolor: Optional[ColorValue] = None
    highlight_color: Optional[ColorValue] = None
    style: Optional[ButtonStyle] = None
    content: Optional[Control] = None
    autofocus: bool = False
    disabled_color: Optional[ColorValue] = None
    hover_color: Optional[ColorValue] = None
    focus_color: Optional[ColorValue] = None
    splash_color: Optional[ColorValue] = None
    splash_radius: OptionalNumber = None
    alignment: Optional[Alignment] = None
    padding: Optional[PaddingValue] = None
    enable_feedback: Optional[bool] = None
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    mouse_cursor: Optional[MouseCursor] = None
    visual_density: Optional[VisualDensity] = None
    size_constraints: Optional[BoxConstraints] = None
    on_click: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    # def before_update(self):
    #     super().before_update()
    #     if self.__style is not None:
    #         self.__style.side = self._wrap_attr_dict(self.__style.side)
    #         self.__style.shape = self._wrap_attr_dict(self.__style.shape)
    #         self.__style.padding = self._wrap_attr_dict(self.__style.padding)

    def focus(self):
        self._set_attr_json("focus", str(time.time()))
        self.update()
