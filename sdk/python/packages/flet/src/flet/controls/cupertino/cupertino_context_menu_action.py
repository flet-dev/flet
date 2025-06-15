from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.types import IconValue, StrOrControl

__all__ = ["CupertinoContextMenuAction"]


@control("CupertinoContextMenuAction")
class CupertinoContextMenuAction(AdaptiveControl):
    """
    An action that can be added to a CupertinoContextMenu.

    Online docs: https://flet.dev/docs/controls/cupertinocontextmenuaction
    """

    content: StrOrControl
    """
    String or Control to be shown in this action button.
    """

    default: bool = False
    """
    Whether this action should receive the style of an emphasized, default action.
    """

    destructive: bool = False
    """
    Whether this action should receive the style of a destructive action.
    """

    trailing_icon: Optional[IconValue] = None
    """
    An optional icon to display at the right of the `text` or `content` control.
    """

    on_click: OptionalControlEventHandler["CupertinoContextMenuAction"] = None
    """
    Fires when this action button is clicked.
    """

    def before_update(self):
        super().before_update()
        assert isinstance(self.content, str) or self.content.visible, (
            "content must be a string or a visible Control"
        )
