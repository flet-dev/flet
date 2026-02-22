import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(
        ft.Container(
            width=220,
            height=120,
            bgcolor=ft.Colors.GREEN_300,
            border_radius=16,
            alignment=ft.Alignment.CENTER,
            content=ft.Text("Scale", size=28, weight=ft.FontWeight.BOLD),
            scale=ft.Scale(
                scale_x=1.18,
                scale_y=0.82,
                alignment=ft.Alignment.CENTER,
                filter_quality=ft.FilterQuality.MEDIUM,
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
