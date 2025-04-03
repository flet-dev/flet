import warnings
from typing import Any, Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.buttons import ButtonStyle
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.ref import Ref
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
    import warnings

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

    def __post_init__(self, ref: Ref[Any] | None):
        super().__post_init__(ref)
        if "text" in self.__dict__:
            self.content = self.__dict__.pop("text")
            warnings.warn(
                "'text' is deprecated. Use 'content' instead.",
                DeprecationWarning,
                stacklevel=2,
            )

    def __setattr__(self, name, value):
        if name == "text":
            warnings.warn(
                "'text' is deprecated since version 0.70.0 and will be removed in 0.70.3. Use 'content' instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            name = "content"
        super().__setattr__(name, value)

    def __getattribute__(self, name):
        if name == "text":
            name = "content"
        return super().__getattribute__(name)

    text: Optional[str] = None  # deprecated
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
        # assert self.icon or (
        #     self.content and self.content.visible
        # ), "at minimum, icon or a visible content must be provided"

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
