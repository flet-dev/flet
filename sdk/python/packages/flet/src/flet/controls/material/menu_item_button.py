from typing import Optional

from flet.controls.alignment import Axis
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ClipBehavior, StrOrControl

__all__ = ["MenuItemButton"]


@control("MenuItemButton")
class MenuItemButton(LayoutControl):
    """
    A button for use in a MenuBar or on its own, that can be activated by click or
    keyboard navigation.

    ```python
    ft.Row(
        controls=[
            ft.MenuItemButton(
                content=ft.Text("Yes"),
                on_click=lambda e: print("yes"),
            ),
            ft.MenuItemButton(
                content=ft.Text("No"),
                on_click=lambda e: print("no"),
            ),
            ft.MenuItemButton(
                content=ft.Text("Maybe"),
                on_click=lambda e: print("maybe"),
            ),
        ],
    )
    ```

    """

    content: Optional[StrOrControl] = None
    """
    The child control or text to be displayed in the center of this button.

    Typically this is the button's label, using a `Text` control.
    """

    close_on_click: bool = True
    """
    Defines if the menu will be closed when the `MenuItemButton` is clicked.
    """

    focus_on_hover: bool = True
    """
    Determine if hovering can request focus.
    """

    leading: Optional[Control] = None
    """
    An optional control to display before the `content`.

    Typically an [`Icon`][flet.] control.
    """

    trailing: Optional[Control] = None
    """
    An optional control to display after the `content`.

    Typically an [`Icon`][flet.] control.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    Whether to clip the content of this control or not.
    """

    style: Optional[ButtonStyle] = None
    """
    Customizes this button's appearance.
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
    """

    on_click: Optional[ControlEventHandler["MenuItemButton"]] = None
    """
    Called when the button is clicked.If not defined the button will be disabled.
    """

    on_hover: Optional[ControlEventHandler["MenuItemButton"]] = None
    """
    Called when the button is hovered.
    """

    on_focus: Optional[ControlEventHandler["MenuItemButton"]] = None
    """
    Called when the button receives focus.
    """

    on_blur: Optional[ControlEventHandler["MenuItemButton"]] = None
    """
    Called when this button loses focus.
    """
