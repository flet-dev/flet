from dataclasses import field
from typing import Optional

import flet as ft
from flet_fluent_ui.types import PaneDisplayMode

__all__ = [
    "NavigationView",
    "PageHeader",
    "PaneItem",
    "PaneItemHeader",
    "PaneItemSeparator",
    "ScaffoldPage",
]


@ft.control("FluentPaneItem")
class PaneItem(ft.Control):
    """
    An item of the pane of a :class:`~flet_fluent_ui.NavigationView`.

    An item with :attr:`content` is a page: clicking it selects it and shows
    its content. An item without content is an action, which only calls
    :attr:`on_click`. An item with :attr:`items` expands to show them.

    Example:
    ```python
    fluent.PaneItem(
        "Inbox",
        icon=fluent.FluentIcons.MAIL,
        content=ft.Text("Your messages"),
    )
    ```
    """

    title: ft.StrOrControl
    """
    The label of this item.
    """

    icon: Optional[ft.IconDataOrControl] = None
    """
    The icon of this item, the only part shown in a compact pane.
    """

    content: Optional[ft.Control] = None
    """
    The control shown next to the pane while this item is selected.

    Usually a :class:`~flet_fluent_ui.ScaffoldPage`.
    """

    items: list[ft.Control] = field(default_factory=list)
    """
    Items shown below this one when it is expanded:
    :class:`~flet_fluent_ui.PaneItem`,
    :class:`~flet_fluent_ui.PaneItemHeader` and
    :class:`~flet_fluent_ui.PaneItemSeparator` controls.
    """

    expanded: bool = False
    """
    Whether :attr:`items` are shown when the view first appears.
    """

    info_badge: Optional[ft.Control] = None
    """
    A badge shown at the end of the item, usually an
    :class:`~flet_fluent_ui.InfoBadge`.
    """

    trailing: Optional[ft.Control] = None
    """
    A control shown at the end of the item.
    """

    on_click: Optional[ft.ControlEventHandler["PaneItem"]] = None
    """
    Called when this item is clicked.
    """


@ft.control("FluentPaneItemHeader")
class PaneItemHeader(ft.Control):
    """
    A heading above a group of items in the pane of a
    :class:`~flet_fluent_ui.NavigationView`.

    It is hidden in a compact pane.
    """

    content: ft.StrOrControl
    """
    The text of the heading.
    """


@ft.control("FluentPaneItemSeparator")
class PaneItemSeparator(ft.Control):
    """
    A line between groups of items in the pane of a
    :class:`~flet_fluent_ui.NavigationView`.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the line.
    """

    thickness: Optional[ft.Number] = None
    """
    The thickness of the line.
    """


@ft.control("FluentNavigationView")
class NavigationView(ft.LayoutControl):
    """
    A Fluent navigation view: the layout of a Windows app, with a pane of
    pages to navigate between and the content of the selected page.

    The view fills the space it is given: give it a size or `expand=True`.

    Example:
    ```python
    fluent.NavigationView(
        expand=True,
        selected_index=0,
        items=[
            fluent.PaneItem(
                "Home",
                icon=fluent.FluentIcons.HOME,
                content=fluent.ScaffoldPage(content=ft.Text("Welcome home")),
            ),
            fluent.PaneItem(
                "Mail",
                icon=fluent.FluentIcons.MAIL,
                content=fluent.ScaffoldPage(content=ft.Text("No new mail")),
            ),
        ],
        footer_items=[
            fluent.PaneItem(
                "Settings",
                icon=fluent.FluentIcons.SETTINGS,
                content=fluent.ScaffoldPage(content=ft.Text("Settings")),
            ),
        ],
    )
    ```
    """

    items: list[ft.Control] = field(default_factory=list)
    """
    The items at the top of the pane: :class:`~flet_fluent_ui.PaneItem`,
    :class:`~flet_fluent_ui.PaneItemHeader` and
    :class:`~flet_fluent_ui.PaneItemSeparator` controls.
    """

    footer_items: list[ft.Control] = field(default_factory=list)
    """
    The items at the bottom of the pane, such as Settings.
    """

    selected_index: Optional[int] = None
    """
    The index of the selected page.

    Pages are the :class:`~flet_fluent_ui.PaneItem` controls that have
    :attr:`~flet_fluent_ui.PaneItem.content`, counted in the order they
    appear: :attr:`items` (including the items inside expandable items),
    then :attr:`footer_items`. Headers, separators and items without content
    are not counted.

    If `None`, no page is selected and the content area is empty.
    """

    display_mode: PaneDisplayMode = PaneDisplayMode.AUTO
    """
    How the pane is shown.
    """

    header: Optional[ft.StrOrControl] = None
    """
    A title or control shown at the top of the pane.
    """

    on_change: Optional[ft.ControlEventHandler["NavigationView"]] = None
    """
    Called when the user selects another page.

    :attr:`selected_index` holds the index of the new page.
    """


@ft.control("FluentPageHeader")
class PageHeader(ft.LayoutControl):
    """
    The header of a :class:`~flet_fluent_ui.ScaffoldPage`: the page title,
    and commands at the end.

    Example:
    ```python
    fluent.PageHeader(
        title="Inbox",
        command_bar=fluent.CommandBar(
            primary_items=[
                fluent.CommandBarButton(icon=fluent.FluentIcons.ADD, content="New")
            ]
        ),
    )
    ```
    """

    title: Optional[ft.StrOrControl] = None
    """
    The title of the page, shown in large text.
    """

    leading: Optional[ft.Control] = None
    """
    A control shown before :attr:`title`, such as a back button.
    """

    command_bar: Optional[ft.Control] = None
    """
    Commands shown at the end of the header, usually a
    :class:`~flet_fluent_ui.CommandBar`.
    """


@ft.control("FluentScaffoldPage")
class ScaffoldPage(ft.LayoutControl):
    """
    A Fluent page: a header, content and footer, with Fluent page margins.

    Use it as the :attr:`~flet_fluent_ui.PaneItem.content` of the pages of a
    :class:`~flet_fluent_ui.NavigationView`.

    Example:
    ```python
    fluent.ScaffoldPage(
        header=fluent.PageHeader(title="Inbox"),
        content=ft.Text("No new messages"),
    )
    ```
    """

    content: Optional[ft.Control] = None
    """
    The content of the page, which fills the space below :attr:`header`.
    """

    header: Optional[ft.Control] = None
    """
    The header of the page, usually a :class:`~flet_fluent_ui.PageHeader`.
    """

    footer: Optional[ft.Control] = None
    """
    A control shown at the bottom of the page.
    """

    padding: Optional[ft.PaddingValue] = None
    """
    The space around :attr:`content`.

    If `None`, Fluent's page margins are used, which are smaller on narrow
    pages.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The background color of the page.

    If `None`, the page is transparent inside a
    :class:`~flet_fluent_ui.NavigationView`, and otherwise uses the Fluent
    page background color.
    """
