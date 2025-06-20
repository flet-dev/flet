from typing import Optional

from flet.controls.alignment import Axis
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.types import ClipBehavior, StrOrControl

__all__ = ["MenuItemButton"]


@control("MenuItemButton")
class MenuItemButton(ConstrainedControl):
    """
    A button for use in a MenuBar or on its own, that can be activated by click or
    keyboard navigation.

    Online docs: https://flet.dev/docs/controls/menuitembutton
    """

    content: Optional[StrOrControl] = None
    """
    The child control or text to be displayed in the center of this button.

    Typically this is the button's label, using a `Text` control.
    """

    close_on_click: bool = True
    """
    Defines if the menu will be closed when the `MenuItemButton` is clicked.

    Defaults to `True`.
    """

    focus_on_hover: bool = True
    """
    Determine if hovering can request focus.

    Defaults to `True`.
    """

    leading: Optional[Control] = None
    """
    An optional control to display before the `content`.

    Typically an [`Icon`](https://flet.dev/docs/controls/icon) control.
    """

    trailing: Optional[Control] = None
    """
    An optional control to display after the `content`.

    Typically an [`Icon`](https://flet.dev/docs/controls/icon) control.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    Whether to clip the content of this control or not.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior) 
    and defaults to `ClipBehavior.NONE`.
    """

    style: Optional[ButtonStyle] = None
    """
    Customizes this button's appearance.

    Value is of type [`ButtonStyle`](https://flet.dev/docs/reference/types/buttonstyle).
    """

    semantic_label: Optional[str] = None
    """
    A string that describes the button's action to assistive technologies.
    """

    autofocus: bool = False
    """
    Whether this button should automatically request focus.

    Defaults to `False`.
    """

    overflow_axis: Axis = Axis.HORIZONTAL
    """
    The direction in which the menu item expands.

    If the menu item button is a descendent of `MenuBar`, then this property is ignored.

    Value is of type [`Axis`](https://flet.dev/docs/reference/types/axis).
    """

    on_click: OptionalControlEventHandler["MenuItemButton"] = None
    """
    Fired when the button is clicked.
    """

    on_hover: OptionalControlEventHandler["MenuItemButton"] = None
    """
    Fired when the button is hovered.
    """

    on_focus: OptionalControlEventHandler["MenuItemButton"] = None
    """
    Fired when the button receives focus.
    """

    on_blur: OptionalControlEventHandler["MenuItemButton"] = None
    """
    Fired when this button loses focus.
    """
