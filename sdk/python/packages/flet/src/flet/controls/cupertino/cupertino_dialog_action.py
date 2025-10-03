from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.text_style import TextStyle
from flet.controls.types import StrOrControl

__all__ = ["CupertinoDialogAction"]


@control("CupertinoDialogAction")
class CupertinoDialogAction(Control):
    """
    A dialog action button.

    Typically used as a child of [`CupertinoAlertDialog.actions`][flet.].
    """

    content: StrOrControl
    """
    The content of this action button.

    Raises:
        ValueError: If [`content`][(c).] is neither a string nor a visible Control.
    """

    default: bool = False
    """
    Whether this action is a default action.
    In this case, the button will have bold text.

    Info:
        Multiple actions can have this property set to `True`
        in a [`CupertinoAlertDialog`][flet.].
    """

    destructive: bool = False
    """
    If set to `True`, this button's text color will be red.

    Typically used for actions that destroy objects,
    such as an delete that deletes an email etc.
    """

    text_style: Optional[TextStyle] = None
    """
    The text style to use for text in this button.

    Can be useful when [`content`][(c).] is a string.
    """

    on_click: Optional[ControlEventHandler["CupertinoDialogAction"]] = None
    """
    Called when a user clicks this button.
    """

    def before_update(self):
        super().before_update()
        if not (isinstance(self.content, str) or self.content.visible):
            raise ValueError("content must be a string or a visible Control")
