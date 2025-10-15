import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Row(
            width=180,
            height=100,
            spacing=0,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.ORANGE_300,
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
                ft.VerticalDivider(),
                ft.Container(
                    bgcolor=ft.Colors.BROWN_400,
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
                ft.VerticalDivider(width=1, color=ft.Colors.WHITE),
                ft.Container(
                    bgcolor=ft.Colors.BLUE_300,
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
                ft.VerticalDivider(width=9, thickness=3),
                ft.Container(
                    bgcolor=ft.Colors.GREEN_300,
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
