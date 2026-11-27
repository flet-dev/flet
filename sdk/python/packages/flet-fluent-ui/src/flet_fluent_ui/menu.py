from dataclasses import field
from typing import Optional

import flet as ft

__all__ = [
    "ContextMenu",
    "MenuBar",
    "MenuBarItem",
    "MenuFlyoutItem",
    "MenuFlyoutSeparator",
    "RadioMenuFlyoutItem",
    "ToggleMenuFlyoutItem",
]


@ft.control("FluentMenuFlyoutItem")
class MenuFlyoutItem(ft.Control):
    """
    An item of a Fluent menu: in a :class:`~flet_fluent_ui.ContextMenu`, a
    :class:`~flet_fluent_ui.MenuBarItem`, a
    :class:`~flet_fluent_ui.DropDownButton` or a
    :class:`~flet_fluent_ui.SplitButton`.

    Give it :attr:`items` to make it open a submenu instead of acting on click.

    Example:
    ```python
    fluent.MenuFlyoutItem(
        "Copy",
        leading=fluent.FluentIcons.COPY,
        trailing="Ctrl+C",
        on_click=copy,
    )
    ```
    """

    content: ft.StrOrControl
    """
    The label of this item.
    """

    leading: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before :attr:`content`.

    When an item of a menu has one, the labels of the other items are
    indented to line up with it.
    """

    trailing: Optional[ft.StrOrControl] = None
    """
    Text or a control shown at the end of this item, typically a keyboard
    shortcut such as `"Ctrl+C"`.

    Items with :attr:`items` show a chevron instead.
    """

    items: list[ft.Control] = field(default_factory=list)
    """
    The items of a submenu that opens when this item is hovered or clicked:
    :class:`~flet_fluent_ui.MenuFlyoutItem`,
    :class:`~flet_fluent_ui.ToggleMenuFlyoutItem`,
    :class:`~flet_fluent_ui.RadioMenuFlyoutItem` and
    :class:`~flet_fluent_ui.MenuFlyoutSeparator` controls.
    """

    selected: bool = False
    """
    Whether this item is highlighted as selected.
    """

    close_on_click: bool = True
    """
    Whether clicking this item closes the menu.
    """

    on_click: Optional[ft.ControlEventHandler["MenuFlyoutItem"]] = None
    """
    Called when this item is clicked.
    """


@ft.control("FluentToggleMenuFlyoutItem")
class ToggleMenuFlyoutItem(ft.Control):
    """
    A menu item that turns an option on or off, showing a checkmark when it
    is on.

    Example:
    ```python
    fluent.ToggleMenuFlyoutItem("Show status bar", value=True)
    ```
    """

    content: ft.StrOrControl
    """
    The label of this item.
    """

    value: bool = False
    """
    Whether the option is on.
    """

    trailing: Optional[ft.StrOrControl] = None
    """
    Text or a control shown at the end of this item, typically a keyboard
    shortcut.
    """

    close_on_click: bool = True
    """
    Whether clicking this item closes the menu.
    """

    on_change: Optional[ft.ControlEventHandler["ToggleMenuFlyoutItem"]] = None
    """
    Called when the user turns the option on or off.

    :attr:`value` holds the new state.
    """


@ft.control("FluentRadioMenuFlyoutItem")
class RadioMenuFlyoutItem(ft.Control):
    """
    A menu item for one of several options, of which only one can be chosen:
    the chosen one shows a dot.

    Clicking it checks it and unchecks the other radio items of the same
    :attr:`group` in the same menu.

    Example:
    ```python
    fluent.MenuFlyoutItem(
        "View",
        items=[
            fluent.RadioMenuFlyoutItem("Large icons"),
            fluent.RadioMenuFlyoutItem("Small icons", checked=True),
            fluent.RadioMenuFlyoutItem("List"),
        ],
    )
    ```
    """

    content: ft.StrOrControl
    """
    The label of this item.
    """

    checked: bool = False
    """
    Whether this option is chosen.
    """

    group: Optional[str] = None
    """
    The name of the group of options this item belongs to.

    Items with the same group in the same menu, including `None`, form one
    group. Use different groups for several sets of options in one menu.
    """

    trailing: Optional[ft.StrOrControl] = None
    """
    Text or a control shown at the end of this item, typically a keyboard
    shortcut.
    """

    close_on_click: bool = True
    """
    Whether clicking this item closes the menu.
    """

    on_change: Optional[ft.ControlEventHandler["RadioMenuFlyoutItem"]] = None
    """
    Called when the user chooses this option.

    :attr:`checked` is `True`, and the other items of the group are
    unchecked, before this is called.
    """


@ft.control("FluentMenuFlyoutSeparator")
class MenuFlyoutSeparator(ft.Control):
    """
    A line between groups of items in a Fluent menu.
    """


@ft.control("FluentContextMenu")
class ContextMenu(ft.LayoutControl):
    """
    Shows a Fluent menu where the user right-clicks or long-presses
    :attr:`content`.

    Example:
    ```python
    fluent.ContextMenu(
        content=ft.Container(width=300, height=150, content=ft.Text("Right click")),
        items=[
            fluent.MenuFlyoutItem("Back", on_click=go_back),
            fluent.MenuFlyoutItem("Reload", trailing="Ctrl+R", on_click=reload),
        ],
    )
    ```
    """

    content: ft.Control
    """
    The control that opens the menu.
    """

    items: list[ft.Control] = field(default_factory=list)
    """
    The menu items: :class:`~flet_fluent_ui.MenuFlyoutItem`,
    :class:`~flet_fluent_ui.ToggleMenuFlyoutItem`,
    :class:`~flet_fluent_ui.RadioMenuFlyoutItem` and
    :class:`~flet_fluent_ui.MenuFlyoutSeparator` controls.
    """

    on_open: Optional[ft.ControlEventHandler["ContextMenu"]] = None
    """
    Called when the menu opens.
    """

    on_dismiss: Optional[ft.ControlEventHandler["ContextMenu"]] = None
    """
    Called when the menu closes, after an item is clicked or when the user
    clicks outside it.
    """


@ft.control("FluentMenuBarItem")
class MenuBarItem(ft.Control):
    """
    A top-level menu of a :class:`~flet_fluent_ui.MenuBar`.
    """

    text: str
    """
    The label of the menu button.
    """

    items: list[ft.Control] = field(default_factory=list)
    """
    The menu items: :class:`~flet_fluent_ui.MenuFlyoutItem`,
    :class:`~flet_fluent_ui.ToggleMenuFlyoutItem`,
    :class:`~flet_fluent_ui.RadioMenuFlyoutItem` and
    :class:`~flet_fluent_ui.MenuFlyoutSeparator` controls.
    """


@ft.control("FluentMenuBar")
class MenuBar(ft.LayoutControl):
    """
    A Fluent menu bar: a row of menus, like File, Edit and View in a desktop
    app.

    Each :class:`~flet_fluent_ui.MenuBarItem` opens a menu of
    :class:`~flet_fluent_ui.MenuFlyoutItem` controls. Once a menu is open,
    hovering another menu button opens that menu instead.

    Example:
    ```python
    fluent.MenuBar(
        items=[
            fluent.MenuBarItem(
                "File",
                items=[
                    fluent.MenuFlyoutItem("New", trailing="Ctrl+N"),
                    fluent.MenuFlyoutItem("Open...", trailing="Ctrl+O"),
                ],
            ),
            fluent.MenuBarItem("Edit", items=[fluent.MenuFlyoutItem("Undo")]),
        ]
    )
    ```
    """

    items: list[MenuBarItem] = field(default_factory=list)
    """
    The menus of this bar.
    """
