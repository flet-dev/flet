import flet as ft

name = "Card example"


def example():
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ALBUM),
                        title=ft.Text("The Enchanted Nightingale"),
                        subtitle=ft.Text(
                            "Music by Julie Gable. Lyrics by Sidney Stein."
                        ),
                    ),
                    ft.Row(
                        [ft.TextButton("Buy tickets"), ft.TextButton("Listen")],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ]
            ),
            width=400,
            padding=10,
        )
    )
