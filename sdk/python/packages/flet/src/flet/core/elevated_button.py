from typing import Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.buttons import ButtonStyle
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import (
    ClipBehavior,
    ColorValue,
    IconValue,
    OptionalControlEventCallable,
    OptionalNumber,
    StrOrControl,
    UrlTarget,
)

__all__ = ["ElevatedButton"]


@control("ElevatedButton")
class ElevatedButton(ConstrainedControl, AdaptiveControl):
    """
    Elevated buttons are essentially filled tonal buttons with a shadow. To prevent shadow creep, only use them when absolutely necessary, such as when the button requires visual separation from a patterned background.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Basic elevated buttons"
        page.add(
            ft.ElevatedButton(text="Elevated button"),
            ft.ElevatedButton("Disabled button", disabled=True),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/elevatedbutton
    """

    text: Optional[str] = None
    icon: Optional[IconValue] = None
    icon_color: Optional[ColorValue] = None
    color: Optional[ColorValue] = None
    bgcolor: Optional[ColorValue] = None
    content: Optional[StrOrControl] = None
    elevation: OptionalNumber = None
    style: Optional[ButtonStyle] = None
    autofocus: Optional[bool] = None
    clip_behavior: Optional[ClipBehavior] = None
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    on_click: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_hover: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.icon or (
            self.content and self.content.visible
        ), "at minimum, icon or a visible content must be provided"

    # def before_update(self):
    #     super().before_update()
    #     assert (
    #         self.text or self.icon or (self.__content and self.__content.visible)
    #     ), "at minimum, text, icon or a visible content must be provided"
    #     style = self.__style or ButtonStyle()
    #     if self.__color is not None:
    #         style.color = self.__color
    #     if self.__bgcolor is not None:
    #         style.bgcolor = self.__bgcolor
    #     if self.__elevation is not None:
    #         style.elevation = self.__elevation

    #     style.side = self._wrap_attr_dict(style.side)
    #     style.shape = self._wrap_attr_dict(style.shape)
    #     style.padding = self._wrap_attr_dict(style.padding)
    #     style.text_style = self._wrap_attr_dict(style.text_style)
    #     self._set_attr_json("style", style)

    def focus(self):
        # self._set_attr_json("focus", str(time.time()))
        self.update()
