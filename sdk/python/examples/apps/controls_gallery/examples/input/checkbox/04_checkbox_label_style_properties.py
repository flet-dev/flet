import flet as ft

name = """Checkbox with different label_style properties"""


def example():
    checkbox = ft.Checkbox(
        label="Checkbox label",
        label_style=ft.TextStyle(
            size=20,
            height=10,
            weight=ft.FontWeight.BOLD,
            italic=True,
            decoration=ft.TextDecoration.OVERLINE,
            decoration_color=ft.Colors.GREEN_300,
            decoration_thickness=5,
            decoration_style=ft.TextDecorationStyle.WAVY,
            font_family="Roboto Mono",
            color=ft.Colors.ORANGE_300,
            bgcolor=ft.Colors.GREEN_100,
            shadow=ft.BoxShadow(
                spread_radius=5,
                blur_radius=5,
                color=ft.Colors.RED,
                offset=ft.Offset(5, 5),
                blur_style=ft.BlurStyle.SOLID,
            ),
            foreground=ft.Paint(
                color=ft.Colors.GREEN_800,
                blend_mode=ft.BlendMode.COLOR_BURN,
                blur_image=1,
                anti_alias=True,
                gradient=ft.PaintLinearGradient(
                    (0, 10),
                    (0, 100),
                    colors=[ft.Colors.BLUE, ft.Colors.YELLOW],
                    color_stops=[20, 30],
                    tile_mode=ft.GradientTileMode.MIRROR,
                    type="linear",
                ),
                stroke_cap=ft.StrokeCap.ROUND,
                stroke_join=ft.StrokeJoin.BEVEL,
                stroke_miter_limit=5,
                stroke_width=5,
                stroke_dash_pattern=[1, 2, 3],
                style=ft.PaintingStyle.STROKE,
            ),
            letter_spacing=5,
            word_spacing=5,
            overflow=ft.TextOverflow.ELLIPSIS,
            baseline=ft.TextBaseline.ALPHABETIC,
        ),
    )

    return ft.Column(
        [
            checkbox,
        ]
    )
