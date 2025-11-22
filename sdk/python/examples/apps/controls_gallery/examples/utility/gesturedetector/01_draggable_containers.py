import flet as ft

name = "Draggable containers"


def example():
    def on_pan_update1(e: ft.DragUpdateEvent):
        c.top = max(0, c.top + e.delta_y)
        c.left = max(0, c.left + e.delta_x)
        c.update()

    def on_pan_update2(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    gd = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=50,
        on_pan_update=on_pan_update1,
    )

    c = ft.Container(gd, bgcolor=ft.Colors.AMBER, width=50, height=50, left=0, top=0)

    gd1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_vertical_drag_update=on_pan_update2,
        left=100,
        top=100,
        content=ft.Container(bgcolor=ft.Colors.BLUE, width=50, height=50),
    )

    return ft.Stack([c, gd1], width=1000, height=500)
