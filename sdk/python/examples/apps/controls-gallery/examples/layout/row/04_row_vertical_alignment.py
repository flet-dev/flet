import flet as ft

name = "Row vertical alignments"


def example():
    def items(count):
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

    def row_with_vertical_alignment(align: ft.CrossAxisAlignment):
        return ft.Column(
            width=500,
            controls=[
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Row(items(3), vertical_alignment=align),
                    bgcolor=ft.Colors.AMBER_100,
                    height=150,
                ),
            ],
        )

    return ft.Column(
        [
            row_with_vertical_alignment(ft.CrossAxisAlignment.START),
            row_with_vertical_alignment(ft.CrossAxisAlignment.CENTER),
            row_with_vertical_alignment(ft.CrossAxisAlignment.END),
        ]
    )
