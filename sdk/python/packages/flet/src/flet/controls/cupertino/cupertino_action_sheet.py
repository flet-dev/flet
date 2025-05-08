from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.types import StrOrControl

__all__ = ["CupertinoActionSheet"]


@control("CupertinoActionSheet")
class CupertinoActionSheet(ConstrainedControl):
    """
    An iOS-style action sheet.

    Online docs: https://flet.dev/docs/controls/cupertinoactionsheet
    """

    title: Optional[StrOrControl] = None
    """
    A control containing the title of the action sheet.

    Typically a [`Text`](https://flet.dev/docs/controls/text) control.
    """

    message: Optional[StrOrControl] = None
    """
    A control containing a descriptive message that provides more details about the
    reason for the alert.

    Typically a [`Text`](https://flet.dev/docs/controls/text) control.
    """

    actions: Optional[list[Control]] = None
    """
    A list of action buttons to be shown in the sheet.

    These actions are typically [`CupertinoActionSheetAction`](https://flet.dev/docs/controls/cupertinoactionsheetaction)s.

    This list must have at least one action.
    """

    cancel: Optional[Control] = None
    """
    An optional control to be shown below the actions but grouped separately from them.

    Typically a [`CupertinoActionSheetAction`](https://flet.dev/docs/controls/cupertinoactionsheetaction) 
    button.
    """
