from dataclasses import field
from typing import Optional

from flet.controls.control import Control, control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["CupertinoBottomSheet"]


@control("CupertinoBottomSheet")
class CupertinoBottomSheet(Control):
    """
    A Cupertino version of modal bottom sheet.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinobottomsheet
    """

    content: Optional[Control] = None
    open: bool = field(default=False)
    modal: bool = field(default=False)
    bgcolor: OptionalColorValue = None
    height: OptionalNumber = None
    padding: OptionalPaddingValue = None
    on_dismiss: OptionalControlEventCallable = None
