import flet as ft


def main(page: ft.Page):
    page.title = "Routes Example"

    def route_change(e):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(
                        title=ft.Text("Flet app"), bgcolor=ft.Colors.SURFACE_BRIGHT
                    ),
                    ft.Button("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(
                            title=ft.Text("Store"), bgcolor=ft.Colors.SURFACE_BRIGHT
                        ),
                        ft.Button("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


ft.run(main)
