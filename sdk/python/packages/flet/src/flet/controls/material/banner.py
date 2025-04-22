from dataclasses import field
from typing import List, Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.margin import OptionalMarginValue
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["Banner"]


@control("Banner")
class Banner(DialogControl):
    """
    A banner displays an important, succinct message, and provides actions for users to address (or dismiss the banner). A user action is required for it to be dismissed.

    Banners are displayed at the top of the screen, below a top app bar. They are persistent and non-modal, allowing the user to either ignore them or interact with them at any time.

    -----

    Online docs: https://flet.dev/docs/controls/banner
    """

    content: Control
    actions: List[Control] = field(default_factory=list)
    leading: Optional[Control] = None
    leading_padding: OptionalPaddingValue = None
    content_padding: OptionalPaddingValue = None
    force_actions_below: bool = field(default=False)
    bgcolor: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    divider_color: OptionalColorValue = None
    elevation: OptionalNumber = None
    margin: OptionalMarginValue = None
    content_text_style: Optional[TextStyle] = None
    min_action_bar_height: Number = field(default=52.0)
    on_visible: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
        assert self.content.visible, "content must be visible"
        assert any(
            a.visible for a in self.actions
        ), "actions must contain at minimum one visible action Control"
