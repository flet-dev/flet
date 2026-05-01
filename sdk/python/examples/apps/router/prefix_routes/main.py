"""Prefix routes — pathless layouts and path-only grouping."""

import flet as ft


@ft.component
def Users():
    return ft.Text("Users page", size=24)


@ft.component
def Settings():
    return ft.Text("Settings page", size=24)


@ft.component
def ApiUsers():
    return ft.Text("API: Users endpoint", size=24)


@ft.component
def ApiProducts():
    return ft.Text("API: Products endpoint", size=24)


@ft.component
def AdminLayout():
    """Pathless layout — wraps children without adding a path segment."""
    outlet = ft.use_route_outlet()
    return ft.Column(
        [
            ft.Container(
                content=ft.Text("ADMIN PANEL", weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.RED_100,
                padding=10,
            ),
            outlet,
        ]
    )


@ft.component
def Home():
    return ft.Text("Select a section above", size=20, italic=True)


@ft.component
def App():
    page = ft.context.page

    return ft.SafeArea(
        content=ft.Column(
            [
                ft.Text("Prefix Routes Demo", size=24),
                ft.Row(
                    [
                        ft.Button(
                            "Home",
                            on_click=lambda: page.navigate("/"),
                        ),
                        ft.Button(
                            "Users",
                            on_click=lambda: page.navigate("/users"),
                        ),
                        ft.Button(
                            "Settings",
                            on_click=lambda: page.navigate("/settings"),
                        ),
                        ft.Button(
                            "API Users",
                            on_click=lambda: page.navigate("/api/users"),
                        ),
                        ft.Button(
                            "API Products",
                            on_click=lambda: page.navigate("/api/products"),
                        ),
                    ]
                ),
                ft.Divider(),
                ft.Router(
                    [
                        ft.Route(index=True, component=Home),
                        # Pathless layout route — children share AdminLayout
                        ft.Route(
                            component=AdminLayout,
                            children=[
                                ft.Route(path="users", component=Users),
                                ft.Route(path="settings", component=Settings),
                            ],
                        ),
                        # Path-only grouping — /api prefix without a layout component
                        ft.Route(
                            path="api",
                            children=[
                                ft.Route(path="users", component=ApiUsers),
                                ft.Route(path="products", component=ApiProducts),
                            ],
                        ),
                    ]
                ),
            ]
        )
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
