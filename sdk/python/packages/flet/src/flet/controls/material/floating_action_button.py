from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    IconDataOrControl,
    MouseCursor,
    Number,
    StrOrControl,
    Url,
)

__all__ = ["FloatingActionButton"]


@control("FloatingActionButton")
class FloatingActionButton(ConstrainedControl):
    """
    A floating action button is a circular icon button that hovers over content to
    promote a primary action in the application. Floating action button is usually set
    to `page.floating_action_button`, but can also be added as a regular control at any
    place on a page.

    Raises:
        AssertionError: If neither [`icon`][(c).] nor a valid [`content`][(c).]
            (string or visible Control) is provided.
        AssertionError: If [`elevation`][(c).],
            [`disabled_elevation`][(c).], [`focus_elevation`][(c).],
            [`highlight_elevation`][(c).], or [`hover_elevation`][(c).]
            is negative.
    """

    content: Optional[StrOrControl] = None
    """
    The content of this button.
    """

    icon: Optional[IconDataOrControl] = None
    """
    Icon shown in this button.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Button background color.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the FAB's border.
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

    foreground_color: Optional[ColorValue] = None
    """
    The default foreground color for icons
    and text within this button.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color to use for filling this button
    when it has input focus.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    Defines how the [`content`][flet.FloatingActionButton.content] is clipped.
    """

    elevation: Optional[Number] = None
    """
    The elevation of this button.

    Defaults to `6`.
    """

    disabled_elevation: Optional[Number] = None
    """
    The elevation of this button when disabled.

    Defaults to the same value as `elevation`.
    """

    focus_elevation: Optional[Number] = None
    """
    The elevation of this button when it has input focus.

    Defaults to `8`.
    """

    highlight_elevation: Optional[Number] = None
    """
    The elevation of this button when it is highlighted.

    Defaults to `12`.
    """

    hover_elevation: Optional[Number] = None
    """
    The elevation of this button it is enabled and being hovered over.

    Defaults to `8`.
    """

    hover_color: Optional[ColorValue] = None
    """
    The color to use for filling this button when hovered.
    """

    splash_color: Optional[ColorValue] = None
    """
    The color to use for the ink splash.
    """

    enable_feedback: Optional[bool] = None
    """
    Whether detected gestures should provide acoustic and/or haptic feedback. On
    Android, for example, setting this to `True` will produce a click sound and a
    long-press will produce a short vibration.
    """

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when this button is clicked.

    Additionally, if [`on_click`][flet.FloatingActionButton.on_click] event callback
    is provided, it is fired after that.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over this
    control.
    """

    on_click: Optional[ControlEventHandler["FloatingActionButton"]] = None
    """
    Called when a user clicks this button.
    """

    def before_update(self):
        super().before_update()
        assert (
            self.icon
            or isinstance(self.content, str)
            or (isinstance(self.content, Control) and self.content.visible)
        ), "at minimum, icon or a content (string or visible Control) must be provided"
        assert self.elevation is None or self.elevation >= 0, (
            f"elevation must be greater than or equal to 0, got {self.elevation}"
        )
        assert self.disabled_elevation is None or self.disabled_elevation >= 0, (
            "disabled_elevation must be greater than or equal to 0, "
            f"got {self.disabled_elevation}"
        )
        assert self.focus_elevation is None or self.focus_elevation >= 0, (
            "focus_elevation must be greater than or equal to 0, "
            f"got {self.focus_elevation}"
        )
        assert self.highlight_elevation is None or self.highlight_elevation >= 0, (
            "highlight_elevation must be greater than or equal to 0, "
            f"got {self.highlight_elevation}"
        )
        assert self.hover_elevation is None or self.hover_elevation >= 0, (
            "hover_elevation must be greater than or equal to 0, "
            f"got {self.hover_elevation}"
        )
