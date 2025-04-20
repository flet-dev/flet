from dataclasses import field
from typing import List

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control

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
    enable_haptic_feedback: bool = True

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
        assert any(
            a.visible for a in self.actions
        ), "at least one action must be visible"
