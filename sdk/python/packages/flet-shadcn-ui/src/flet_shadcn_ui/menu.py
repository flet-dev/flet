from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["ContextMenu", "MenuItem", "Menubar", "MenubarItem"]


@ft.control("ShadMenuItem")
class MenuItem(ft.Control):
    """
    An item in a :class:`~flet_shadcn_ui.ContextMenu` or a
    :class:`~flet_shadcn_ui.MenubarItem` menu.

    Give it :attr:`items` to make it open a submenu instead of acting on click.
    To separate groups of items, put a :class:`~flet_shadcn_ui.Separator` with
    a small margin (e.g. `margin=ft.Margin.symmetric(vertical=4)`) between them.

    Example:
    ```python
    shad.MenuItem("Copy", trailing="Ctrl+C", on_click=copy)
    ```
    """

    content: ft.StrOrControl
    """
    The label of this item.
    """

    leading: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before :attr:`content`.
    """

    trailing: Optional[ft.StrOrControl] = None
    """
    Text or a control shown at the end of the item, typically a keyboard
    shortcut such as `"Ctrl+C"`.

    Items with :attr:`items` show a chevron instead.
    """

    items: list[ft.Control] = field(default_factory=list)
    """
    The items of a submenu that opens when this item is hovered or clicked.
    """

    inset: bool = False
    """
    Whether to indent :attr:`content` to line up with items that have a
    :attr:`leading` icon.
    """

    close_on_click: bool = True
    """
    Whether clicking this item closes the menu.
    """

    on_click: Optional[ft.ControlEventHandler["MenuItem"]] = None
    """
    Called when this item is clicked.
    """


@ft.control("ShadContextMenu")
class ContextMenu(ft.LayoutControl):
    """
    Shows a Shadcn context menu for :attr:`content`.

    How the menu opens depends on the platform:

    - Windows, macOS, Linux and desktop web: right-click. On the web the
      browser's own context menu is suppressed while this one shows.
    - Android and iOS (including the web on phones): long-press or tap.
      Because a tap opens the menu, tappable controls inside :attr:`content`
      also open it; set :attr:`open_on_tap` to `False` to avoid that.

    Example:
    ```python
    shad.ContextMenu(
        content=ft.Container(width=300, height=150, content=ft.Text("Right click")),
        items=[
            shad.MenuItem("Back", on_click=go_back),
            shad.MenuItem("Reload", trailing="Ctrl+R", on_click=reload),
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
    The menu items, usually :class:`~flet_shadcn_ui.MenuItem` and
    :class:`~flet_shadcn_ui.Separator` controls.
    """

    open_on_long_press: Optional[bool] = None
    """
    Whether a long-press on :attr:`content` opens the menu.

    If `None`, it does on Android and iOS only.
    """

    open_on_tap: Optional[bool] = None
    """
    Whether a tap (or left-click) on :attr:`content` opens the menu.

    If `None`, it does on Android and iOS only.
    """


@ft.control("ShadMenubarItem")
class MenubarItem(ft.Control):
    """
    A top-level menu of a :class:`~flet_shadcn_ui.Menubar`.
    """

    content: ft.StrOrControl
    """
    The label of the menu button.
    """

    items: list[ft.Control] = field(default_factory=list)
    """
    The menu items, usually :class:`~flet_shadcn_ui.MenuItem` and
    :class:`~flet_shadcn_ui.Separator` controls.
    """


@ft.control("ShadMenubar")
class Menubar(ft.LayoutControl):
    """
    A Shadcn menu bar: a row of menu buttons, like the menus of a desktop app.

    Example:
    ```python
    shad.Menubar(
        items=[
            shad.MenubarItem(
                "File",
                items=[
                    shad.MenuItem("New tab", trailing="Ctrl+T", on_click=new_tab),
                    shad.MenuItem(
                        "Print...", trailing="Ctrl+P", on_click=print_page
                    ),
                ],
            ),
        ]
    )
    ```
    """

    items: list[MenubarItem] = field(default_factory=list)
    """
    The menus of this bar.
    """

    select_on_hover: bool = True
    """
    Whether, once a menu is open, hovering another menu button opens that
    menu instead.
    """
