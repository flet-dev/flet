from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.control import control
from flet.controls.types import IconValue, OptionalControlEventCallable, StrOrControl

__all__ = ["CupertinoContextMenuAction"]

from flet.utils import deprecated_warning


@control("CupertinoContextMenuAction")
class CupertinoContextMenuAction(AdaptiveControl):
    """
    An action that can be added to a CupertinoContextMenu.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinocontextmenuaction
    """

    content: Optional[StrOrControl] = None  # todo(0.70.3): make required
    text: Optional[str] = None  # todo(0.70.3): remove in favor of content
    is_default_action: bool = False
    is_destructive_action: bool = False
    trailing_icon: Optional[IconValue] = None
    on_click: OptionalControlEventCallable = None

    def __setattr__(self, name, value):
        if name == "text" and value is not None:
            deprecated_warning(
                name=name,
                reason="Use content instead.",
                version="0.70.0",
                delete_version="0.70.3",
            )
        super().__setattr__(name, value)
