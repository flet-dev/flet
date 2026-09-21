import flet as ft


def container(title: str, margin: ft.Margin) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(value=title, weight=ft.FontWeight.BOLD),
                ft.Container(
                    bgcolor=ft.Colors.RED,
                    padding=0,
                    content=ft.Container(
                        bgcolor=ft.Colors.AMBER,
                        margin=margin,
                        width=200,
                        height=200,
                    ),
                ),
            ],
            spacing=8,
        )
    )


def main(page: ft.Page):
    page.title = "Margin Example"
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
                            container("Margin.all(10)", ft.Margin.all(10)),
                            container("Margin.all(20)", ft.Margin.all(20)),
                            container(
                                "Margin.symmetric(vertical=10)",
                                ft.Margin.symmetric(vertical=10),
                            ),
                            container(
                                "Margin.symmetric(horizontal=10)",
                                ft.Margin.symmetric(horizontal=10),
                            ),
                            container("Margin.only(left=10)", ft.Margin.only(left=10)),
                            container("Margin.only(top=10)", ft.Margin.only(top=10)),
                            container(
                                "Margin.only(right=10)", ft.Margin.only(right=10)
                            ),
                            container(
                                "Margin.only(bottom=10)", ft.Margin.only(bottom=10)
                            ),
                        ],
                    )
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
