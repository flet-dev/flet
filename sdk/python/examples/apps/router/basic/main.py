"""Basic Router — simplest example with flat routes."""

import flet as ft


@ft.component
def Home():
    return ft.Text("Home page", size=24)


@ft.component
def About():
    return ft.Text("About page", size=24)


@ft.component
def App():
    return ft.SafeArea(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Button(
                            "Home",
                            on_click=lambda: ft.context.page.navigate("/"),
                        ),
                        ft.Button(
                            "About",
                            on_click=lambda: ft.context.page.navigate("/about"),
                        ),
                    ]
                ),
                ft.Router(
                    [
                        ft.Route(index=True, component=Home),
                        ft.Route(path="about", component=About),
                    ]
                ),
            ]
        )
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
