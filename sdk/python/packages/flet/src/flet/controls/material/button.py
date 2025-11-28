from dataclasses import field
from typing import Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    IconDataOrControl,
    Number,
    StrOrControl,
    Url,
)

__all__ = ["Button"]


@control("Button")
class Button(LayoutControl, AdaptiveControl):
    """
    A material button.

    It supports various styles, colors, event handlers for user interaction,
    and can be used to display text, icons, etc.

    ```python
    ft.Button(content="Enabled button")
    ft.Button(content="Disabled button", disabled=True)
    ```
    """

    content: Optional[StrOrControl] = None
    """
    The button's label.
    Typically a [`Text`][flet.] control or a string.
    If a string is provided, it will be wrapped in a [`Text`][flet.] control.

    Raises:
        ValueError: If neither [`icon`][(c).] nor [`content`][(c).]
            (string or visible control) is provided.
    """

    icon: Optional[IconDataOrControl] = None
    """
    The icon to display inside the button.
    Typically an [`Icon`][flet.] control or an `IconData`.
    If an `IconData` is provided, it will be wrapped in an [`Icon`][flet.] control.

    Raises:
        ValueError: If neither [`icon`][(c).] nor [`content`][(c).]
            (string or visible control) is provided.
    """
    icon_color: Optional[ColorValue] = None
    """
    The color of the icon.
    If not specified, defaults to the current foreground color.
    """

    color: Optional[ColorValue] = field(default=None, metadata={"skip": True})
    """
    The button's foreground color.
    If not specified, defaults to the theme's primary color.
    """

    bgcolor: Optional[ColorValue] = field(default=None, metadata={"skip": True})
    """
    The button's background color.
    If not specified, defaults to the theme's primary color.
    """

    elevation: Number = field(default=1, metadata={"skip": True})
    """
    The button's elevation.
    If not specified, defaults to `1`.
    """

    style: Optional[ButtonStyle] = field(default=None, metadata={"skip": True})
    """
    The button's style.
    """

    autofocus: Optional[bool] = None
    """
    Whether this button should be focused initially.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    The button's clip behavior.
    """

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when the button is clicked.
    """

    on_click: Optional[ControlEventHandler["Button"]] = None
    """
    Called when the button is clicked.
    """

    on_long_press: Optional[ControlEventHandler["Button"]] = None
    """
    Called when the button is long-pressed.
    """

    on_hover: Optional[ControlEventHandler["Button"]] = None
    """
    Called when the button is hovered.
    """

    on_focus: Optional[ControlEventHandler["Button"]] = None
    """
    Called when the button is focused.
    """

    on_blur: Optional[ControlEventHandler["Button"]] = None
    """
    Called when the button loses focus.
    """

    def before_update(self):
        super().before_update()
        if not (
            self.icon
            or isinstance(self.content, str)
            or (isinstance(self.content, Control) and self.content.visible)
        ):
            raise ValueError(
                "At least icon or content (string or visible Control) must be provided"
            )

        if (
            self.style is not None
            or self.color is not None
            or self.bgcolor is not None
            or self.elevation != 1
        ):
            self._internals["style"] = (self.style or ButtonStyle()).copy(
                color=self.color,
                bgcolor=self.bgcolor,
                elevation=self.elevation,
            )

    async def focus(self):
        """Requests focus for this control."""
        await self._invoke_method("focus")
