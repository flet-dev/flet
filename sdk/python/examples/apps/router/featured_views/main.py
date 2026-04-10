import flet as ft

# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------


@ft.component
def HomeContent():
    return ft.Column(
        [
            ft.Text("Home", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("Welcome to the app!", size=16),
        ]
    )


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

PROJECTS = {
    "1": "Landing Page Redesign",
    "2": "Mobile App v2",
    "3": "API Migration",
}


@ft.component
def ProjectsList():
    return ft.Column(
        [
            ft.Text("All Projects", size=24),
            *[
                ft.Button(
                    name,
                    on_click=lambda _, pid=pid: ft.context.page.navigate(
                        f"/projects/{pid}"
                    ),
                )
                for pid, name in PROJECTS.items()
            ],
        ]
    )


@ft.component
def ProjectDetails():
    params = ft.use_route_params()
    pid = params.get("pid", "?")
    name = PROJECTS.get(pid, "Unknown")
    return ft.Column(
        [
            ft.Text(name, size=24, weight=ft.FontWeight.BOLD),
            ft.Text(f"Project ID: {pid}", size=16),
            ft.Text(
                "This is where project details, tasks, and team info would go.",
                size=14,
            ),
        ]
    )


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------


@ft.component
def GeneralSettings():
    return ft.Column(
        [
            ft.Text("General Settings", size=24),
            ft.Switch(label="Dark mode"),
            ft.Switch(label="Notifications"),
            ft.Switch(label="Auto-save"),
        ]
    )


@ft.component
def AccountSettings():
    return ft.Column(
        [
            ft.Text("Account Settings", size=24),
            ft.TextField(label="Display name", value="Feodor"),
            ft.TextField(label="Email", value="feodor@example.com"),
            ft.Button("Save changes"),
        ]
    )


@ft.component
def SettingsLayout():
    """Tab navigation for settings — returns controls, not a View."""
    outlet = ft.use_route_outlet()
    return ft.Column(
        [
            ft.Text("Settings", size=28, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    ft.Button(
                        "General",
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PRIMARY_CONTAINER
                            if ft.is_route_active("/settings/general", exact=True)
                            else None,
                        ),
                        on_click=lambda: ft.context.page.navigate("/settings/general"),
                    ),
                    ft.Button(
                        "Account",
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PRIMARY_CONTAINER
                            if ft.is_route_active("/settings/account", exact=True)
                            else None,
                        ),
                        on_click=lambda: ft.context.page.navigate("/settings/account"),
                    ),
                ],
            ),
            ft.Divider(),
            ft.Container(content=outlet, expand=True),
        ],
        expand=True,
    )


# ---------------------------------------------------------------------------
# Root layout with NavigationRail
# ---------------------------------------------------------------------------

NAV_ROUTES = ["/", "/projects", "/settings/general"]


@ft.component
def RootLayout():
    """Root layout — returns a View with NavigationRail + outlet."""
    outlet = ft.use_route_outlet()

    selected = 0
    if ft.is_route_active("/projects"):
        selected = 1
    elif ft.is_route_active("/settings"):
        selected = 2

    def on_nav_change(e):
        ft.context.page.navigate(NAV_ROUTES[e.control.selected_index])

    return ft.View(
        route="/",  # fixed key — no transition animation between top-level pages
        can_pop=False,
        controls=[
            ft.Row(
                [
                    ft.NavigationRail(
                        selected_index=selected,
                        label_type=ft.NavigationRailLabelType.ALL,
                        destinations=[
                            ft.NavigationRailDestination(
                                icon=ft.Icons.HOME_OUTLINED,
                                selected_icon=ft.Icons.HOME,
                                label="Home",
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.FOLDER_OUTLINED,
                                selected_icon=ft.Icons.FOLDER,
                                label="Projects",
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.SETTINGS_OUTLINED,
                                selected_icon=ft.Icons.SETTINGS,
                                label="Settings",
                            ),
                        ],
                        on_change=on_nav_change,
                    ),
                    ft.VerticalDivider(width=1),
                    ft.Container(content=outlet, expand=True, padding=20),
                ],
                expand=True,
            ),
        ],
    )


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------


@ft.component
def App():
    return ft.Router(
        [
            ft.Route(
                component=RootLayout,
                outlet=True,
                children=[
                    ft.Route(index=True, component=HomeContent),
                    ft.Route(
                        path="projects",
                        component=ProjectsList,
                        children=[
                            ft.Route(path=":pid", component=ProjectDetails),
                        ],
                    ),
                    ft.Route(
                        path="settings",
                        component=SettingsLayout,
                        outlet=True,
                        children=[
                            ft.Route(path="general", component=GeneralSettings),
                            ft.Route(path="account", component=AccountSettings),
                        ],
                    ),
                ],
            ),
        ],
        manage_views=True,
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render_views(App))
