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

    Typically used as a child of [`CupertinoContextMenu.actions`][flet.].
    """

    content: StrOrControl
    """
    The content of this action button.

    Raises:
        ValueError: If [`content`][(c).] is neither a string nor a visible Control.
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
    An icon to display at the right of the [`content`][(c).] control.
    """

    on_click: Optional[ControlEventHandler["CupertinoContextMenuAction"]] = None
    """
    Called when this action button is clicked.
    """

    def before_update(self):
        super().before_update()
        if not (isinstance(self.content, str) or self.content.visible):
            raise ValueError("content must be a string or a visible Control")
