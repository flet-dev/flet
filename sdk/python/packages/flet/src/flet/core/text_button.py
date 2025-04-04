import time
from typing import Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.buttons import ButtonStyle
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import (
    ClipBehavior,
    IconValue,
    OptionalColorValue,
    OptionalControlEventCallable,
    UrlTarget,
)

__all__ = ["TextButton"]


@control("TextButton")
class TextButton(ConstrainedControl, AdaptiveControl):
    """
    Text buttons are used for the lowest priority actions, especially when presenting multiple options. Text buttons can be placed on a variety of backgrounds. Until the button is interacted with, its container isn’t visible.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Basic text buttons"
        page.add(
            ft.TextButton(text="Text button"),
            ft.TextButton("Disabled button", disabled=True),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/textbutton
    """

    text: Optional[str] = None
    icon: Optional[IconValue] = None
    icon_color: OptionalColorValue = None
    content: Optional[Control] = None
    style: Optional[ButtonStyle] = None
    autofocus: bool = False
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    clip_behavior: Optional[ClipBehavior] = None
    on_click: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_hover: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    # def before_update(self):
    #     super().before_update()
    #     if self.__style is not None:
    #         self.__style.side = self._wrap_attr_dict(self.__style.side)
    #         self.__style.shape = self._wrap_attr_dict(self.__style.shape)
    #         self.__style.padding = self._wrap_attr_dict(self.__style.padding)
    #     self._set_attr_json("style", self.__style)

    def focus(self):
        self._set_attr_json("focus", str(time.time()))
        self.update()
