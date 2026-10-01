from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["Breadcrumb", "BreadcrumbEllipsis", "BreadcrumbItem"]


@ft.control("ShadBreadcrumbItem")
class BreadcrumbItem(ft.Control):
    """
    One step in a :class:`~flet_shadcn_ui.Breadcrumb`.

    An item with an :attr:`on_click` handler is shown as a link. Without one it
    is plain text, which suits the last item (the current page).
    """

    content: ft.StrOrControl
    """
    The label of this item.

    If a string is provided, it is wrapped in a :class:`~flet.Text` control.
    """

    on_click: Optional[ft.ControlEventHandler["BreadcrumbItem"]] = None
    """
    Called when this item is clicked.
    """


@ft.control("ShadBreadcrumbEllipsis")
class BreadcrumbEllipsis(ft.Control):
    """
    An ellipsis (`…`) in a :class:`~flet_shadcn_ui.Breadcrumb`, standing in for
    steps that are not shown.
    """


@ft.control("ShadBreadcrumb")
class Breadcrumb(ft.LayoutControl):
    """
    A Shadcn breadcrumb: the path to the current page, as a row of links.

    Example:
    ```python
    shad.Breadcrumb(
        items=[
            shad.BreadcrumbItem("Home", on_click=go_home),
            shad.BreadcrumbItem("Components", on_click=go_components),
            shad.BreadcrumbItem("Breadcrumb"),
        ]
    )
    ```
    """

    items: list[ft.Control] = field(default_factory=list)
    """
    The steps of the path, usually :class:`~flet_shadcn_ui.BreadcrumbItem` and
    :class:`~flet_shadcn_ui.BreadcrumbEllipsis` controls.

    The last item is highlighted as the current page.
    """

    separator: Optional[ft.IconDataOrControl] = None
    """
    The icon or control shown between items.

    If `None`, a chevron is shown.
    """

    spacing: Optional[ft.Number] = None
    """
    The space on each side of :attr:`separator`, and between wrapped lines.

    If `None`, defaults to `10`.
    """
