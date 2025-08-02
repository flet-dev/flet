import flet as ft


def main(page: ft.Page):
    def handle_tile_click(e: ft.Event[ft.ListTile]):
        anchor.close_view(e.control.title.value)

    def handle_change(e: ft.Event[ft.SearchBar]):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e: ft.Event[ft.SearchBar]):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e: ft.Event[ft.SearchBar]):
        print("handle_tap")
        anchor.open_view()

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.OutlinedButton(
                    content="Open Search View",
                    on_click=lambda _: anchor.open_view(),
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
