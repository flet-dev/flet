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
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text("My App", size=20, weight=ft.FontWeight.BOLD),
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
                    ]
                ),
                bgcolor=ft.Colors.SURFACE_BRIGHT,
                padding=10,
            ),
            ft.Container(content=outlet, padding=20),
            ft.Text("Footer - (c) 2026", text_align=ft.TextAlign.CENTER),
        ],
    )


@ft.component
def App():
    return ft.SafeArea(
        content=ft.Router(
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
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
