import flet as ft

name = "Draggable VerticalDivider"


def example():
    def move_vertical_divider(e: ft.DragUpdateEvent):
        if (e.delta_x > 0 and c.width < 300) or (e.delta_x < 0 and c.width > 100):
            c.width += e.delta_x
        c.update()

    def show_draggable_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    c = ft.Container(
        bgcolor=ft.Colors.ORANGE_300,
        alignment=ft.Alignment.CENTER,
        width=100,
        # expand=1,
    )

    return ft.Row(
        controls=[
            c,
            ft.GestureDetector(
                content=ft.VerticalDivider(),
                drag_interval=10,
                on_pan_update=move_vertical_divider,
                on_hover=show_draggable_cursor,
            ),
            ft.Container(
                bgcolor=ft.Colors.BROWN_400,
                alignment=ft.Alignment.CENTER,
                expand=1,
            ),
        ],
        spacing=0,
        width=400,
        height=400,
    )
