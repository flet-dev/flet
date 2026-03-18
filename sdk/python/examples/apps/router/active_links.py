"""Active links — nav highlighting with is_route_active()."""

import flet as ft


@ft.component
def Home():
    return ft.Text("Home page", size=24)


@ft.component
def Products():
    return ft.Text("Products page", size=24)


@ft.component
def Settings():
    return ft.Text("Settings page", size=24)


@ft.component
def NavLink(label, path):
    """A navigation link that highlights when its path is active."""
    active = ft.is_route_active(path)
    return ft.Container(
        content=ft.Text(
            label,
            weight=ft.FontWeight.BOLD if active else ft.FontWeight.NORMAL,
            color=ft.Colors.BLUE if active else ft.Colors.ON_SURFACE,
        ),
        bgcolor=ft.Colors.BLUE_50 if active else None,
        padding=ft.Padding.symmetric(horizontal=16, vertical=8),
        border_radius=8,
        on_click=lambda: ft.context.page.navigate(path),
    )


@ft.component
def AppLayout():
    """Layout route — NavLink must be inside Router to use is_route_active()."""
    outlet = ft.use_route_outlet()
    return ft.Column(
        [
            ft.Row(
                [
                    NavLink("Home", "/"),
                    NavLink("Products", "/products"),
                    NavLink("Settings", "/settings"),
                ]
            ),
            ft.Divider(),
            outlet,
        ]
    )


@ft.component
def App():
    return ft.Router(
        [
            ft.Route(
                component=AppLayout,
                children=[
                    ft.Route(index=True, component=Home),
                    ft.Route(path="products", component=Products),
                    ft.Route(path="settings", component=Settings),
                ],
            ),
        ]
    )


ft.run(lambda page: page.render(App))
