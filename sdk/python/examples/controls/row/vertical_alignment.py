import flet as ft


class RowWithVerticalAlignment(ft.Column):
    def __init__(self, alignment: ft.CrossAxisAlignment):
        super().__init__()
        self.controls = [
            ft.Text(str(alignment), size=16),
            ft.Container(
                content=ft.Row(self.generate_items(3), vertical_alignment=alignment),
                bgcolor=ft.Colors.AMBER_100,
                height=150,
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
    page.add(
        RowWithVerticalAlignment(ft.CrossAxisAlignment.START),
        RowWithVerticalAlignment(ft.CrossAxisAlignment.CENTER),
        RowWithVerticalAlignment(ft.CrossAxisAlignment.END),
    )


ft.run(main)
