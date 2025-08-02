import flet as ft

name = "ColorPicker color property"


def example():
    from flet_contrib.color_picker import ColorPicker

    color_picker = ColorPicker(color="#c8df6f")
    new_color = ft.TextField(label="Color in #RRGGBB format")

    def change_color(e):
        color_picker.color = new_color.value
        color_picker.update()

    return ft.Column(
        [
            color_picker,
            new_color,
            ft.FilledButton("Change color", on_click=change_color),
        ]
    )
