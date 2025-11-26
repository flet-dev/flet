import flet as ft


class ColumnFromHorizontalAlignment(ft.Column):
    def __init__(self, alignment: ft.CrossAxisAlignment):
        super().__init__()
        self.controls = [
            ft.Text(str(alignment), size=16),
            ft.Container(
                bgcolor=ft.Colors.AMBER_100,
                width=100,
                content=ft.Column(
                    controls=self.generate_items(3),
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=alignment,
                ),
            ),
        ]

    @staticmethod
    def generate_items(count: int):
        """Generates a list of custom Containers with length `count`."""
        return [
            ft.Container(
                content=ft.Text(value=str(i)),
                alignment=ft.Alignment.CENTER,
                width=50,
                height=50,
                bgcolor=ft.Colors.AMBER_500,
            )
            for i in range(1, count + 1)
        ]


def main(page: ft.Page):
    page.add(
        ft.Row(
            spacing=30,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ColumnFromHorizontalAlignment(ft.CrossAxisAlignment.START),
                ColumnFromHorizontalAlignment(ft.CrossAxisAlignment.CENTER),
                ColumnFromHorizontalAlignment(ft.CrossAxisAlignment.END),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
