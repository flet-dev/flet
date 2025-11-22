import flet as ft

name = "Column vertical alignments"


def example():
    HEIGHT = 400

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

    def column_with_alignment(align: ft.MainAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=10),
                ft.Container(
                    content=ft.Column(items(3), alignment=align),
                    bgcolor=ft.Colors.AMBER_100,
                    height=HEIGHT,
                ),
            ]
        )

    return ft.Row(
        [
            column_with_alignment(ft.MainAxisAlignment.START),
            column_with_alignment(ft.MainAxisAlignment.CENTER),
            column_with_alignment(ft.MainAxisAlignment.END),
            column_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),
            column_with_alignment(ft.MainAxisAlignment.SPACE_AROUND),
            column_with_alignment(ft.MainAxisAlignment.SPACE_EVENLY),
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.START,
    )
