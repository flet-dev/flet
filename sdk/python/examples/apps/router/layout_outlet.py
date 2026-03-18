"""Layout routes with Outlet — shared layout wrapping child routes."""

import flet as ft


@ft.component
def Home():
    return ft.Text("Welcome home!", size=24)


@ft.component
def About():
    return ft.Text("About us", size=24)


@ft.component
def Contact():
    return ft.Text("Contact page", size=24)


@ft.component
def AppLayout():
    outlet = ft.use_route_outlet()
    return ft.Column(
        [
            ft.AppBar(
                title=ft.Text("My App"),
                bgcolor=ft.Colors.SURFACE_BRIGHT,
                actions=[
                    ft.Button(
                        "Home",
                        on_click=lambda: ft.context.page.navigate("/"),
                    ),
                    ft.Button(
                        "About",
                        on_click=lambda: ft.context.page.navigate("/about"),
                    ),
                    ft.Button(
                        "Contact",
                        on_click=lambda: ft.context.page.navigate("/contact"),
                    ),
                ],
            ),
            ft.Container(content=outlet, padding=20, expand=True),
            ft.Text("Footer - (c) 2026", text_align=ft.TextAlign.CENTER),
        ],
        expand=True,
    )


@ft.component
def App():
    return ft.Router(
        [
            ft.Route(
                component=AppLayout,
                children=[
                    ft.Route(index=True, component=Home),
                    ft.Route(path="about", component=About),
                    ft.Route(path="contact", component=Contact),
                ],
            ),
        ]
    )


ft.run(lambda page: page.render(App))
