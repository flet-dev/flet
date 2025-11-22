import flet as ft

name = "Selectable Text controls"


def example():
    return ft.Column(
        controls=[
            ft.SelectionArea(
                content=ft.Column(
                    [ft.Text("Selectable text"), ft.Text("Also selectable")]
                )
            ),
            ft.Text("Not selectable"),
        ]
    )
