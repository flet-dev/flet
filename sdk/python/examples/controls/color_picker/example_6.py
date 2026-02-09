import flet as ft
from flet_color_picker import MultipleChoiceBlockPicker


def main(page: ft.Page):
    page.title = "MultipleChoiceBlockPicker"
    page.padding = 20

    def on_colors_change(e: ft.ControlEvent):
        print(f"colors: {e.data}")

    dialog_picker = MultipleChoiceBlockPicker(
        colors=["#03a9f4", "#4caf50"],
        available_colors=[
            "#f44336",
            "#e91e63",
            "#9c27b0",
            "#3f51b5",
            "#2196f3",
            "#03a9f4",
            "#009688",
            "#4caf50",
            "#ff9800",
            "#795548",
        ],
        on_colors_change=on_colors_change,
    )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Pick colors"),
        content=dialog_picker,
        actions=[
            ft.TextButton("Close", on_click=lambda e: page.pop_dialog()),
        ],
    )

    page.add(
        ft.IconButton(icon=ft.Icons.BRUSH, on_click=lambda e: page.show_dialog(dialog)),
    )


ft.run(main)
