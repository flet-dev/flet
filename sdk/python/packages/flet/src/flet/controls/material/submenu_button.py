from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.material.menu_bar import MenuStyle
from flet.controls.transform import OffsetValue
from flet.controls.types import ClipBehavior, OptionalControlEventCallable

__all__ = ["SubmenuButton"]


@control("SubmenuButton")
class SubmenuButton(ConstrainedControl):
    """
    A menu button that displays a cascading menu. It can be used as part of
    a MenuBar, or as a standalone control.

    -----

    Online docs: https://flet.dev/docs/controls/submenubutton
    """

    content: Optional[Control] = None
    controls: list[Control] = field(default_factory=list)
    leading: Optional[Control] = None
    trailing: Optional[Control] = None
    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    menu_style: Optional[MenuStyle] = None
    style: Optional[ButtonStyle] = None
    alignment_offset: Optional[OffsetValue] = None
    on_open: OptionalControlEventCallable = None
    on_close: OptionalControlEventCallable = None
    on_hover: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
