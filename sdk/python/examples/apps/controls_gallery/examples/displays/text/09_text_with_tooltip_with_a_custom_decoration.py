import flet as ft

name = "Gradually fade out image to the bottom edge"


def example():
    import math

    return ft.Text(
        value="Hover to see tooltip",
        tooltip=ft.Tooltip(
            message="This is tooltip",
            # content=ft.Text("Hover to see tooltip"),
            padding=20,
            border_radius=10,
            text_style=ft.TextStyle(size=20, color=ft.Colors.WHITE),
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment(0.8, 1),
                # end=ft.Alignment.bottom_left(),
                # colors=[ft.Colors.BLUE, ft.Colors.YELLOW],
                colors=[
                    "0xff1f005c",
                    "0xff5b0060",
                    "0xff870160",
                    "0xffac255e",
                    "0xffca485c",
                    "0xffe16b5c",
                    "0xfff39060",
                    "0xffffb56b",
                ],
                tile_mode=ft.GradientTileMode.MIRROR,
                rotation=math.pi / 3,
            ),
        ),
    )
