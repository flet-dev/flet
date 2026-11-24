import flet as ft


@ft.control
class RowWithVerticalAlignment(ft.Column):
    alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.START

    def init(self):
        self.controls = [
            ft.Text(str(self.alignment), size=16),
            ft.Container(
                bgcolor=ft.Colors.AMBER_100,
                height=150,
                content=ft.Row(
                    vertical_alignment=self.alignment,
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
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    RowWithVerticalAlignment(alignment=ft.CrossAxisAlignment.START),
                    RowWithVerticalAlignment(alignment=ft.CrossAxisAlignment.CENTER),
                    RowWithVerticalAlignment(alignment=ft.CrossAxisAlignment.END),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
