from dataclasses import field

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control

__all__ = ["CupertinoContextMenu"]


@control("CupertinoContextMenu")
class CupertinoContextMenu(AdaptiveControl):
    """
    A full-screen modal route that opens up when the content is long-pressed.

    Online docs: https://flet.dev/docs/controls/cupertinocontextmenu
    """

    content: Control
    """
    The child control to be shown. This is a required property.
  
    When the `CupertinoContextMenu` is long-pressed, the menu will open and this widget
    will be moved to the new route and be expanded. This allows the child to resize to 
    fit in its place in the new route, if it doesn't size itself.
    """

    actions: list[Control] = field(default_factory=list)
    """
    A list of action buttons to be shown in the menu. These actions are typically 
    [`CupertinoContextMenuAction`](https://flet.dev/docs/controls/cupertinocontextmenuaction)s. 
    This list must have at least one action.
    """

    enable_haptic_feedback: bool = True
    """
    Whether a click on the `actions` should produce haptic feedback.
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
        assert any(
            a.visible for a in self.actions
        ), "at least one action must be visible"
