from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.material.menu_bar import MenuStyle
from flet.controls.transform import OffsetValue
from flet.controls.types import ClipBehavior

__all__ = ["SubmenuButton"]


@control("SubmenuButton")
class SubmenuButton(ConstrainedControl):
    """
    A menu button that displays a cascading menu. It can be used as part of
    a MenuBar, or as a standalone control.
    """

    content: Optional[Control] = None
    """
    The child control to be displayed in the middle portion of this button.

    Typically this is the button's label, using a `Text` control.
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of controls that appear in the menu when it is opened.

    Typically either `MenuItemButton` or `SubMenuButton` controls.

    If this list is empty, then the button for this menu item will be disabled.
    """

    leading: Optional[Control] = None
    """
    An optional control to display before the `content`.

    Typically an [`Icon`][flet.Icon] control.
    """

    trailing: Optional[Control] = None
    """
    An optional control to display after the `content`.

    Typically an [`Icon`][flet.Icon] control.
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    Whether to clip the content of this control or not.

    Value is of type
    [`ClipBehavior`][flet.ClipBehavior] and
    defaults to `ClipBehavior.HARD_EDGE`.
    """

    menu_style: Optional[MenuStyle] = None
    """
    Customizes this menu's appearance.

    Value is of type
    [`MenuStyle`][flet.MenuStyle]
    """

    style: Optional[ButtonStyle] = None
    """
    Customizes this button's appearance.

    Value is of type
    [`ButtonStyle`][flet.ButtonStyle]
    """

    alignment_offset: Optional[OffsetValue] = None
    """
    The offset of the menu relative to the alignment origin determined by
    `MenuStyle.alignment` on the `style` attribute.
    """

    on_open: Optional[ControlEventHandler["SubmenuButton"]] = None
    """
    Fired when the menu is opened.
    """

    on_close: Optional[ControlEventHandler["SubmenuButton"]] = None
    """
    Fired when the menu is closed.
    """

    on_hover: Optional[ControlEventHandler["SubmenuButton"]] = None
    """
    Fired when the button is hovered.
    """

    on_focus: Optional[ControlEventHandler["SubmenuButton"]] = None
    """
    Fired when the button receives focus.
    """

    on_blur: Optional[ControlEventHandler["SubmenuButton"]] = None
    """
    Fired when this button loses focus.
    """
