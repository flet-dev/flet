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

    content: Optional[Control] = (None,)
    open: bool = (False,)
    modal: bool = (False,)
    bgcolor: Optional[ColorValue] = (None,)
    height: OptionalNumber = (None,)
    padding: Optional[PaddingValue] = (None,)
    on_dismiss: OptionalControlEventCallable = (None,)
