import flet as ft

name = "ColorPicker dialog"


def example():
    from flet_contrib.color_picker import ColorPicker

    async def open_color_picker(e):
        e.control.page.dialog = d
        d.open = True
        await e.control.page.update_async()

    color_picker = ColorPicker(color="#c8df6f", width=300)
    color_icon = ft.IconButton(icon=ft.Icons.BRUSH, on_click=open_color_picker)

    async def change_color(e):
        color_icon.icon_color = color_picker.color
        d.open = False
        await e.control.page.update_async()

    async def close_dialog(e):
        d.open = False
        await d.update_async()

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
