import flet as ft

name = "Adding a pink glow around image edges"


def example():
    return ft.Row(
        [
            ft.ShaderMask(
                content=ft.Image(
                    src="https://picsum.photos/200/200?1",
                    width=200,
                    height=200,
                    fit=ft.BoxFit.FILL,
                ),
                blend_mode=ft.BlendMode.MULTIPLY,
                shader=ft.RadialGradient(
                    center=ft.Alignment.CENTER,
                    radius=2.0,
                    colors=[ft.Colors.WHITE, ft.Colors.PINK],
                    tile_mode=ft.GradientTileMode.CLAMP,
                ),
            )
        ]
    )
