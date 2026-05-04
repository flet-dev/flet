import flet as ft


@ft.control
class RowWithAlignment(ft.Column):
    alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.START

    def init(self):
        self.controls = [
            ft.Text(str(self.alignment), size=16),
            ft.Container(
                bgcolor=ft.Colors.AMBER_100,
                content=ft.Row(
                    alignment=self.alignment,
                    controls=self.generate_items(3),
                ),
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
        ft.SafeArea(
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    RowWithAlignment(alignment=ft.MainAxisAlignment.START),
                    RowWithAlignment(alignment=ft.MainAxisAlignment.CENTER),
                    RowWithAlignment(alignment=ft.MainAxisAlignment.END),
                    RowWithAlignment(alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    RowWithAlignment(alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    RowWithAlignment(alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
