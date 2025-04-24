from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.padding import PaddingValue

__all__ = ["SafeArea"]


@control("SafeArea", kw_only=True)
class SafeArea(ConstrainedControl, AdaptiveControl):
    content: Control
    left: bool = True
    top: bool = True
    right: bool = True
    bottom: bool = True
    maintain_bottom_view_padding: bool = False
    minimum_padding: PaddingValue = 0

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
