import flet as ft


def main(page: ft.Page):
    page.title = "Routes Example"

    print("Initial route:", page.route)

    def route_change(e):
        print("Route change:", e.route)
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(title=ft.Text("Flet app")),
                    ft.ElevatedButton("Go to settings", on_click=open_settings),
                ],
            )
        )
        if page.route == "/settings" or page.route == "/settings/mail":
            page.views.append(
                ft.View(
                    route="/settings",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Settings"),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        ),
                        ft.Text("Settings!", theme_style=ft.TextThemeStyle.BODY_MEDIUM),
                        ft.ElevatedButton(
                            content="Go to mail settings",
                            on_click=open_mail_settings,
                        ),
                    ],
                )
            )
        if page.route == "/settings/mail":
            page.views.append(
                ft.View(
                    route="/settings/mail",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Mail Settings"),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        ),
                        ft.Text("Mail settings!"),
                    ],
                )
            )
        page.update()

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    def open_mail_settings(e):
        page.go("/settings/mail")

    def open_settings(e):
        page.go("/settings")

    page.go(page.route)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
