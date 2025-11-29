import flet as ft


def main(page: ft.Page):
    def get_items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.Alignment.CENTER,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER_500,
                )
            )
        return items

    def column_with_horiz_alignment(alignment: ft.CrossAxisAlignment):
        return ft.Column(
            controls=[
                ft.Text(alignment.name, size=16),
                ft.Container(
                    bgcolor=ft.Colors.AMBER_100,
                    width=100,
                    content=ft.Column(
                        get_items(3),
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=alignment,
                    ),
                ),
            ]
        )

    page.add(
        ft.Row(
            spacing=25,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                column_with_horiz_alignment(ft.CrossAxisAlignment.START),
                column_with_horiz_alignment(ft.CrossAxisAlignment.CENTER),
                column_with_horiz_alignment(ft.CrossAxisAlignment.END),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
