import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(
        ft.Stack(
            width=460,
            height=260,
            controls=[
                ft.Text(
                    "Offset translates by control size.",
                    left=12,
                    top=8,
                    size=16,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Container(
                    left=30,
                    top=70,
                    width=170,
                    height=90,
                    border_radius=16,
                    bgcolor=ft.Colors.BLUE_100,
                    border=ft.Border.all(2, ft.Colors.BLUE_GREY_400),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Original", size=20, color=ft.Colors.BLUE_GREY_700),
                ),
                ft.Container(
                    left=30,
                    top=70,
                    width=170,
                    height=90,
                    border_radius=16,
                    bgcolor=ft.Colors.AMBER_300,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Offset", size=26, weight=ft.FontWeight.BOLD),
                    offset=ft.Offset(
                        x=1.05,
                        y=0.55,
                        filter_quality=ft.FilterQuality.MEDIUM,
                    ),
                ),
                ft.Icon(
                    ft.Icons.ARROW_RIGHT_ALT_ROUNDED,
                    left=212,
                    top=82,
                    size=44,
                    color=ft.Colors.BLUE_GREY_600,
                ),
                ft.Text(
                    "offset = Offset(1.05, 0.55)",
                    left=194,
                    top=222,
                    size=14,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
