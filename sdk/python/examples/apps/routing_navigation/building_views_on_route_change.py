import flet as ft


def main(page: ft.Page):
    page.title = "Routes Example"

    print("Initial route:", page.route)

    async def open_mail_settings(e):
        await page.push_route("/settings/mail")

    async def open_settings(e):
        await page.push_route("/settings")

    def route_change():
        print("Route change:", page.route)
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(title=ft.Text("Flet app")),
                    ft.Button("Go to settings", on_click=open_settings),
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
                        ft.Button(
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

    async def view_pop(e):
        if e.view is not None:
            print("View pop:", e.view)
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
