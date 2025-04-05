from flet.core.adaptive_control import AdaptiveControl
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control


@control("ReorderableDraggable")
class ReorderableDraggable(ConstrainedControl, AdaptiveControl):
    index: int
    content: Control
