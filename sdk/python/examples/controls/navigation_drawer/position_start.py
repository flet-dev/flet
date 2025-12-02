import flet as ft


def main(page: ft.Page):
    async def handle_show_drawer():
        await page.show_drawer()

    def handle_dismissal(e: ft.Event[ft.NavigationDrawer]):
        print("Drawer dismissed!")

    async def handle_change(e: ft.Event[ft.NavigationDrawer]):
        print(f"Selected Index changed: {e.control.selected_index}")
        await page.close_drawer()

    page.drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.Icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.Icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.Icons.PHONE,
            ),
        ],
    )
    page.add(
        ft.Button(
            content="Show drawer",
            on_click=handle_show_drawer,
        )
    )


if __name__ == "__main__":
    ft.run(main)
