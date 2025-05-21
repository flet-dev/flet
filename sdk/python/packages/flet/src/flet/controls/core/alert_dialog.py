from dataclasses import field
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import OptionalTextStyle
from flet.controls.types import (
    ClipBehavior,
    MainAxisAlignment,
    OptionalColorValue,
    OptionalNumber,
    OptionalString,
    StrOrControl,
)

__all__ = ["AlertDialog"]


@control("AlertDialog")
class AlertDialog(DialogControl):
    """
    An alert dialog informs the user about situations that require acknowledgement. An 
    alert dialog has an optional title and an optional list of actions. The title is 
    displayed above the content and the actions are displayed below the content.

    Online docs: https://flet.dev/docs/controls/alertdialog
    """

    content: Optional[Control] = None
    modal: bool = False
    title: Optional[StrOrControl] = None
    actions: list[Control] = field(default_factory=list)
    bgcolor: OptionalColorValue = None
    elevation: OptionalNumber = None
    icon: Optional[Control] = None
    title_padding: OptionalPaddingValue = None
    content_padding: OptionalPaddingValue = None
    actions_padding: OptionalPaddingValue = None
    actions_alignment: Optional[MainAxisAlignment] = None
    shape: Optional[OutlinedBorder] = None
    inset_padding: OptionalPaddingValue = None
    icon_padding: OptionalPaddingValue = None
    action_button_padding: OptionalPaddingValue = None
    surface_tint_color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    icon_color: OptionalColorValue = None
    scrollable: bool = False
    actions_overflow_button_spacing: OptionalNumber = None
    alignment: Optional[Alignment] = None
    content_text_style: OptionalTextStyle = None
    title_text_style: OptionalTextStyle = None
    clip_behavior: Optional[ClipBehavior] = None
    semantics_label: OptionalString = None
    barrier_color: OptionalColorValue = None

    def before_update(self):
        super().before_update()
        assert (
            self.title or self.content or self.actions
        ), "AlertDialog has nothing to display. Provide at minimum one of the "
        "following: title, content, actions"
