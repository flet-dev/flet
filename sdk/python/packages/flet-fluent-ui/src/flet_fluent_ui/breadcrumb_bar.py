from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["BreadcrumbBar", "BreadcrumbItem"]


@ft.control("FluentBreadcrumbItem")
class BreadcrumbItem(ft.Control):
    """
    An item of a :class:`~flet_fluent_ui.BreadcrumbBar`.
    """

    content: ft.StrOrControl
    """
    The label of this item.
    """

    on_click: Optional[ft.ControlEventHandler["BreadcrumbItem"]] = None
    """
    Called when this item is clicked.
    """


@ft.control("FluentBreadcrumbBar")
class BreadcrumbBar(ft.LayoutControl):
    """
    A Fluent breadcrumb bar: the path to the current location, such as a
    folder, with an item for each level.

    Items that don't fit go into a "..." menu at the start of the bar.

    Example:
    ```python
    fluent.BreadcrumbBar(
        items=[
            fluent.BreadcrumbItem("Home"),
            fluent.BreadcrumbItem("Documents"),
            fluent.BreadcrumbItem("Design"),
        ]
    )
    ```
    """

    items: list[BreadcrumbItem] = field(default_factory=list)
    """
    The items, from the top level to the current location.
    """
