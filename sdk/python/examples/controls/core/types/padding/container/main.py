import flet as ft


def container(title: str, padding: ft.Padding) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(value=title, weight=ft.FontWeight.BOLD),
                ft.Container(
                    bgcolor=ft.Colors.BLUE_GREY_100,
                    content=ft.Container(
                        bgcolor=ft.Colors.AMBER,
                        border=ft.Border.all(2, ft.Colors.RED),
                        padding=padding,
                        content=ft.Container(
                            bgcolor=ft.Colors.BLACK,
                            content=ft.Text("Content", color=ft.Colors.WHITE),
                        ),
                        width=200,
                        height=200,
                    ),
                ),
            ],
            spacing=8,
        )
    )


def main(page: ft.Page):
    page.title = "Containers with different padding"
    page.padding = 20

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Column(
                        spacing=22,
                        controls=[
                            container("Padding.all(10)", ft.Padding.all(10)),
                            container("Padding.all(20)", ft.Padding.all(20)),
                            container(
                                "Padding.symmetric(horizontal=10)",
                                ft.Padding.symmetric(horizontal=10),
                            ),
                            container(
                                "Padding.symmetric(vertical=10)",
                                ft.Padding.symmetric(vertical=10),
                            ),
                            container(
                                "Padding.only(left=10)", ft.Padding.only(left=10)
                            ),
                            container("Padding.only(top=10)", ft.Padding.only(top=10)),
                            container(
                                "Padding.only(right=10)", ft.Padding.only(right=10)
                            ),
                            container(
                                "Padding.only(bottom=10)", ft.Padding.only(bottom=10)
                            ),
                        ],
                    )
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
