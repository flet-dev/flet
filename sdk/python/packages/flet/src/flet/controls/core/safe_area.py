from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import PaddingValue

__all__ = ["SafeArea"]


@control("SafeArea")
class SafeArea(ConstrainedControl, AdaptiveControl):
    """
    A control that insets its `content` by sufficient padding to avoid intrusions by 
    the operating system.

    For example, this will indent the `content` by enough to avoid the status bar at 
    the top of the screen.

    It will also indent the `content` by the amount necessary to avoid The Notch on the 
    iPhone X, or other similar creative physical features of the display.

    When a `minimum_padding` is specified, the greater of the minimum padding or the 
    safe area padding will be applied.
    """
    content: Control
    avoid_intrusions_left: bool = True
    avoid_intrusions_top: bool = True
    avoid_intrusions_right: bool = True
    avoid_intrusions_bottom: bool = True
    maintain_bottom_view_padding: bool = False
    minimum_padding: PaddingValue = 0

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
