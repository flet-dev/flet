from typing import Optional

from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.types import (
    ClipBehavior,
    IconValueOrControl,
    MouseCursor,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
    UrlTarget,
)

__all__ = ["FloatingActionButton"]


@control("FloatingActionButton")
class FloatingActionButton(ConstrainedControl):
    """
    A floating action button is a circular icon button that hovers over content to
    promote a primary action in the application. Floating action button is usually set
    to `page.floating_action_button`, but can also be added as a regular control at any
    place on a page.

    Online docs: https://flet.dev/docs/controls/floatingactionbutton
    """

    content: Optional[StrOrControl] = None
    """
    A Control representing custom button content.
    """

    icon: Optional[IconValueOrControl] = None
    """
    Icon shown in the button.
    """

    bgcolor: OptionalColorValue = None
    """
    Button background [color](https://flet.dev/docs/reference/colors).
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the FAB's border.

    The value is an instance of [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder) 
    class.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than 
    one control on a page with autofocus set, then the first one added to the page will 
    get focus.
    """

    mini: bool = False
    """
    Controls the size of this button.

    By default, floating action buttons are non-mini and have a height and width of 
    `56.0` logical pixels. Mini floating action buttons have a height and width of 
    `40.0` logical pixels with a layout width and height of `48.0` logical pixels.
    """

    foreground_color: OptionalColorValue = None
    """
    The default foreground [color](https://flet.dev/docs/reference/colors) for icons 
    and text within the button.
    """

    focus_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to use for filling the button 
    when the button has input focus.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    The content will be clipped (or not) according to this option.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior) 
    and defaults to `ClipBehavior.NONE`.
    """

    elevation: OptionalNumber = None
    """
    The button's elevation.

    Defaults to `6`.
    """

    disabled_elevation: OptionalNumber = None
    """
    The button's elevation when disabled.

    Defaults to the same value as `elevation`.
    """

    focus_elevation: OptionalNumber = None
    """
    The button's elevation when it has input focus.

    Defaults to `8`.
    """

    highlight_elevation: OptionalNumber = None
    """
    The button's elevation when being touched.

    Defaults to `12`.
    """

    hover_elevation: OptionalNumber = None
    """
    The button's elevation when it is enabled and being hovered.

    Defaults to `8`.
    """

    enable_feedback: Optional[bool] = None
    """
    Whether detected gestures should provide acoustic and/or haptic feedback. On 
    Android, for example, setting this to `True` will produce a click sound and a 
    long-press will produce a short vibration.
    """

    url: Optional[str] = None
    """
    The URL to open when the button is clicked. If registered, `on_click` event is 
    fired after that.
    """

    url_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.

    Value is of type [`UrlTarget`](https://flet.dev/docs/reference/types/urltarget) and 
    defaults to `UrlTarget.BLANK`.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over this 
    control.

    Value is of type [`MouseCursor`](https://flet.dev/docs/reference/types/mousecursor).
    """

    on_click: OptionalControlEventHandler["FloatingActionButton"] = None
    """
    Fires when a user clicks the button.
    """

    def before_update(self):
        super().before_update()
        assert (
            self.icon
            or isinstance(self.content, str)
            or (isinstance(self.content, Control) and self.content.visible)
        ), "at minimum, icon or a visible content must be provided"
        assert self.elevation is None or self.elevation >= 0, (
            "elevation cannot be negative"
        )
        assert self.disabled_elevation is None or self.disabled_elevation >= 0, (
            "disabled_elevation cannot be negative"
        )
        assert self.focus_elevation is None or self.focus_elevation >= 0, (
            "focus_elevation cannot be negative"
        )
        assert self.highlight_elevation is None or self.highlight_elevation >= 0, (
            "highlight_elevation cannot be negative"
        )
        assert self.hover_elevation is None or self.hover_elevation >= 0, (
            "hover_elevation cannot be negative"
        )
