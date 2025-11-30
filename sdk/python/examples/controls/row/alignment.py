import flet as ft


class RowWithAlignment(ft.Column):
    def __init__(self, alignment: ft.MainAxisAlignment):
        super().__init__()
        self.controls = [
            ft.Text(str(alignment), size=16),
            ft.Container(
                content=ft.Row(self.generate_items(3), alignment=alignment),
                bgcolor=ft.Colors.AMBER_100,
            ),
        ]

    @staticmethod
    def generate_items(count: int):
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
    page.scroll = ft.ScrollMode.AUTO

    page.add(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                RowWithAlignment(ft.MainAxisAlignment.START),
                RowWithAlignment(ft.MainAxisAlignment.CENTER),
                RowWithAlignment(ft.MainAxisAlignment.END),
                RowWithAlignment(ft.MainAxisAlignment.SPACE_BETWEEN),
                RowWithAlignment(ft.MainAxisAlignment.SPACE_AROUND),
                RowWithAlignment(ft.MainAxisAlignment.SPACE_EVENLY),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
