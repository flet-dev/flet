import flet as ft


def _line(width: int, height: int = 12) -> ft.Control:
    return ft.Container(
        width=width,
        height=height,
        bgcolor=ft.Colors.GREY_300,
        border_radius=ft.BorderRadius.all(height),
    )


def _placeholder_tile() -> ft.Control:
    return ft.Container(
        width=320,
        padding=ft.Padding.all(16),
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.BorderRadius.all(20),
        content=ft.Row(
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    width=48,
                    height=48,
                    bgcolor=ft.Colors.GREY_300,
                    border_radius=ft.BorderRadius.all(24),
                ),
                ft.Column(
                    expand=True,
                    spacing=10,
                    controls=[
                        _line(160),
                        _line(120),
                        ft.Row(
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[_line(70, 10), _line(90, 10)],
                        ),
                    ],
                ),
                ft.Container(
                    width=32,
                    height=32,
                    bgcolor=ft.Colors.GREY_300,
                    border_radius=ft.BorderRadius.all(16),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.title = "Shimmer - loading placeholders"
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 30

    page.add(
        ft.Shimmer(
            base_color=ft.Colors.with_opacity(0.3, ft.Colors.GREY_400),
            highlight_color=ft.Colors.GREY_100,
            content=ft.Column(
                spacing=14,
                controls=[_placeholder_tile() for _ in range(3)],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
