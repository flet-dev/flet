from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import MouseCursor, OptionalControlEventCallable, StrOrControl

__all__ = ["CupertinoActionSheetAction"]


@control("CupertinoActionSheetAction")
class CupertinoActionSheetAction(ConstrainedControl):
    """
    An action button typically used in a CupertinoActionSheet.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoactionsheetaction
    """

    content: StrOrControl
    default: bool = False
    destructive: bool = False
    mouse_cursor: Optional[MouseCursor] = None
    on_click: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            isinstance(self.content, str) or self.content.visible
        ), "content must be a string or a visible Control"
