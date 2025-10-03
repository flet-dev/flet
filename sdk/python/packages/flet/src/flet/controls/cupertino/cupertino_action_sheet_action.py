from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import MouseCursor, StrOrControl

__all__ = ["CupertinoActionSheetAction"]


@control("CupertinoActionSheetAction")
class CupertinoActionSheetAction(LayoutControl):
    """
    An action button typically used in a CupertinoActionSheet.
    """

    content: StrOrControl
    """
    The child control to be shown in this action button.

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

    mouse_cursor: Optional[MouseCursor] = None
    """
    Defines the mouse cursor for this action button.
    """

    on_click: Optional[ControlEventHandler["CupertinoActionSheetAction"]] = None
    """
    Called when this action button is clicked.
    """

    def before_update(self):
        super().before_update()
        if not (isinstance(self.content, str) or self.content.visible):
            raise ValueError("content must be a string or a visible Control")
