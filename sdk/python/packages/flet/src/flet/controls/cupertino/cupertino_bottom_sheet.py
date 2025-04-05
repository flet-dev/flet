from dataclasses import field
from typing import Optional

from flet.core.control import Control, control
from flet.core.padding import OptionalPaddingValue
from flet.core.types import (
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
