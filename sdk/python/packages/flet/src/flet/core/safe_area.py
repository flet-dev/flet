from dataclasses import field

from flet.core import padding
from flet.core.adaptive_control import AdaptiveControl
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.padding import OptionalPaddingValue

__all__ = ["SafeArea"]


@control("SafeArea", kw_only=True)
class SafeArea(ConstrainedControl, AdaptiveControl):
    content: Control
    left: bool = True
    top: bool = True
    right: bool = True
    bottom: bool = True
    maintain_bottom_view_padding: bool = False
    minimum_padding: OptionalPaddingValue = field(
        default_factory=lambda: padding.all(0)
    )

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
