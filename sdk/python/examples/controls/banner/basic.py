import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_banner_close(e: ft.Event[ft.TextButton]):
        page.pop_dialog()
        page.add(ft.Text("Action clicked: " + e.control.content))

    action_button_style = ft.ButtonStyle(color=ft.Colors.BLUE)
    banner = ft.Banner(
        bgcolor=ft.Colors.AMBER_100,
        leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
        content=ft.Text(
            value="Oops, there were some errors while trying to delete the file. What would you like to do?",
            color=ft.Colors.BLACK,
        ),
        actions=[
            ft.TextButton(
                content="Retry",
                style=action_button_style,
                on_click=handle_banner_close,
            ),
            ft.TextButton(
                content="Ignore",
                style=action_button_style,
                on_click=handle_banner_close,
            ),
            ft.TextButton(
                content="Cancel",
                style=action_button_style,
                on_click=handle_banner_close,
            ),
        ],
    )

    page.add(
        ft.ElevatedButton("Show Banner", on_click=lambda e: page.show_dialog(banner))
    )


ft.run(main)
