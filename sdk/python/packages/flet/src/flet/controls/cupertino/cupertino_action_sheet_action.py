from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEventHandler
from flet.controls.types import MouseCursor, StrOrControl

__all__ = ["CupertinoActionSheetAction"]


@control("CupertinoActionSheetAction")
class CupertinoActionSheetAction(ConstrainedControl):
    """
    An action button typically used in a CupertinoActionSheet.
    """

    content: StrOrControl
    """
    The child control to be shown in this action button.

    In case both `text` and `content` are provided, then `content` will be used.
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
    TBD
    """

    on_click: Optional[ControlEventHandler["CupertinoActionSheetAction"]] = None
    """
    Fires when this action button is clicked.
    """

    def before_update(self):
        super().before_update()
        assert isinstance(self.content, str) or self.content.visible, (
            "content must be a string or a visible Control"
        )
