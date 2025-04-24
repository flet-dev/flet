from typing import Optional

from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import (
    ClipBehavior,
    IconValueOrControl,
    MouseCursor,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    StrOrControl,
    UrlTarget,
)

__all__ = ["FloatingActionButton"]


@control("FloatingActionButton")
class FloatingActionButton(ConstrainedControl):
    """
    A floating action button is a circular icon button that hovers over content to promote a primary action in the application. Floating action button is usually set to `page.floating_action_button`, but can also be added as a regular control at any place on a page.

    Online docs: https://flet.dev/docs/controls/floatingactionbutton
    """

    content: Optional[StrOrControl] = None
    icon: Optional[IconValueOrControl] = None
    bgcolor: OptionalColorValue = None
    shape: Optional[OutlinedBorder] = None
    autofocus: bool = False
    mini: bool = False
    foreground_color: OptionalColorValue = None
    focus_color: OptionalColorValue = None
    clip_behavior: Optional[ClipBehavior] = None
    elevation: OptionalNumber = None
    disabled_elevation: OptionalNumber = None
    focus_elevation: OptionalNumber = None
    highlight_elevation: OptionalNumber = None
    hover_elevation: OptionalNumber = None
    enable_feedback: bool = True
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    mouse_cursor: Optional[MouseCursor] = None
    on_click: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.icon or (
            self.content and self.content.visible
        ), "at minimum, text, icon or a visible content must be provided"
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
        assert (
            self.disabled_elevation is None or self.disabled_elevation >= 0
        ), "disabled_elevation cannot be negative"
        assert (
            self.focus_elevation is None or self.focus_elevation >= 0
        ), "focus_elevation cannot be negative"
        assert (
            self.highlight_elevation is None or self.highlight_elevation >= 0
        ), "highlight_elevation cannot be negative"
        assert (
            self.hover_elevation is None or self.hover_elevation >= 0
        ), "hover_elevation cannot be negative"
