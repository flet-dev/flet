from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.types import IconValue, OptionalControlEventCallable, StrOrControl

__all__ = ["CupertinoContextMenuAction"]


@control("CupertinoContextMenuAction")
class CupertinoContextMenuAction(AdaptiveControl):
    """
    An action that can be added to a CupertinoContextMenu.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinocontextmenuaction
    """

    content: StrOrControl
    default: bool = False
    destructive: bool = False
    trailing_icon: Optional[IconValue] = None
    on_click: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            isinstance(self.content, str) or self.content.visible
        ), "content must be a string or a visible Control"
