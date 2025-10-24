import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Row(
            controls=[
                ft.ShaderMask(
                    blend_mode=ft.BlendMode.COLOR_BURN,
                    shader=ft.RadialGradient(
                        center=ft.Alignment.TOP_LEFT,
                        radius=1.0,
                        colors=[ft.Colors.YELLOW, ft.Colors.DEEP_ORANGE_900],
                        tile_mode=ft.GradientTileMode.CLAMP,
                    ),
                    content=ft.Image(
                        src="https://picsum.photos/id/288/300/300",
                        width=300,
                        height=300,
                        fit=ft.BoxFit.FILL,
                    ),
                ),
                ft.ShaderMask(
                    blend_mode=ft.BlendMode.DST_IN,
                    shader=ft.LinearGradient(
                        begin=ft.Alignment.TOP_CENTER,
                        end=ft.Alignment.BOTTOM_CENTER,
                        colors=[ft.Colors.BLACK, ft.Colors.TRANSPARENT],
                        stops=[0.5, 1.0],
                    ),
                    content=ft.Image(src="https://picsum.photos/id/288/300/300"),
                ),
            ]
        )
    )


if __name__ == "__main__":
    ft.run(main)
