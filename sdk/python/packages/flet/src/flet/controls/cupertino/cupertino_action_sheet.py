from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.types import StrOrControl

__all__ = ["CupertinoActionSheet"]


@control("CupertinoActionSheet")
class CupertinoActionSheet(LayoutControl):
    """
    An iOS-style action sheet.
    """

    title: Optional[StrOrControl] = None
    """
    A control containing the title of the action sheet.

    Typically a [`Text`][flet.Text] control.
    """

    message: Optional[StrOrControl] = None
    """
    A control containing a descriptive message that provides more details about the
    reason for the alert.

    Typically a [`Text`][flet.Text] control.
    """

    actions: Optional[list[Control]] = None
    """
    A list of action buttons to be shown in the sheet.

    These actions are typically
    [`CupertinoActionSheetAction`][flet.CupertinoActionSheetAction]s.

    This list must have at least one action.
    """

    cancel: Optional[Control] = None
    """
    An optional control to be shown below the actions but grouped separately from them.

    Typically a [`CupertinoActionSheetAction`][flet.CupertinoActionSheetAction]
    button.
    """
