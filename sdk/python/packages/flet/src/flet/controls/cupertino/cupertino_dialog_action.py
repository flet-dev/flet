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

    Typically used as a child of [`CupertinoAlertDialog.actions`][flet.CupertinoAlertDialog.actions].

    Raises:
        AssertionError: If [`content`][(c).] is neither a string nor a visible Control.
    """

    content: StrOrControl
    """
    The content of this action button.
    """

    default: bool = False
    """
    Whether this action is a default action. In this case, the button will have bold text.

    Info:
        More than one action can have
        this property set to `True` in [`CupertinoAlertDialog`][flet.CupertinoAlertDialog].
    """

    destructive: bool = False
    """
    If set to True, the button's text color will be red. Use it for actions that
    destroy objects, such as an delete that deletes an email etc.
    """

    text_style: Optional[TextStyle] = None
    """
    The text style to use for text in the button.

    Can be useful when [`content`][flet.CupertinoDialogAction.content] is a string.
    """

    on_click: Optional[ControlEventHandler["CupertinoDialogAction"]] = None
    """
    Called when a user clicks the button.
    """

    def before_update(self):
        super().before_update()
        assert isinstance(self.content, str) or self.content.visible, (
            "content must be a string or a visible Control"
        )
