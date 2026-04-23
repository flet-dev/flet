import flet as ft


@ft.component
def App():
    selected, set_selected = ft.use_state(0)

    pages = [
        ("Home", ft.Icons.HOME_OUTLINED, ft.Icons.HOME),
        ("Store", ft.Icons.STORE_OUTLINED, ft.Icons.STORE),
        ("About", ft.Icons.INFO_OUTLINED, ft.Icons.INFO),
    ]

    async def show_drawer():
        await ft.context.page.show_drawer()

    async def handle_change(e: ft.Event[ft.NavigationDrawer]):
        set_selected(e.control.selected_index)
        await ft.context.page.close_drawer()

    return ft.View(
        appbar=ft.AppBar(
            title=ft.Text(pages[selected][0]),
            leading=ft.IconButton(ft.Icons.MENU, on_click=show_drawer),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        ),
        drawer=ft.NavigationDrawer(
            selected_index=selected,
            on_change=handle_change,
            controls=[
                ft.Container(height=12),
                *[
                    ft.NavigationDrawerDestination(
                        label=label, icon=icon, selected_icon=sel
                    )
                    for label, icon, sel in pages
                ],
            ],
        ),
        controls=[
            ft.SafeArea(content=ft.Text(f"Welcome to {pages[selected][0]}", size=24))
        ],
    )


def main(page: ft.Page):
    page.render_views(App)


if __name__ == "__main__":
    ft.run(main)
