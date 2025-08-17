from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.types import IconData, StrOrControl

__all__ = ["CupertinoContextMenuAction"]


@control("CupertinoContextMenuAction")
class CupertinoContextMenuAction(AdaptiveControl):
    """
    A cupertino context menu action.

    Typically used as a child of
    [`CupertinoContextMenu.actions`][flet.CupertinoContextMenu.actions].

    Raises:
        AssertionError: If [`content`][(c).] is neither a string nor a visible Control.
    """

    content: StrOrControl
    """
    The content of this action button.
    """

    default: bool = False
    """
    Whether this action should receive the style of an emphasized, default action.
    """

    destructive: bool = False
    """
    Whether this action should receive the style of a destructive action.
    """

    trailing_icon: Optional[IconData] = None
    """
    An optional icon to display at the right of the
    [`content`][flet.CupertinoContextMenuAction.content] control.
    """

    on_click: Optional[ControlEventHandler["CupertinoContextMenuAction"]] = None
    """
    Called when this action button is clicked.
    """

    def before_update(self):
        super().before_update()
        assert isinstance(self.content, str) or self.content.visible, (
            "content must be a string or a visible Control"
        )
