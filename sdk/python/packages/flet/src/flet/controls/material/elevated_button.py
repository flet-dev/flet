import asyncio
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    IconValueOrControl,
    Number,
    StrOrControl,
    UrlTarget,
)

__all__ = ["ElevatedButton"]

DEFAULT_ELEVATION = 1


@control("ElevatedButton")
class ElevatedButton(ConstrainedControl, AdaptiveControl):
    """
    Elevated buttons are essentially filled tonal buttons with a shadow. To prevent
    shadow creep, only use them when absolutely necessary, such as when the button
    requires visual separation from a patterned background.

    Raises:
        AssertionError: If both [`content`][(c).] and [`icon`][(c).] are not set or invalid.
    """

    content: Optional[StrOrControl] = None
    """
    A Control representing custom button content.
    """

    icon: Optional[IconValueOrControl] = None
    """
    Icon shown in the button.
    """

    icon_color: Optional[ColorValue] = None
    """
    Icon color.
    """

    color: Optional[ColorValue] = None
    """
    Button's text color.

    Note:
        If both `color` and [`style.color`][flet.ElevatedButton.style]
        are provided, `color` value will be used.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Button's background color.

    Note:
        If both `bgcolor` and [`style.bgcolor`][flet.ElevatedButton.style]
        are provided, `bgcolor` value will be used.
    """

    elevation: Number = DEFAULT_ELEVATION
    """
    Button's elevation.

    Note:
        If both `elevation` and [`style.elevation`][flet.ElevatedButton.style]
        are provided, `elevation` value will be used.
    """

    style: Optional[ButtonStyle] = None
    """
    """

    autofocus: Optional[bool] = None
    """
    True if the control will be selected as the initial focus. If there is more than
    one control on a page with autofocus set, then the first one added to the page will
    get focus.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    The content will be clipped (or not) according to this option.

    Defaults to `ClipBehavior.NONE`.
    """

    url: Optional[str] = None
    """
    The URL to open when the button is clicked. If registered, `on_click` event is
    fired after that.
    """

    url_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.

    Defaults to `UrlTarget.BLANK`.
    """

    on_click: Optional[ControlEventHandler["ElevatedButton"]] = None
    """
    Called when a user clicks the button.
    """

    on_long_press: Optional[ControlEventHandler["ElevatedButton"]] = None
    """
    Called when the button is long-pressed.
    """

    on_hover: Optional[ControlEventHandler["ElevatedButton"]] = None
    """
    Called when a mouse pointer enters or exists the button response area. `data`
    property of event object contains `true` (string) when cursor enters and `false`
    when it exits.

    /// details | Example
        type: example
    ```python
    import flet as ft

    def main(page: ft.Page):
        def on_hover(e):
            e.control.bgcolor = "orange" if e.data == "true" else "yellow"
            e.control.update()

        page.add(
            ft.ElevatedButton(
                "I'm changing color on hover", bgcolor="yellow", on_hover=on_hover
            )
        )

    ft.run(main)
    ```
    ///
    """

    on_focus: Optional[ControlEventHandler["ElevatedButton"]] = None
    """
    Called when the control has received focus.
    """

    on_blur: Optional[ControlEventHandler["ElevatedButton"]] = None
    """
    Called when the control has lost focus.
    """

    def before_update(self):
        super().before_update()
        assert (
            self.icon
            or isinstance(self.content, str)
            or (isinstance(self.content, Control) and self.content.visible)
        ), "at least icon or content (string or visible Control) must be provided"
        if self.style is None and (
            self.color is not None
            or self.bgcolor is not None
            or self.elevation != DEFAULT_ELEVATION
        ):
            self.style = ButtonStyle()
        if self.color is not None:
            self.style.color = self.color
        if self.bgcolor is not None:
            self.style.bgcolor = self.bgcolor
        if self.elevation != DEFAULT_ELEVATION:
            self.style.elevation = self.elevation

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
