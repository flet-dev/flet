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
    StrOrControl,
    Url,
)

__all__ = ["OutlinedButton"]


@control("OutlinedButton")
class OutlinedButton(LayoutControl, AdaptiveControl):
    """
    Outlined buttons are medium-emphasis buttons. They contain actions that are
    important, but aren't the primary action in an app. Outlined buttons pair well with
    filled buttons to indicate an alternative, secondary action.

    ```python
    ft.OutlinedButton(content="Outlined button")
    ```

    """

    content: Optional[StrOrControl] = None
    """
    A Control representing custom button content.

    Raises:
        ValueError: If neither [`icon`][(c).] nor [`content`][(c).] is provided.
    """

    icon: Optional[IconDataOrControl] = None
    """
    An icon to display in this button.
    """

    icon_color: Optional[ColorValue] = None
    """
    Icon color.
    """

    style: Optional[ButtonStyle] = None
    """
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus.

    If there is more than one control on a page with autofocus set, then the first one
    added to the page will get focus.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    The content will be clipped (or not) according to this option.
    """

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when this button is clicked.

    Additionally, if [`on_click`][(c).] event callback is
    provided, it is fired after that.
    """

    on_click: Optional[ControlEventHandler["OutlinedButton"]] = None
    """
    Called when a user clicks this button.
    """

    on_long_press: Optional[ControlEventHandler["OutlinedButton"]] = None
    """
    Called when this button is long-pressed.
    """

    on_hover: Optional[ControlEventHandler["OutlinedButton"]] = None
    """
    Called when a mouse pointer enters or exists this button's response area.

    `data` property of event object contains `true` (string) when cursor enters and
    `false` when it exits.
    """

    on_focus: Optional[ControlEventHandler["OutlinedButton"]] = None
    """
    Called when this button has received focus.
    """

    on_blur: Optional[ControlEventHandler["OutlinedButton"]] = None
    """
    Called when this button has lost focus.
    """

    def before_update(self):
        super().before_update()
        if not (
            self.icon
            or isinstance(self.content, str)
            or (isinstance(self.content, Control) and self.content.visible)
        ):
            raise ValueError("at minimum, icon or a visible content must be provided")

    async def focus(self):
        await self._invoke_method("focus")
