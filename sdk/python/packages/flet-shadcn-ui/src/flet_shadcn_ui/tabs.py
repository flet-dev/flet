from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["Tab", "Tabs"]


@ft.control("ShadTab")
class Tab(ft.Control):
    """
    One tab in :class:`~flet_shadcn_ui.Tabs`.
    """

    value: str
    """
    The value the tabs take when this tab is selected.
    """

    label: ft.StrOrControl
    """
    The label of the tab button.
    """

    content: Optional[ft.Control] = None
    """
    The control shown below the tab bar while this tab is selected.
    """

    icon: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before :attr:`label`.
    """


@ft.control("ShadTabs")
class Tabs(ft.LayoutControl):
    """
    Shadcn tabs: a bar of tab buttons, showing the content of the selected tab
    below it.

    Example:
    ```python
    shad.Tabs(
        value="account",
        tabs=[
            shad.Tab(value="account", label="Account", content=ft.Text("...")),
            shad.Tab(value="password", label="Password", content=ft.Text("...")),
        ],
    )
    ```
    """

    tabs: list[Tab] = field(default_factory=list)
    """
    The tabs.
    """

    value: Optional[str] = None
    """
    The :attr:`~flet_shadcn_ui.Tab.value` of the selected tab.

    If `None`, the first tab is selected.
    """

    gap: Optional[ft.Number] = None
    """
    The space between the tab bar and the selected tab's content.

    If `None`, defaults to `8`.
    """

    on_change: Optional[ft.ControlEventHandler["Tabs"]] = None
    """
    Called when the selected tab changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new :attr:`value`.
    """
