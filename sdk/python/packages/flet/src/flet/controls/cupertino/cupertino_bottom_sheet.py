from dataclasses import field
from typing import Optional

from flet.controls.control import Control, control
from flet.controls.dialog_control import DialogControl
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["CupertinoBottomSheet"]


@control("CupertinoBottomSheet")
class CupertinoBottomSheet(DialogControl):
    """
    A Cupertino version of modal bottom sheet.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinobottomsheet
    """

    content: Optional[Control] = None
    modal: bool = field(default=False)
    bgcolor: OptionalColorValue = None
    height: OptionalNumber = None
    padding: OptionalPaddingValue = None
