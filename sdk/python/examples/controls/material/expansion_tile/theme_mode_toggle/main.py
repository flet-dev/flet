import flet as ft


def main(page: ft.Page):
    page.spacing = 0
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    def handle_switch_change(e: ft.Event[ft.Switch]):
        page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        e.control.thumb_icon = (
            ft.Icons.DARK_MODE
            if page.theme_mode == ft.ThemeMode.DARK
            else ft.Icons.LIGHT_MODE
        )
        page.update()

    def handle_expansion_tile_change(e: ft.Event[ft.ExpansionTile]):
        page.show_dialog(
            ft.SnackBar(
                duration=1000,
                content=ft.Text(
                    value=(
                        f"ExpansionTile was "
                        f"{'expanded' if e.data == 'true' else 'collapsed'}"
                    )
                ),
            )
        )
        if e.control.trailing:
            e.control.trailing.icon = (
                ft.Icons.ARROW_DROP_DOWN
                if e.control.trailing.icon == ft.Icons.ARROW_DROP_DOWN_CIRCLE
                else ft.Icons.ARROW_DROP_DOWN_CIRCLE
            )
            e.control.trailing.update()

    switch = ft.Switch(
        thumb_icon=ft.Icons.DARK_MODE,
        on_change=handle_switch_change,
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=0,
                controls=[
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
                        controls=[
                            ft.ListTile(title=ft.Text("This is sub-tile number 2"))
                        ],
                    ),
                    ft.ExpansionTile(
                        title=ft.Text("ExpansionTile 3"),
                        subtitle=ft.Text("Leading expansion arrow icon"),
                        affinity=ft.TileAffinity.LEADING,
                        expanded=True,
                        collapsed_text_color=ft.Colors.BLUE_800,
                        text_color=ft.Colors.BLUE_200,
                        controls=[
                            ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                            ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                            ft.ListTile(title=ft.Text("This is sub-tile number 5")),
                        ],
                    ),
                    ft.Container(
                        padding=ft.Padding.only(right=16, bottom=32),
                        alignment=ft.Alignment.center_right,
                        content=switch,
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
