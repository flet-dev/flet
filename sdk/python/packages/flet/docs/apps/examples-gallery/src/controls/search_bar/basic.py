import flet as ft

colors = [
    "Amber",
    "Blue Grey",
    "Brown",
    "Deep Orange",
    "Green",
    "Light Blue",
    "Orange",
    "Red",
]


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def build_tiles(items: list[str]) -> list[ft.Control]:
        return [
            ft.ListTile(
                title=ft.Text(item),
                data=item,
                on_click=handle_tile_click,
            )
            for item in items
        ]

    async def handle_tile_click(e: ft.Event[ft.ListTile]):
        await anchor.close_view()

    async def handle_change(e: ft.Event[ft.SearchBar]):
        query = e.control.value.strip().lower()
        matching = (
            [color for color in colors if query in color.lower()] if query else colors
        )
        anchor.controls = build_tiles(matching)

    def handle_submit(e: ft.Event[ft.SearchBar]):
        print(f"Submit: {e.data}")

    async def handle_tap(e: ft.Event[ft.SearchBar]):
        await anchor.open_view()

    page.add(
        anchor := ft.SearchBar(
            view_elevation=4,
            divider_color=ft.Colors.AMBER,
            bar_hint_text="Search colors...",
            view_hint_text="Choose a color from the suggestions...",
            on_change=handle_change,
            on_submit=handle_submit,
            on_tap=handle_tap,
            controls=build_tiles(colors),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
