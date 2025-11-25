import flet as ft


def main(page: ft.Page):
    page.title = "Drawer navigation"

    async def handle_change(e):
        if e.control.selected_index == 0:
            await page.push_route("/")
        elif e.control.selected_index == 1:
            await page.push_route("/store")
        elif e.control.selected_index == 2:
            await page.push_route("/about")

    def create_drawer(selected_index=0):
        return ft.NavigationDrawer(
            selected_index=selected_index,
            on_change=handle_change,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Home",
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.HOME),
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="Store",
                    icon=ft.Icon(ft.Icons.STORE_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.STORE),
                ),
                ft.NavigationDrawerDestination(
                    label="About",
                    icon=ft.Icon(ft.Icons.PHONE_OUTLINED),
                    selected_icon=ft.Icons.PHONE,
                ),
            ],
        )

    async def show_drawer():
        await page.show_drawer()

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(
                        title=ft.Text("Home", expand=True),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        leading=ft.IconButton(ft.Icons.MENU, on_click=show_drawer),
                    ),
                    ft.Text("Welcome to Home Page"),
                ],
                drawer=create_drawer(selected_index=0)
                if page.route == "/"
                else None,  # add drawer only if home page is shown
            )
        )

        if page.route == "/store":
            page.views.append(
                ft.View(
                    route="/store",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Store", expand=True),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            leading=ft.IconButton(ft.Icons.MENU, on_click=show_drawer),
                            automatically_imply_leading=False,
                        ),
                        ft.Text("Welcome to Store Page"),
                        ft.Button("Go About", on_click=lambda _: page.go("/about")),
                    ],
                    drawer=create_drawer(selected_index=1),
                )
            )

        if page.route == "/about":
            page.views.append(
                ft.View(
                    route="/about",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("About", expand=True),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            leading=ft.IconButton(ft.Icons.MENU, on_click=show_drawer),
                            automatically_imply_leading=False,
                        ),
                        ft.Text("Welcome to About Page"),
                        ft.Button("Go Store", on_click=lambda _: page.go("/store")),
                    ],
                    drawer=create_drawer(selected_index=2),
                )
            )

    async def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change(page.route)


if __name__ == "__main__":
    ft.run(main)
