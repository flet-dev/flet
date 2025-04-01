from dataclasses import field
from typing import Optional

from flet.core.alignment import Axis
from flet.core.buttons import ButtonStyle
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import (
    ClipBehavior,
    OptionalControlEventCallable,
)


@control("MenuItemButton")
class MenuItemButton(ConstrainedControl):
    """
    A button for use in a MenuBar or on its own, that can be activated by click or keyboard navigation.

    -----

    Online docs: https://flet.dev/docs/controls/menuitembutton
    """

    content: Optional[Control] = None
    close_on_click: bool = field(default=True)
    focus_on_hover: bool = field(default=True)
    leading: Optional[Control] = None
    trailing: Optional[Control] = None
    clip_behavior: Optional[ClipBehavior] = None
    style: Optional[ButtonStyle] = None
    semantic_label: Optional[str] = None
    autofocus: bool = field(default=False)
    overflow_axis: Optional[Axis] = None
    on_click: OptionalControlEventCallable = None
    on_hover: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
