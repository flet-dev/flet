import flet as ft

name = "CupertinoSegmentedButton example"


def example():
    return ft.CupertinoSegmentedButton(
        selected_index=1,
        selected_color=ft.Colors.RED_400,
        on_change=lambda e: print(f"selected_index: {e.data}"),
        controls=[
            ft.Text("One"),
            ft.Container(
                padding=ft.Padding.symmetric(vertical=0, horizontal=30),
                content=ft.Text("Two"),
            ),
            ft.Container(
                padding=ft.Padding.symmetric(vertical=0, horizontal=10),
                content=ft.Text("Three"),
            ),
        ],
    )
