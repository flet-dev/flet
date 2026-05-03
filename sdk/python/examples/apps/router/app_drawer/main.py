import asyncio

import flet as ft

APPS = {
    "1": "Acme Web",
    "2": "Beta API",
    "3": "Gamma Mobile",
}


@ft.component
def Home():
    return ft.View(
        route="/",
        can_pop=False,
        appbar=ft.AppBar(title=ft.Text("Home")),
        controls=[
            ft.Text("Welcome", size=24),
            ft.Button(
                "Browse Apps",
                on_click=lambda: ft.context.page.navigate("/apps"),
            ),
        ],
    )


@ft.component
def AppsList():
    return ft.View(
        route="/apps",
        appbar=ft.AppBar(title=ft.Text("Apps")),
        controls=[
            ft.Text("Your apps", size=24),
            *[
                ft.Button(
                    name,
                    data=app_id,
                    on_click=lambda e: ft.context.page.navigate(
                        f"/apps/{e.control.data}"
                    ),
                )
                for app_id, name in APPS.items()
            ],
        ],
    )


@ft.component
def GeneralTab():
    params = ft.use_route_params()
    return ft.Column(
        [
            ft.Text("General Settings", size=20),
            ft.TextField(label="App name", value=APPS.get(params["app_id"], "")),
            ft.Switch(label="Public"),
            ft.Switch(label="Maintenance mode"),
        ]
    )


@ft.component
def PermissionsTab():
    return ft.Column(
        [
            ft.Text("Permissions", size=20),
            ft.Switch(label="Read access for guests"),
            ft.Switch(label="Allow API tokens"),
            ft.Switch(label="Require 2FA for admins"),
        ]
    )


@ft.component
def AppDetails():
    """App details view with a settings drawer.

    The drawer's open state and selected tab are derived from the URL:
    - /apps/:app_id              — drawer closed
    - /apps/:app_id/settings/general      — drawer open, General tab
    - /apps/:app_id/settings/permissions  — drawer open, Permissions tab
    """
    params = ft.use_route_params()
    app_id = params["app_id"]
    name = APPS.get(app_id, "Unknown")

    # If a settings child route matched, this is non-None — the drawer
    # should be open and `outlet` is the rendered tab content.
    outlet = ft.use_route_outlet()
    drawer_open = outlet is not None

    page = ft.context.page

    def on_dismiss(e):
        # User swiped the drawer away — sync URL back to /apps/:app_id
        page.navigate(f"/apps/{app_id}")

    location = ft.use_route_location()
    tab_routes = [
        f"/apps/{app_id}/settings/general",
        f"/apps/{app_id}/settings/permissions",
    ]
    # Pure string comparison — don't call is_route_active() here because
    # it uses a context hook and varying call counts break hook ordering.
    route_tab = next(
        (i for i, r in enumerate(tab_routes) if location == r),
        0,
    )
    selected_tab, set_selected_tab = ft.use_state(route_tab)

    def sync_tab():
        if route_tab != selected_tab:
            set_selected_tab(route_tab)

    ft.use_effect(sync_tab, dependencies=[location])

    def on_tab_change(e):
        idx = e.control.selected_index
        # Skip programmatic echoes: Tabs fires on_change after its own
        # animation completes, including when we set selected_index via
        # state. If idx matches our current state, it's not a user tap.
        if idx == selected_tab:
            return
        set_selected_tab(idx)
        page.navigate(tab_routes[idx])

    drawer = ft.NavigationDrawer(
        on_dismiss=on_dismiss,
        controls=[
            ft.Container(
                content=ft.Text("App settings", size=22, weight=ft.FontWeight.BOLD),
                padding=20,
            ),
            ft.Tabs(
                length=2,
                selected_index=selected_tab,
                on_change=on_tab_change,
                content=ft.TabBar(
                    scrollable=False,
                    tabs=[
                        ft.Tab(label="General"),
                        ft.Tab(label="Permissions"),
                    ],
                ),
            ),
            ft.Container(content=outlet, padding=20, expand=True),
        ],
    )

    # Imperatively open/close the drawer when the route changes.
    def sync_drawer():
        if drawer_open:
            asyncio.create_task(page.show_end_drawer())
        else:
            asyncio.create_task(page.close_end_drawer())

    ft.use_effect(sync_drawer, dependencies=[drawer_open])

    return ft.View(
        route=f"/apps/{app_id}",
        appbar=ft.AppBar(
            title=ft.Text(name),
            actions=[
                ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    tooltip="Settings",
                    on_click=lambda: page.navigate(f"/apps/{app_id}/settings/general"),
                ),
            ],
        ),
        end_drawer=drawer,
        controls=[
            ft.Text(name, size=28, weight=ft.FontWeight.BOLD),
            ft.Text(f"App ID: {app_id}", size=16),
            ft.Text("Welcome to the app dashboard.", size=14),
            ft.Divider(height=30),
            ft.Button(
                "Open Settings",
                icon=ft.Icons.SETTINGS,
                on_click=lambda: page.navigate(f"/apps/{app_id}/settings/general"),
            ),
            ft.Button(
                "Direct link to Permissions",
                icon=ft.Icons.SECURITY,
                on_click=lambda: page.navigate(f"/apps/{app_id}/settings/permissions"),
            ),
        ],
    )


@ft.component
def App():
    return ft.Router(
        [
            ft.Route(
                component=Home,
                children=[
                    ft.Route(
                        path="apps",
                        component=AppsList,
                        children=[
                            ft.Route(
                                path=":app_id",
                                component=AppDetails,
                                outlet=True,
                                children=[
                                    ft.Route(
                                        path="settings/general",
                                        component=GeneralTab,
                                    ),
                                    ft.Route(
                                        path="settings/permissions",
                                        component=PermissionsTab,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
        manage_views=True,
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render_views(App))
