import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Row(
            controls=[
                ft.Image(
                    src="https://picsum.photos/300/300?1",
                    width=300,
                    height=300,
                    fit=ft.BoxFit.FILL,
                ),
                ft.ShaderMask(
                    blend_mode=ft.BlendMode.MULTIPLY,
                    shader=ft.RadialGradient(
                        center=ft.Alignment.CENTER,
                        radius=0.5,
                        colors=[ft.Colors.WHITE, ft.Colors.PINK],
                        tile_mode=ft.GradientTileMode.CLAMP,
                    ),
                    content=ft.Image(
                        src="https://picsum.photos/300/300?1",
                        width=300,
                        height=300,
                        fit=ft.BoxFit.FILL,
                    ),
                ),
            ]
        )
    )


if __name__ == "__main__":
    ft.run(main)
