import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Shimmer(
            base_color=ft.Colors.with_opacity(0.3, ft.Colors.GREY_400),
            highlight_color=ft.Colors.WHITE,
            content=ft.Column(
                controls=[
                    ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
                    ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
                    ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
