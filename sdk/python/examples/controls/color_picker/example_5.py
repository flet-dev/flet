import flet as ft
from flet_color_picker import BlockPicker


def main(page: ft.Page):
    page.title = "BlockPicker"
    page.padding = 20

    selected = ft.Text("#9c27b0")
    swatch = ft.Container(width=40, height=40, bgcolor="#9c27b0", border_radius=6)

    def on_color_change(e: ft.ControlEvent):
        selected.value = e.data
        swatch.bgcolor = e.data
        page.update()

    dialog_picker = BlockPicker(
        picker_color="#9c27b0",
        available_colors=[
            "#f44336",
            "#e91e63",
            "#9c27b0",
            "#3f51b5",
            "#2196f3",
            "#009688",
            "#4caf50",
            "#795548",
        ],
        on_color_change=on_color_change,
    )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Pick a color"),
        content=dialog_picker,
        actions=[
            ft.TextButton("Close", on_click=lambda e: page.pop_dialog()),
        ],
    )

    page.add(
        ft.Row(
            spacing=12,
            controls=[swatch, selected],
        ),
        ft.Button("Open dialog", on_click=lambda e: page.show_dialog(dialog)),
    )


ft.run(main)
