from dataclasses import field
from typing import Optional

import flet as ft
from flet_fluent_ui.types import CloseButtonVisibilityMode, TabWidthBehavior

__all__ = ["Tab", "TabView"]


@ft.control("FluentTab")
class Tab(ft.Control):
    """
    A tab of a :class:`~flet_fluent_ui.TabView`.

    Example:
    ```python
    fluent.Tab(
        "Document 1",
        icon=fluent.FluentIcons.DOCUMENT,
        content=ft.Text("Contents of document 1"),
        on_close=close_tab,
    )
    ```
    """

    text: ft.StrOrControl
    """
    The label of the tab.
    """

    content: ft.Control
    """
    The control shown below the tabs while this tab is selected.
    """

    icon: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before :attr:`text`.
    """

    on_close: Optional[ft.ControlEventHandler["Tab"]] = None
    """
    Called when the user closes this tab, with its close button or with
    Ctrl+W (Cmd+W on macOS) while it is selected.

    The tab has a close button only if this is set. The tab is not removed
    automatically: remove it from :attr:`flet_fluent_ui.TabView.tabs` here.
    """


@ft.control("FluentTabView")
class TabView(ft.LayoutControl):
    """
    A Fluent tab view: a row of tabs, like the tabs of a browser, above the
    content of the selected tab.

    The user can select tabs with Ctrl+1 to Ctrl+9, and close the selected
    tab with Ctrl+W or Ctrl+F4 (Cmd instead of Ctrl on macOS).

    Example:
    ```python
    fluent.TabView(
        height=200,
        tabs=[
            fluent.Tab("Home", content=ft.Text("Welcome home")),
            fluent.Tab("Settings", content=ft.Text("Your settings")),
        ],
    )
    ```
    """

    tabs: list[Tab] = field(default_factory=list)
    """
    The tabs.
    """

    selected_index: int = 0
    """
    The index of the selected tab in :attr:`tabs`.
    """

    tab_width_behavior: TabWidthBehavior = TabWidthBehavior.EQUAL
    """
    How wide the tabs are.
    """

    close_button_visibility: CloseButtonVisibilityMode = (
        CloseButtonVisibilityMode.ALWAYS
    )
    """
    When the close buttons of tabs that have an
    :attr:`~flet_fluent_ui.Tab.on_close` handler are shown.
    """

    show_scroll_buttons: bool = True
    """
    Whether buttons to scroll the tabs are shown when they don't fit.
    """

    header: Optional[ft.Control] = None
    """
    A control shown before the tabs.
    """

    footer: Optional[ft.Control] = None
    """
    A control shown after the tabs and the new tab button.
    """

    on_change: Optional[ft.ControlEventHandler["TabView"]] = None
    """
    Called when the user selects another tab.

    :attr:`selected_index` holds the index of the new tab.
    """

    on_add: Optional[ft.ControlEventHandler["TabView"]] = None
    """
    Called when the user clicks the "+" button after the tabs, or presses
    Ctrl+T (Cmd+T on macOS).

    The "+" button is shown only if this is set. Add the new tab to
    :attr:`tabs` here.
    """

    on_reorder: Optional[ft.EventHandler[ft.OnReorderEvent]] = None
    """
    Called when the user drags a tab to another position.

    Tabs can be dragged only if this is set. :attr:`tabs` is not reordered
    automatically: move the tab from
    :attr:`~flet.OnReorderEvent.old_index` to
    :attr:`~flet.OnReorderEvent.new_index` here.
    """
