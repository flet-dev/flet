import flet as ft


def main(page: ft.Page):
    page.title = "Card Example"
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.Card(
            shadow_color=ft.Colors.ON_SURFACE_VARIANT,
            content=ft.Container(
                width=400,
                padding=10,
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            bgcolor=ft.Colors.GREY_400,
                            leading=ft.Icon(ft.Icons.ALBUM),
                            title=ft.Text("The Enchanted Nightingale"),
                            subtitle=ft.Text(
                                "Music by Julie Gable. Lyrics by Sidney Stein."
                            ),
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.TextButton("Buy tickets"),
                                ft.TextButton("Listen"),
                            ],
                        ),
                    ]
                ),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
