import flet as ft

name = "Draggable Divider example"


def example():
    def move_divider(e: ft.DragUpdateEvent):
        if (e.delta_y > 0 and c.height < 300) or (e.delta_y < 0 and c.height > 100):
            c.height += e.delta_y
        c.update()

    def show_draggable_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_UP_DOWN
        e.control.update()

    c = ft.Container(
        bgcolor=ft.Colors.AMBER,
        alignment=ft.Alignment.CENTER,
        height=100,
        # expand=1,
    )

    return ft.Column(
        [
            c,
            ft.GestureDetector(
                content=ft.Divider(),
                on_pan_update=move_divider,
                on_hover=show_draggable_cursor,
            ),
            ft.Container(
                bgcolor=ft.Colors.PINK, alignment=ft.Alignment.CENTER, expand=1
            ),
        ],
        spacing=0,
        width=400,
        height=400,
    )
