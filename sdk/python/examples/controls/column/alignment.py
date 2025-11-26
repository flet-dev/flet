import flet as ft


class ColumnFromVerticalAlignment(ft.Column):
    def __init__(self, alignment: ft.MainAxisAlignment):
        super().__init__()
        self.controls = [
            ft.Text(str(alignment), size=10),
            ft.Container(
                content=ft.Column(self.generate_items(3), alignment=alignment),
                bgcolor=ft.Colors.AMBER_100,
                height=400,
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
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ColumnFromVerticalAlignment(ft.MainAxisAlignment.START),
                ColumnFromVerticalAlignment(ft.MainAxisAlignment.CENTER),
                ColumnFromVerticalAlignment(ft.MainAxisAlignment.END),
                ColumnFromVerticalAlignment(ft.MainAxisAlignment.SPACE_BETWEEN),
                ColumnFromVerticalAlignment(ft.MainAxisAlignment.SPACE_AROUND),
                ColumnFromVerticalAlignment(ft.MainAxisAlignment.SPACE_EVENLY),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
