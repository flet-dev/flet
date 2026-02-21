from math import pi

import flet as ft


def card(title: str, color: str, matrix: ft.Matrix4) -> ft.Container:
    return ft.Container(
        width=220,
        height=130,
        border_radius=18,
        bgcolor=color,
        padding=12,
        content=ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
        transform=ft.Transform(
            matrix=matrix,
            alignment=ft.Alignment.CENTER,
            filter_quality=ft.FilterQuality.MEDIUM,
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.spacing = 20

    perspective_tilt = (
        ft.Matrix4.identity()
        .set_entry(3, 2, 0.0018)
        .rotate_x(-0.35)
        .rotate_y(0.45)
        .translate(0, -10, 0)
    )

    skew_and_rotate = ft.Matrix4.skew_y(0.28).rotate_z(-pi / 14)

    mirrored_spin = ft.Matrix4.diagonal3_values(-1, 1, 1).rotate_z(pi / 10)

    mix = ft.Matrix4.translation_values(24, -8, 0).multiply(
        ft.Matrix4.rotation_z(pi / 16).scale(0.9, 0.9)
    )

    page.add(
        ft.Text("Matrix4 transform recording + replay", size=24),
        ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col={"sm": 6, "md": 3},
                    content=card(
                        "Perspective tilt",
                        ft.Colors.CYAN_300,
                        perspective_tilt,
                    ),
                ),
                ft.Container(
                    col={"sm": 6, "md": 3},
                    content=card(
                        "Skew + rotate",
                        ft.Colors.AMBER_300,
                        skew_and_rotate,
                    ),
                ),
                ft.Container(
                    col={"sm": 6, "md": 3},
                    content=card(
                        "Mirror + spin",
                        ft.Colors.PINK_200,
                        mirrored_spin,
                    ),
                ),
                ft.Container(
                    col={"sm": 6, "md": 3},
                    content=card("Multiply chain", ft.Colors.LIGHT_GREEN_300, mix),
                ),
            ]
        ),
    )


if __name__ == "__main__":
    ft.run(main)
