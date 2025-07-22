import flet as ft

name = "ExpansionTile example"


def example():
    return ft.Column(
        controls=[
            ft.ExpansionTile(
                title=ft.Text("ExpansionTile 1"),
                subtitle=ft.Text("Trailing expansion arrow icon"),
                affinity=ft.TileAffinity.PLATFORM,
                maintain_state=True,
                collapsed_text_color=ft.Colors.RED,
                text_color=ft.Colors.RED,
                controls=[ft.ListTile(title=ft.Text("This is sub-tile number 1"))],
            ),
            ft.ExpansionTile(
                title=ft.Text("ExpansionTile 2"),
                subtitle=ft.Text("Custom expansion arrow icon"),
                trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                collapsed_text_color=ft.Colors.GREEN,
                text_color=ft.Colors.GREEN,
                controls=[ft.ListTile(title=ft.Text("This is sub-tile number 2"))],
            ),
            ft.ExpansionTile(
                title=ft.Text("ExpansionTile 3"),
                subtitle=ft.Text("Leading expansion arrow icon"),
                affinity=ft.TileAffinity.LEADING,
                initially_expanded=True,
                collapsed_text_color=ft.Colors.BLUE,
                text_color=ft.Colors.BLUE,
                controls=[
                    ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                    ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                    ft.ListTile(title=ft.Text("This is sub-tile number 5")),
                ],
            ),
        ]
    )
