import flet as ft


def main(page: ft.Page):
    async def handle_tile_click(e: ft.Event[ft.ListTile]):
        await anchor.close_view_async(e.control.title.value)

    async def open_click():
        await anchor.open_view_async()

    def handle_change(e: ft.Event[ft.SearchBar]):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e: ft.Event[ft.SearchBar]):
        print(f"handle_submit e.data: {e.data}")

    async def handle_tap(e: ft.Event[ft.SearchBar]):
        print("handle_tap")
        await anchor.open_view_async()

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.OutlinedButton(
                    content="Open Search View",
                    on_click=open_click,
                ),
            ],
        ),
        anchor := ft.SearchBar(
            view_elevation=4,
            divider_color=ft.Colors.AMBER,
            bar_hint_text="Search colors...",
            view_hint_text="Choose a color from the suggestions...",
            on_change=handle_change,
            on_submit=handle_submit,
            on_tap=handle_tap,
            controls=[
                ft.ListTile(title=ft.Text(f"Color {i}"), on_click=handle_tile_click)
                for i in range(10)
            ],
        ),
    )


ft.run(main)
