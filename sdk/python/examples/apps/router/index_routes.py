"""Index routes — default child routes with index=True."""

import flet as ft


@ft.component
def Dashboard():
    return ft.Text("Dashboard (index route for /)", size=24)


@ft.component
def SettingsHome():
    return ft.Text("Settings Home (index route for /settings)", size=20)


@ft.component
def ProfileSettings():
    return ft.Text("Profile Settings", size=20)


@ft.component
def SecuritySettings():
    return ft.Text("Security Settings", size=20)


@ft.component
def SettingsLayout():
    outlet = ft.use_route_outlet()
    return ft.Column(
        [
            ft.Text("Settings", size=24),
            ft.Row(
                [
                    ft.Button(
                        "General",
                        on_click=lambda: ft.context.page.navigate("/settings"),
                    ),
                    ft.Button(
                        "Profile",
                        on_click=lambda: ft.context.page.navigate("/settings/profile"),
                    ),
                    ft.Button(
                        "Security",
                        on_click=lambda: ft.context.page.navigate("/settings/security"),
                    ),
                ]
            ),
            ft.Divider(),
            outlet,
        ]
    )


@ft.component
def App():
    return ft.Column(
        [
            ft.Row(
                [
                    ft.Button(
                        "Home",
                        on_click=lambda: ft.context.page.navigate("/"),
                    ),
                    ft.Button(
                        "Settings",
                        on_click=lambda: ft.context.page.navigate("/settings"),
                    ),
                ]
            ),
            ft.Divider(),
            ft.Router(
                [
                    ft.Route(index=True, component=Dashboard),
                    ft.Route(
                        path="settings",
                        component=SettingsLayout,
                        children=[
                            ft.Route(index=True, component=SettingsHome),
                            ft.Route(path="profile", component=ProfileSettings),
                            ft.Route(path="security", component=SecuritySettings),
                        ],
                    ),
                ]
            ),
        ]
    )


ft.run(lambda page: page.render(App))
