import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Row(
            controls=[
                ft.ShaderMask(
                    content=ft.Image(src="https://picsum.photos/id/288/300/300"),
                    blend_mode=ft.BlendMode.DST_IN,
                    border_radius=10,
                    shader=ft.LinearGradient(
                        begin=ft.Alignment.TOP_CENTER,
                        end=ft.Alignment.BOTTOM_CENTER,
                        colors=[ft.Colors.BLACK, ft.Colors.TRANSPARENT],
                        stops=[0.5, 1.0],
                    ),
                ),
            ]
        )
    )


if __name__ == "__main__":
    ft.run(main)
