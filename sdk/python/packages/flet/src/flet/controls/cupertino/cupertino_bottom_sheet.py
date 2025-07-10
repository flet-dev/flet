from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.padding import PaddingValue
from flet.controls.types import ColorValue, Number

__all__ = ["CupertinoBottomSheet"]


@control("CupertinoBottomSheet")
class CupertinoBottomSheet(DialogControl):
    """
    A Cupertino version of modal bottom sheet.
    """

    content: Control
    """
    The control to be displayed.
    """

    modal: bool = False
    """
    Whether this bottom sheet can be dismissed/closed by clicking the area outside of
    it.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The sheet's background color.
    """

    height: Optional[Number] = None
    """
    The height of this bottom sheet.
    """

    padding: Optional[PaddingValue] = None
    """
    The sheet's padding.
    """
