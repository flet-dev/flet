from typing import Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.control import Control, control
from flet.core.types import IconValue, OptionalControlEventCallable

__all__ = ["CupertinoContextMenuAction"]


@control("CupertinoContextMenuAction")
class CupertinoContextMenuAction(AdaptiveControl):
    """
    An action that can be added to a CupertinoContextMenu.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinocontextmenuaction
    """

    text: Optional[str] = None
    content: Optional[Control] = None
    is_default_action: Optional[bool] = None
    is_destructive_action: Optional[bool] = None
    trailing_icon: Optional[IconValue] = None
    on_click: OptionalControlEventCallable = None
