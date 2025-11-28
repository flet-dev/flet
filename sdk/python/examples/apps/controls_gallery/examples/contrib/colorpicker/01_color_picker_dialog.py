import flet as ft

name = "ColorPicker dialog"


def example():
    from flet_contrib.color_picker import ColorPicker

    async def open_color_picker(e):
        e.control.page.dialog = d
        d.open = True
        e.control.page.update()

    color_picker = ColorPicker(color="#c8df6f", width=300)
    color_icon = ft.IconButton(icon=ft.Icons.BRUSH, on_click=open_color_picker)

    def change_color(e):
        color_icon.icon_color = color_picker.color
        d.open = False
        e.control.page.update()

    def close_dialog(e):
        d.open = False
        d.update()

    d = ft.AlertDialog(
        content=color_picker,
        actions=[
            ft.TextButton("OK", on_click=change_color),
            ft.TextButton("Cancel", on_click=close_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=change_color,
    )

    return color_icon
