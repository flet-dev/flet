from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.text_style import TextStyle
from flet.controls.types import OptionalControlEventCallable, StrOrControl

__all__ = ["CupertinoDialogAction"]


@control("CupertinoDialogAction")
class CupertinoDialogAction(Control):
    """
    A button typically used in a CupertinoAlertDialog.

    Online docs: https://flet.dev/docs/controls/cupertinodialogaction
    """

    content: StrOrControl
    default: bool = False
    destructive: bool = False
    text_style: Optional[TextStyle] = None
    on_click: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            isinstance(self.content, str) or self.content.visible
        ), "content must be a string or a visible Control"
