import flet as ft


def main(page: ft.Page):
    page.spacing = 0
    page.padding = 0

    def handle_switch_change(e: ft.Event[ft.Switch]):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            switch.thumb_icon = ft.Icons.LIGHT_MODE
        else:
            switch.thumb_icon = ft.Icons.DARK_MODE
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    def handle_expansion_tile_change(e: ft.Event[ft.ExpansionTile]):
        page.show_dialog(
            ft.SnackBar(
                duration=1000,
                content=ft.Text(
                    f"ExpansionTile was {'expanded' if e.data == 'true' else 'collapsed'}"
                ),
            )
        )
        if e.control.trailing:
            e.control.trailing.name = (
                ft.Icons.ARROW_DROP_DOWN
                if e.control.trailing.name == ft.Icons.ARROW_DROP_DOWN_CIRCLE
                else ft.Icons.ARROW_DROP_DOWN_CIRCLE
            )
            page.update()

    switch = ft.Switch(thumb_icon=ft.Icons.DARK_MODE, on_change=handle_switch_change)

    page.add(
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 1"),
            subtitle=ft.Text("Trailing expansion arrow icon"),
            bgcolor=ft.Colors.BLUE_GREY_200,
            collapsed_bgcolor=ft.Colors.BLUE_GREY_200,
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=True,
            collapsed_text_color=ft.Colors.RED,
            text_color=ft.Colors.RED,
            controls=[
                ft.ListTile(
                    title=ft.Text("This is sub-tile number 1"),
                    bgcolor=ft.Colors.BLUE_GREY_200,
                )
            ],
        ),
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 2"),
            subtitle=ft.Text("Custom expansion arrow icon"),
            trailing=ft.Icon(ft.Icons.ARROW_DROP_DOWN),
            collapsed_text_color=ft.Colors.GREEN,
            text_color=ft.Colors.GREEN,
            on_change=handle_expansion_tile_change,
            controls=[ft.ListTile(title=ft.Text("This is sub-tile number 2"))],
        ),
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 3"),
            subtitle=ft.Text("Leading expansion arrow icon"),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=True,
            collapsed_text_color=ft.Colors.BLUE_800,
            text_color=ft.Colors.BLUE_200,
            controls=[
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
            ],
        ),
        ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.Container(
                    content=switch,
                    padding=ft.Padding.only(bottom=50),
                    alignment=ft.Alignment.BOTTOM_RIGHT,
                    expand=True,
                ),
            ],
        ),
    )


ft.run(main)
