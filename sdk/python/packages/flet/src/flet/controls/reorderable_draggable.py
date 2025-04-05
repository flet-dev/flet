from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control


@control("ReorderableDraggable")
class ReorderableDraggable(ConstrainedControl, AdaptiveControl):
    index: int
    content: Control

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
