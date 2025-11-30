import flet as ft


def main(page: ft.Page):
    page.title = "CupertinoSlidingSegmentedButton Example"
    page.theme_mode = ft.ThemeMode.LIGHT

    def handle_selection_change(e: ft.Event[ft.CupertinoSlidingSegmentedButton]):
        page.show_dialog(
            ft.SnackBar(ft.Text(f"Segment {e.control.selected_index + 1} was chosen!"))
        )

    page.add(
        ft.CupertinoSlidingSegmentedButton(
            selected_index=1,
            thumb_color=ft.Colors.BLUE_400,
            on_change=handle_selection_change,
            controls=[
                ft.Text("One"),
                ft.Text("Two"),
                ft.Text("Three"),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
