import flet as ft


def main(page: ft.Page):
    def handle_dismissal(e: ft.Event[ft.NavigationDrawer]):
        print("End drawer dismissed")

    def handle_change(e: ft.Event[ft.NavigationDrawer]):
        print(f"Selected Index changed: {e.control.selected_index}")
        page.pop_dialog()

    end_drawer = ft.NavigationDrawer(
        position=ft.NavigationDrawerPosition.END,
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
        ft.ElevatedButton(
            content="Show end drawer",
            on_click=lambda e: page.show_dialog(end_drawer),
        )
    )


ft.run(main)
