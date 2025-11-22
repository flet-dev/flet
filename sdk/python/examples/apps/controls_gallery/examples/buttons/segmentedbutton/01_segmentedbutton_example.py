import flet as ft

name = "SegmentedButton example"


def example():
    return ft.SegmentedButton(
        selected_icon=ft.Icon(ft.Icons.ONETWOTHREE),
        selected=["1", "4"],
        allow_multiple_selection=True,
        segments=[
            ft.Segment(
                value="1",
                label=ft.Text("1"),
                icon=ft.Icon(ft.Icons.LOOKS_ONE),
            ),
            ft.Segment(
                value="2",
                label=ft.Text("2"),
                icon=ft.Icon(ft.Icons.LOOKS_TWO),
            ),
            ft.Segment(
                value="3",
                label=ft.Text("3"),
                icon=ft.Icon(ft.Icons.LOOKS_3),
            ),
            ft.Segment(
                value="4",
                label=ft.Text("4"),
                icon=ft.Icon(ft.Icons.LOOKS_4),
            ),
        ],
    )
