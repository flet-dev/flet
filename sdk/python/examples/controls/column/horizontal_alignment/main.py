import flet as ft


@ft.control
class ColumnFromHorizontalAlignment(ft.Column):
    alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.START

    def init(self):
        self.controls = [
            ft.Text(str(self.alignment), size=16),
            ft.Container(
                bgcolor=ft.Colors.AMBER_100,
                width=100,
                content=ft.Column(
                    controls=self.generate_items(3),
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=self.alignment,
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
                ColumnFromHorizontalAlignment(alignment=ft.CrossAxisAlignment.START),
                ColumnFromHorizontalAlignment(alignment=ft.CrossAxisAlignment.CENTER),
                ColumnFromHorizontalAlignment(alignment=ft.CrossAxisAlignment.END),
            ],
        )
    )


ft.run(main)
