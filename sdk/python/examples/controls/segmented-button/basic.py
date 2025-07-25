import flet as ft


def main(page: ft.Page):
    def handle_selection_change(e: ft.Event[ft.SegmentedButton]):
        print(e)

    page.add(
        ft.SegmentedButton(
            on_change=handle_selection_change,
            selected_icon=ft.Icon(ft.Icons.CHECK_SHARP),
            selected=["1"],
            allow_empty_selection=True,
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
        ),
        ft.SegmentedButton(
            on_change=handle_selection_change,
            selected_icon=ft.Icon(ft.Icons.ONETWOTHREE),
            selected=["2"],
            allow_multiple_selection=False,
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
        ),
    )


ft.run(main)
