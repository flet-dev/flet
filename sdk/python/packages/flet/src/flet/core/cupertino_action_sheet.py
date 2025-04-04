from dataclasses import field
from typing import List, Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control

__all__ = ["CupertinoActionSheet"]


@control("CupertinoActionSheet")
class CupertinoActionSheet(ConstrainedControl):
    """
    An iOS-style action sheet.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoactionsheet
    """

    title: Optional[Control] = None
    message: Optional[Control] = None
    actions: List[Control] = field(default_factory=list)
    cancel: Optional[Control] = None
