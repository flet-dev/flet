from dataclasses import field
from typing import Optional

import flet as ft
from flet_fluent_ui.types import TreeViewSelectionMode

__all__ = ["TreeView", "TreeViewItem"]


@ft.control("FluentTreeViewItem")
class TreeViewItem(ft.Control):
    """
    An item of a :class:`~flet_fluent_ui.TreeView`, with optional subitems.

    Example:
    ```python
    fluent.TreeViewItem(
        "Documents",
        leading=fluent.FluentIcons.FOLDER,
        items=[fluent.TreeViewItem("Report.docx")],
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
    """

    items: list["TreeViewItem"] = field(default_factory=list)
    """
    The subitems of this item, shown below it when it is expanded.
    """

    expanded: bool = False
    """
    Whether the subitems are shown.

    Updated when the user expands or collapses this item.
    """

    selected: Optional[bool] = False
    """
    Whether this item is selected.

    Updated when the user selects items. In
    :attr:`~flet_fluent_ui.TreeViewSelectionMode.MULTIPLE` mode, an item with
    some of its subitems selected is `None`.
    """

    on_click: Optional[ft.ControlEventHandler["TreeViewItem"]] = None
    """
    Called when this item is clicked.
    """

    on_expand_change: Optional[ft.ControlEventHandler["TreeViewItem"]] = None
    """
    Called when the user expands or collapses this item.

    :attr:`expanded` holds the new state.
    """


@ft.control("FluentTreeView")
class TreeView(ft.LayoutControl):
    """
    A Fluent tree view: a list of items that can be expanded to show their
    subitems, like the folders of a file explorer.

    Example:
    ```python
    fluent.TreeView(
        items=[
            fluent.TreeViewItem(
                "Documents",
                expanded=True,
                items=[
                    fluent.TreeViewItem("Report.docx"),
                    fluent.TreeViewItem("Budget.xlsx"),
                ],
            ),
            fluent.TreeViewItem("Pictures", items=[fluent.TreeViewItem("Cat.png")]),
        ]
    )
    ```
    """

    items: list[TreeViewItem] = field(default_factory=list)
    """
    The top-level items.
    """

    selection_mode: TreeViewSelectionMode = TreeViewSelectionMode.NONE
    """
    How items can be selected.
    """

    on_selection_change: Optional[ft.ControlEventHandler["TreeView"]] = None
    """
    Called when the user selects or deselects items.

    The :attr:`~flet_fluent_ui.TreeViewItem.selected` property of every item
    is updated before this is called.
    """
