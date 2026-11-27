"""The app shell. Every route component returns `Screen(...)`, which builds the View:
app bar, safe area, centred content column, and the tab navigation that switches
between a bottom NavigationBar (phones) and a NavigationRail (wide windows).
"""

from collections.abc import Callable
from dataclasses import dataclass

import theme

import flet as ft

CompactContext = ft.create_context(True)  # provided by App from the window width


@dataclass(frozen=True)
class Tab:
    path: str
    label: str
    icon: ft.IconData
    selected_icon: ft.IconData


# One Tab per top-level screen, each with a route in app.py. The tab navigation
# appears once there are two.
TABS = [
    Tab("/", "Expenses", ft.Icons.RECEIPT_LONG, ft.Icons.RECEIPT_LONG),
    Tab("/insights", "Insights", ft.Icons.PIE_CHART_OUTLINE, ft.Icons.PIE_CHART),
    Tab("/settings", "Settings", ft.Icons.SETTINGS, ft.Icons.SETTINGS),
]


@dataclass(frozen=True)
class PrimaryAction:
    """The screen's one main action.

    A FAB on phones, a filled button in the app bar on wide windows.
    """

    label: str
    icon: ft.IconData
    on_click: Callable


@ft.component
def Screen(
    title: str,
    body: ft.Control,
    *,
    tab: str | None = None,  # path of the tab this screen is the root of
    actions: list[ft.Control] | None = None,
    primary: PrimaryAction | None = None,
    modal: bool = False,
):
    compact = ft.use_context(CompactContext)
    page = ft.context.page
    tab_index = next((i for i, t in enumerate(TABS) if t.path == tab), None)
    show_tabs = tab_index is not None and len(TABS) > 1

    def go_to_tab(e):
        page.navigate(TABS[e.control.selected_index].path)

    async def back_to_first_tab(e):
        # Android back on a secondary tab goes to the first tab, as in most apps.
        await e.control.confirm_pop(False)
        page.navigate(TABS[0].path)

    content = ft.SafeArea(
        expand=True,
        content=ft.Container(
            expand=True,
            alignment=ft.Alignment.TOP_CENTER,
            padding=ft.Padding.symmetric(horizontal=theme.Space.L),
            content=ft.Container(
                content=body, max_width=theme.MAX_CONTENT_WIDTH, expand=True
            ),
        ),
    )
    if show_tabs and not compact:
        content = ft.Row(
            expand=True,
            spacing=0,
            controls=[
                ft.NavigationRail(
                    selected_index=tab_index,
                    label_type=ft.NavigationRailLabelType.ALL,
                    destinations=[
                        ft.NavigationRailDestination(
                            icon=t.icon, selected_icon=t.selected_icon, label=t.label
                        )
                        for t in TABS
                    ],
                    on_change=go_to_tab,
                ),
                ft.VerticalDivider(width=1),
                content,
            ],
        )

    bar_actions = list(actions or [])
    if primary and not compact:
        bar_actions.append(
            ft.FilledButton(primary.label, icon=primary.icon, on_click=primary.on_click)
        )

    return ft.View(
        # Tab roots share one key so switching tabs doesn't animate like a push.
        route="/" if tab_index is not None else ft.use_view_path(),
        # Secondary tabs: block the pop (it would close the app) and go to the
        # first tab.
        # on_confirm_pop only fires when can_pop is False.
        can_pop=not tab_index,
        on_confirm_pop=back_to_first_tab if tab_index else None,
        fullscreen_dialog=modal,
        padding=0,
        spacing=0,
        appbar=ft.AppBar(
            title=ft.Text(title),
            actions=bar_actions,
            actions_padding=ft.Padding.only(right=theme.Space.S),
        ),
        navigation_bar=ft.NavigationBar(
            selected_index=tab_index,
            destinations=[
                ft.NavigationBarDestination(
                    icon=t.icon, selected_icon=t.selected_icon, label=t.label
                )
                for t in TABS
            ],
            on_change=go_to_tab,
        )
        if show_tabs and compact
        else None,
        floating_action_button=ft.FloatingActionButton(
            icon=primary.icon, tooltip=primary.label, on_click=primary.on_click
        )
        if primary and compact
        else None,
        controls=[content],
    )
