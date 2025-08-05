import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Stack(
            width=300,
            height=300,
            controls=[
                ft.Image(
                    src="https://picsum.photos/300/300",
                    width=300,
                    height=300,
                    fit=ft.BoxFit.CONTAIN,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            value="Image title",
                            color=ft.Colors.SURFACE_TINT,
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            opacity=0.5,
                        )
                    ],
                ),
            ],
        )
    )


ft.run(main)
