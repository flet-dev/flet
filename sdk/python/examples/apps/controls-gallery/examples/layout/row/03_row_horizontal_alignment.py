import flet as ft

name = "Row horizontal alignments"


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

    def row_with_alignment(align: ft.MainAxisAlignment):
        return ft.Column(
            width=500,
            controls=[
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Row(items(3), alignment=align),
                    bgcolor=ft.Colors.AMBER_100,
                ),
            ],
        )

    return ft.Column(
        [
            row_with_alignment(ft.MainAxisAlignment.START),
            row_with_alignment(ft.MainAxisAlignment.CENTER),
            row_with_alignment(ft.MainAxisAlignment.END),
            row_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),
            row_with_alignment(ft.MainAxisAlignment.SPACE_AROUND),
            row_with_alignment(ft.MainAxisAlignment.SPACE_EVENLY),
        ]
    )
