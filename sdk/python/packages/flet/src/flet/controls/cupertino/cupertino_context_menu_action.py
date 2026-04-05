from typing import Annotated, Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.types import IconData, StrOrControl
from flet.utils.validation import V

__all__ = ["CupertinoContextMenuAction"]


@control("CupertinoContextMenuAction")
class CupertinoContextMenuAction(AdaptiveControl):
    """
    A cupertino context menu action.

    Typically used as a child of :attr:`flet.CupertinoContextMenu.actions`.
    """

    content: Annotated[
        StrOrControl,
        V.str_or_visible_control(),
    ]
    """
    The content of this action button.

    Raises:
        ValueError: If it is neither a string nor a visible `Control`.
    """

    default: bool = False
    """
    Whether this action should receive the style of an emphasized, default action.
    """

    destructive: bool = False
    """
    Whether this action should receive the style of a destructive action.
    """

    trailing_icon: Optional[IconData] = None
    """
    An icon to display at the right of the :attr:`content` control.
    """

    on_click: Optional[ControlEventHandler["CupertinoContextMenuAction"]] = None
    """
    Called when this action button is clicked.
    """
