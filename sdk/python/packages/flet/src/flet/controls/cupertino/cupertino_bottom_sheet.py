from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import OptionalColorValue, OptionalNumber

__all__ = ["CupertinoBottomSheet"]


@control("CupertinoBottomSheet")
class CupertinoBottomSheet(DialogControl):
    """
    A Cupertino version of modal bottom sheet.

    Online docs: https://flet.dev/docs/controls/cupertinobottomsheet
    """

    content: Control
    """
    The content of the bottom sheet.
    """

    modal: bool = False
    """
    Whether this bottom sheet can be dismissed/closed by clicking the area outside of 
    it.
    """

    bgcolor: OptionalColorValue = None
    """
    The sheet's background [color](https://flet.dev/docs/reference/colors).
    """

    height: OptionalNumber = None
    """
    The height of the bottom sheet.
    """

    padding: OptionalPaddingValue = None
    """
    The sheet's padding. The value is an instance of 
    [`Padding`](https://flet.dev/docs/reference/types/padding) class or a number.
    """
