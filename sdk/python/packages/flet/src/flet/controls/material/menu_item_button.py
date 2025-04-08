from typing import Optional

from flet.controls.alignment import Axis
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.types import ClipBehavior, OptionalControlEventCallable

__all__ = ["MenuItemButton"]


@control("MenuItemButton")
class MenuItemButton(ConstrainedControl):
    """
    A button for use in a MenuBar or on its own, that can be activated by click or keyboard navigation.

    -----

    Online docs: https://flet.dev/docs/controls/menuitembutton
    """

    content: Optional[Control] = None
    close_on_click: bool = True
    focus_on_hover: bool = True
    leading: Optional[Control] = None
    trailing: Optional[Control] = None
    clip_behavior: ClipBehavior = ClipBehavior.NONE
    style: Optional[ButtonStyle] = None
    semantic_label: Optional[str] = None
    autofocus: bool = False
    overflow_axis: Axis = Axis.HORIZONTAL
    on_click: OptionalControlEventCallable = None
    on_hover: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
