import flet as ft


def main(page: ft.Page):
    def handle_chip1_click(e: ft.Event[ft.Chip]):
        e.control.label.value = "Saved to favorites"
        e.control.leading = ft.Icon(ft.Icons.FAVORITE_OUTLINED)
        e.control.disabled = True
        page.update()

    async def handle_chip2_click(e: ft.Event[ft.Chip]):
        await page.launch_url("https://maps.google.com")
        page.update()

    page.add(
        ft.Row(
            controls=[
                ft.Chip(
                    label=ft.Text("Save to favourites"),
                    leading=ft.Icon(ft.Icons.FAVORITE_BORDER_OUTLINED),
                    bgcolor=ft.Colors.GREEN_200,
                    disabled_color=ft.Colors.GREEN_100,
                    autofocus=True,
                    on_click=handle_chip1_click,
                ),
                ft.Chip(
                    label=ft.Text("9 min walk"),
                    leading=ft.Icon(ft.Icons.MAP_SHARP),
                    bgcolor=ft.Colors.GREEN_200,
                    on_click=handle_chip2_click,
                ),
            ]
        )
    )


ft.run(main)
