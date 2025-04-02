from dataclasses import field
from typing import List, Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.control import Control, control

__all__ = ["CupertinoContextMenu"]


@control("CupertinoContextMenu")
class CupertinoContextMenu(AdaptiveControl):
    """
    A full-screen modal route that opens up when the content is long-pressed.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinocontextmenu
    """

    content: Control
    actions: List[Control] = field(default_factory=list)
    enable_haptic_feedback: Optional[bool] = None

    def before_update(self):
        super().before_update()
        assert (
            len(self.actions) > 0
        ), "actions must be provided and at least one must be visible"
