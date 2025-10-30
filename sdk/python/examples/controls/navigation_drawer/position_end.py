import flet as ft


def main(page: ft.Page):
    async def handle_show_drawer():
        await page.show_end_drawer()

    def handle_dismissal(e: ft.Event[ft.NavigationDrawer]):
        print("Drawer dismissed!")

    async def handle_change(e: ft.Event[ft.NavigationDrawer]):
        print(f"Selected Index changed: {e.control.selected_index}")
        await page.close_end_drawer()

    page.end_drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP,
                label="Item 1",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ADD_COMMENT),
                label="Item 2",
            ),
        ],
    )
    page.add(
        ft.Button(
            content="Show end drawer",
            on_click=handle_show_drawer,
        )
    )


ft.run(main)
