from dataclasses import field
from typing import Optional

import flet as ft
from flet_fluent_ui.types import FlyoutPlacementMode

__all__ = ["DropDownButton", "SplitButton"]


@ft.control("FluentDropDownButton")
class DropDownButton(ft.LayoutControl):
    """
    A Fluent button with a chevron that opens a menu of
    :class:`~flet_fluent_ui.MenuFlyoutItem` controls.

    Example:
    ```python
    fluent.DropDownButton(
        "Sort by",
        items=[
            fluent.MenuFlyoutItem("Name"),
            fluent.MenuFlyoutItem("Date modified"),
            fluent.MenuFlyoutItem("Size"),
        ],
    )
    ```
    """

    content: Optional[ft.StrOrControl] = None
    """
    The button's label.
    """

    items: list[ft.Control] = field(default_factory=list)
    """
    The menu items: :class:`~flet_fluent_ui.MenuFlyoutItem`,
    :class:`~flet_fluent_ui.ToggleMenuFlyoutItem` and
    :class:`~flet_fluent_ui.MenuFlyoutSeparator` controls.

    The button is disabled while there are none.
    """

    leading: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before :attr:`content`.
    """

    placement: FlyoutPlacementMode = FlyoutPlacementMode.BOTTOM_CENTER
    """
    Where the menu opens relative to the button.
    """

    autofocus: bool = False
    """
    Whether this button should be focused on initial display.
    """

    on_open: Optional[ft.ControlEventHandler["DropDownButton"]] = None
    """
    Called when the menu opens.
    """

    on_dismiss: Optional[ft.ControlEventHandler["DropDownButton"]] = None
    """
    Called when the menu closes, after an item is clicked or when the user
    clicks outside it.
    """


@ft.control("FluentSplitButton")
class SplitButton(ft.LayoutControl):
    """
    A Fluent split button: a button for the main action, and a chevron next to
    it that opens a menu of related actions.

    Example:
    ```python
    fluent.SplitButton(
        "Paste",
        on_click=paste,
        items=[
            fluent.MenuFlyoutItem("Paste as text"),
            fluent.MenuFlyoutItem("Paste with formatting"),
        ],
    )
    ```
    """

    content: ft.StrOrControl
    """
    The label of the main part of the button.
    """

    items: list[ft.Control] = field(default_factory=list)
    """
    The menu items: :class:`~flet_fluent_ui.MenuFlyoutItem`,
    :class:`~flet_fluent_ui.ToggleMenuFlyoutItem` and
    :class:`~flet_fluent_ui.MenuFlyoutSeparator` controls.
    """

    flyout: Optional[ft.Control] = None
    """
    A control shown in the popup instead of a menu of :attr:`items`, for
    example a grid of colors to pick from.
    """

    checked: Optional[bool] = None
    """
    Whether the button is on, for a toggle split button.

    If `None`, this is a regular split button. If `True` or `False`, clicking
    the main part turns the button on or off, and it is filled with the
    accent color while it is on.
    """

    on_click: Optional[ft.ControlEventHandler["SplitButton"]] = None
    """
    Called when the main part of the button is clicked.
    """

    on_change: Optional[ft.ControlEventHandler["SplitButton"]] = None
    """
    Called when the user turns a toggle split button on or off.

    :attr:`checked` holds the new state.
    """
