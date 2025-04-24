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

    -----

    Online docs: https://flet.dev/docs/controls/cupertinobottomsheet
    """

    content: Control
    modal: bool = False
    bgcolor: OptionalColorValue = None
    height: OptionalNumber = None
    padding: OptionalPaddingValue = None
