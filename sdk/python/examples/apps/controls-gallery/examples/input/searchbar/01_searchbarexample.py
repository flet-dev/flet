import flet as ft

name = "SearchBar example"


def example():
    async def close_anchor(e):
        text = f"Color {e.control.data}"
        print(f"closing view from {text}")
        await anchor.close_view_async(text)

    async def open_anchor():
        await anchor.open_view_async()

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        print("handle_tap")

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=[
            ft.ListTile(title=ft.Text(f"Color {i}"), on_click=close_anchor, data=i)
            for i in range(10)
        ],
    )

    return ft.Column(
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.OutlinedButton(
                        "Open Search View",
                        on_click=open_anchor,
                    ),
                ],
            ),
            anchor,
        ]
    )
