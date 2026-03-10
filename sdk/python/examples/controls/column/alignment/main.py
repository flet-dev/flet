import flet as ft


@ft.control
class ColumnFromVerticalAlignment(ft.Column):
    alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.START

    def init(self):
        self.controls = [
            ft.Text(str(self.alignment), size=10),
            ft.Container(
                content=ft.Column(self.generate_items(3), alignment=self.alignment),
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
                ColumnFromVerticalAlignment(alignment=ft.MainAxisAlignment.START),
                ColumnFromVerticalAlignment(alignment=ft.MainAxisAlignment.CENTER),
                ColumnFromVerticalAlignment(alignment=ft.MainAxisAlignment.END),
                ColumnFromVerticalAlignment(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ColumnFromVerticalAlignment(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                ColumnFromVerticalAlignment(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                ),
            ],
        )
    )


ft.run(main)
