from typing import Annotated

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.utils.validation import V

__all__ = ["CupertinoContextMenu"]


@control("CupertinoContextMenu")
class CupertinoContextMenu(AdaptiveControl):
    """
    A full-screen modal route that opens up when the [`content`][(c).] is \
    long-pressed.
    """

    content: Annotated[
        Control,
        V.visible_control(),
    ]
    """
    The content of this context menu.

    Info:
        When this context menu is long-pressed, the menu will open and this control
        will be moved to the new route and be expanded. This allows the content
        to resize to fit in its place in the new route, if it doesn't size itself.

    Raises:
        ValueError: If it is not visible.
    """

    actions: Annotated[
        list[Control],
        V.visible_controls(min_count=1),
    ]
    """
    A list of action buttons to be shown in the menu.

    Typically [`CupertinoContextMenuAction`][flet.]s.

    Raises:
        ValueError: If it does not contain at least one visible `Control`.
    """

    enable_haptic_feedback: bool = True
    """
    Whether a click on the [`actions`][(c).] should produce haptic feedback.
    """
