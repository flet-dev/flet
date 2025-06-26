from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.types import MouseCursor, StrOrControl

__all__ = ["CupertinoActionSheetAction"]


@control("CupertinoActionSheetAction")
class CupertinoActionSheetAction(ConstrainedControl):
    """
    An action button typically used in a CupertinoActionSheet.

    Online docs: https://flet.dev/docs/controls/cupertinoactionsheetaction
    """

    content: StrOrControl
    """
    The child control to be shown in this action button.

    In case both `text` and `content` are provided, then `content` will be used.
    """

    default: bool = False
    """
    Whether this action should receive the style of an emphasized, default action.

    Defaults to `False`.
    """

    destructive: bool = False
    """
    Whether this action should receive the style of a destructive action.

    Defaults to `False`.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    TBD
    """

    on_click: OptionalControlEventHandler["CupertinoActionSheetAction"] = None
    """
    Fires when this action button is clicked.
    """

    def before_update(self):
        super().before_update()
        assert isinstance(self.content, str) or self.content.visible, (
            "content must be a string or a visible Control"
        )
