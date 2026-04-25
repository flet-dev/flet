import flet as ft


def main(page: ft.Page):
    page.spacing = 20

    tile = ft.ExpansionTile(
        title=ft.Text("I am the title of this tile.", weight=ft.FontWeight.BOLD),
        subtitle=ft.Text("This is the subtitle."),
        affinity=ft.TileAffinity.LEADING,
        controls=[ft.Text("👻", size=80)],
        expanded=True,
        on_change=lambda e: print(f"Tile was {'expanded' if e.data else 'collapsed'}"),
    )

    def expand_tile(_: ft.Event[ft.FilledButton]):
        tile.expanded = True
        tile.update()

    def collapse_tile(_: ft.Event[ft.OutlinedButton]):
        tile.expanded = False
        tile.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.FilledButton("Expand Tile", on_click=expand_tile),
                            ft.OutlinedButton("Collapse Tile", on_click=collapse_tile),
                        ],
                    ),
                    tile,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
