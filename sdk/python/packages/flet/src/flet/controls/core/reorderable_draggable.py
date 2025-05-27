from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control


@control("ReorderableDraggable")
class ReorderableDraggable(ConstrainedControl, AdaptiveControl):
    """
    TBD
    """
    index: int
    """
    TBD
    """
    content: Control
    """
    TBD
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
