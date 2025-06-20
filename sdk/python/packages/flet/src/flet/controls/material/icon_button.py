import asyncio
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.box import BoxConstraints
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    IconValueOrControl,
    MouseCursor,
    OptionalColorValue,
    OptionalNumber,
    UrlTarget,
    VisualDensity,
)
from flet.utils.deprecated import deprecated_warning

__all__ = ["IconButton"]


@control("IconButton")
class IconButton(ConstrainedControl, AdaptiveControl):
    """
    An icon button is a round button with an icon in the middle that reacts to touches
    by filling with color (ink).

    Icon buttons are commonly used in the toolbars, but they can be used in many other
    places as well.

    Online docs: https://flet.dev/docs/controls/iconbutton
    """

    def __setattr__(self, name, value):
        if name == "content" and value is not None:
            deprecated_warning(
                name="content",
                reason="Use 'icon' instead.",
                version="0.70.0",
                delete_version="0.73.0",
            )
        super().__setattr__(name, value)

    icon: Optional[IconValueOrControl] = None
    """
    Icon shown in the button.
    """

    icon_color: OptionalColorValue = None
    """
    Icon [color](https://flet.dev/docs/reference/colors).
    """

    icon_size: OptionalNumber = None
    """
    Icon size in virtual pixels.

    Defaults to `24`.
    """

    selected: Optional[bool] = None
    """
    The optional selection state of the icon button.

    If this property is not set, the button will behave as a normal push button, 
    otherwise, the button will toggle between showing `icon` and `selected_icon` based
    on the value of `selected`. 
    
    If True, it will show `selected_icon`, if False it will show `icon`.
    """

    selected_icon: Optional[IconValueOrControl] = None
    """
    Icon shown in the button in selected state.
    """

    selected_icon_color: OptionalColorValue = None
    """
    Icon [color](https://flet.dev/docs/reference/colors) for the selected state.

    An example of icon toggle button:

    <img src="/img/blog/gradients/toggle-icon-button.gif" className="screenshot-10" />

    ```python
    import flet as ft

    def main(page: ft.Page):

        def toggle_icon_button(e):
            e.control.selected = not e.control.selected

        page.add(
            ft.IconButton(
                icon=ft.Icons.BATTERY_1_BAR,
                selected_icon=ft.Icons.BATTERY_FULL,
                on_click=toggle_icon_button,
                selected=False,
                style=ft.ButtonStyle(
                    color={"selected": ft.Colors.GREEN, "": ft.Colors.RED},
                ),
            )
        )

    ft.app(main)
    ```
    """

    bgcolor: OptionalColorValue = None
    """
    TBD
    """

    highlight_color: OptionalColorValue = None
    """
    The button's [color](https://flet.dev/docs/reference/colors) when the button is 
    pressed. The highlight fades in quickly as the button is held down.
    """

    style: Optional[ButtonStyle] = None
    """
    Value is of type [`ButtonStyle`](https://flet.dev/docs/reference/types/buttonstyle).
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than 
    one control on a page with autofocus set, then the first one added to the page will 
    get focus.
    """

    disabled_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for the icon inside the
      button when disabled.
    """

    hover_color: OptionalColorValue = None
    """
    The button's [color](https://flet.dev/docs/reference/colors) when hovered.
    """

    focus_color: OptionalColorValue = None
    """
    The button's [color](https://flet.dev/docs/reference/colors) when in focus.
    """

    splash_color: OptionalColorValue = None
    """
    The primary [color](https://flet.dev/docs/reference/colors) of the button when the 
    button is in the down (pressed) state.
    """

    splash_radius: OptionalNumber = None
    """
    The splash radius. Honoured only when in Material 2.
    """

    alignment: Optional[Alignment] = None
    """
    Defines how the icon is positioned within the IconButton. Alignment is an instance
    of [`Alignment`](https://flet.dev/docs/reference/types/alignment) class.

    Defaults to `alignment.center`.
    """

    padding: OptionalPaddingValue = None
    """
    Defines the padding around this button. The entire padded icon will react to input 
    gestures.

    Value is of type [`Padding`](https://flet.dev/docs/reference/types/padding) and 
    defaults to `Padding.all(8)`.
    """

    enable_feedback: Optional[bool] = None
    """
    Whether detected gestures should provide acoustic and/or haptic feedback. 
    On Android, for example, setting this to `True` produce a click sound and a 
    long-press will produce a short vibration. 
    """

    url: Optional[str] = None
    """
    The URL to open when the button is clicked. If registered, `on_click` event is fired
    after that.
    """

    url_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.

    Value is of type [`UrlTarget`](https://flet.dev/docs/reference/types/urltarget).
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over this 
    control.

    Value is of type [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor).
    """

    visual_density: Optional[VisualDensity] = None
    """
    Defines how compact the control's layout will be.

    Value is of type [`VisualDensity`](https://flet.dev/docs/reference/types/visualdensity).
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    TBD
    """

    on_click: OptionalControlEventHandler["IconButton"] = None
    """
    Fires when a user clicks the button.
    """

    on_focus: OptionalControlEventHandler["IconButton"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["IconButton"] = None
    """
    Fires when the control has lost focus.
    """

    content: Optional[Control] = None  # todo(0.70.3): remove in favor of icon
    """
    A Control representing custom button content.
    """

    async def focus_async(self):
        """
        Moves focus to a button.
        """
        await self._invoke_method_async("focus")

    def focus(self):
        """
        Moves focus to a button.
        """
        asyncio.create_task(self.focus_async())
