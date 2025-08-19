from dataclasses import field
from typing import Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    IconDataOrControl,
    Number,
    StrOrControl,
    Url,
)

__all__ = ["ElevatedButton"]


@control("ElevatedButton")
class ElevatedButton(ConstrainedControl, AdaptiveControl):
    """
    Elevated buttons are essentially filled tonal buttons with a shadow. To prevent
    shadow creep, only use them when absolutely necessary, such as when the button
    requires visual separation from a patterned background.

    Raises:
        AssertionError: If both [`content`][(c).] and [`icon`][(c).] are not set
            or invalid.
    """

    content: Optional[StrOrControl] = None
    """
    A Control representing custom button content.
    """

    icon: Optional[IconDataOrControl] = None
    """
    Icon shown in the button.
    """

    icon_color: Optional[ColorValue] = None
    """
    Icon color.
    """

    color: Optional[ColorValue] = field(default=None, metadata={"skip": True})
    """
    Button's text color.

    Note:
        If both `color` and [`style.color`][flet.ElevatedButton.style]
        are provided, `color` value will be used.
    """

    bgcolor: Optional[ColorValue] = field(default=None, metadata={"skip": True})
    """
    Button's background color.

    Note:
        If both `bgcolor` and [`style.bgcolor`][flet.ElevatedButton.style]
        are provided, `bgcolor` value will be used.
    """

    elevation: Number = field(default=1, metadata={"skip": True})
    """
    Button's elevation.

    Note:
        If both `elevation` and [`style.elevation`][flet.ElevatedButton.style]
        are provided, `elevation` value will be used.
    """

    style: Optional[ButtonStyle] = field(default=None, metadata={"skip": True})
    """
    The style of the button.

    Note:
        The values of [`color`][flet.ElevatedButton.color],
        [`bgcolor`][flet.ElevatedButton.bgcolor`] and
        [`elevation`][flet.ElevatedButton.elevation], if not `None`, will override
        the respective values of this `style`.
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

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when this button is clicked.

    Additionally, if [`on_click`][flet.ElevatedButton.on_click] event callback is
    provided, it is fired after that.
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
            e.control.bgcolor = ft.Colors.ORANGE if e.data else ft.Colors.YELLOW
            e.control.update()

        page.add(
            ft.ElevatedButton(
                "I'm changing color on hover",
                bgcolor="ft.Colors.YELLOW",
                on_hover=on_hover,
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
        await self._invoke_method("focus")
