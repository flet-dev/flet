from typing import Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.padding import OptionalPaddingValue

__all__ = ["SafeArea"]


@control("SafeArea", kw_only=True)
class SafeArea(ConstrainedControl, AdaptiveControl):
    content: Control
    left: Optional[bool] = None
    top: Optional[bool] = None
    right: Optional[bool] = None
    bottom: Optional[bool] = None
    maintain_bottom_view_padding: Optional[bool] = None
    minimum_padding: OptionalPaddingValue = None

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
