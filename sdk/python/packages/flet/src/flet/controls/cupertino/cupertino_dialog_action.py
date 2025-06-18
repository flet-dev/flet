from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.text_style import TextStyle
from flet.controls.types import StrOrControl

__all__ = ["CupertinoDialogAction"]


@control("CupertinoDialogAction")
class CupertinoDialogAction(Control):
    """
    A button typically used in a CupertinoAlertDialog.

    Online docs: https://flet.dev/docs/controls/cupertinodialogaction
    """

    content: StrOrControl
    """
    A Control representing custom button content.
    """

    default: bool = False
    """
    If set to True, the button will have bold text. More than one action can have 
    this property set to True in CupertinoAlertDialog.

    Defaults to `False`.
    """

    destructive: bool = False
    """
    If set to True, the button's text color will be red. Use it for actions that 
    destroy objects, such as an delete that deletes an email etc.

    Defaults to `False`.
    """

    text_style: Optional[TextStyle] = None
    """
    The text style to use for text on the button.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    on_click: OptionalControlEventHandler["CupertinoDialogAction"] = None
    """
    Fires when a user clicks the button.
    """

    def before_update(self):
        super().before_update()
        assert isinstance(self.content, str) or self.content.visible, (
            "content must be a string or a visible Control"
        )
