import flet as ft


def main(page: ft.Page) -> None:
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_fullscreen_change(e: ft.Event[ft.Switch]):
        page.full_screen = e.control.value

    page.add(
        ft.SafeArea(
            ft.Switch(
                value=page.full_screen,
                label="Toggle Fullscreen",
                on_change=handle_fullscreen_change,
            ),
        )
    )


ft.run(main)
