import flet as ft

name = "CupertinoSlidingSegmentedButton example"


def example():
    return ft.CupertinoSlidingSegmentedButton(
        selected_index=1,
        thumb_color=ft.Colors.BLUE_400,
        on_change=lambda e: print(f"selected_index: {e.data}"),
        padding=ft.Padding.symmetric(vertical=0, horizontal=10),
        controls=[
            ft.Text("One"),
            ft.Text("Two"),
            ft.Text("Three"),
        ],
    )
