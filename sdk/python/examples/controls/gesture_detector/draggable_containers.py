import flet as ft


def main(page: ft.Page):
    def handle_pan_update1(e: ft.DragUpdateEvent[ft.GestureDetector]):
        container = e.control.parent
        container.top = max(0.0, container.top + e.delta_y)
        container.left = max(0.0, container.left + e.delta_x)
        container.update()

    def handle_pan_update2(e: ft.DragUpdateEvent[ft.GestureDetector]):
        e.control.top = max(0.0, e.control.top + e.delta_y)
        e.control.left = max(0.0, e.control.left + e.delta_x)
        e.control.update()

    page.add(
        ft.Stack(
            width=1000,
            height=500,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.AMBER,
                    width=50,
                    height=50,
                    left=0,
                    top=0,
                    content=ft.GestureDetector(
                        mouse_cursor=ft.MouseCursor.MOVE,
                        drag_interval=50,
                        on_pan_update=handle_pan_update1,
                    ),
                ),
                ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.MOVE,
                    drag_interval=10,
                    on_vertical_drag_update=handle_pan_update2,
                    left=100,
                    top=100,
                    content=ft.Container(bgcolor=ft.Colors.BLUE, width=50, height=50),
                ),
            ],
        )
    )


ft.run(main)
