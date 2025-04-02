from dataclasses import field
from typing import Optional

from flet.core.control import Control, control
from flet.core.types import (
    ColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    PaddingValue,
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
    bgcolor: Optional[ColorValue] = None
    height: OptionalNumber = None
    padding: Optional[PaddingValue] = None
    on_dismiss: OptionalControlEventCallable = None
