import flet as ft


def main(page: ft.Page):
    def on_pan_update(e: ft.DragUpdateEvent[ft.GestureDetector]):
        page.window.left += e.global_delta.x
        page.window.top += e.global_delta.y
        page.update()

    page.add(
        ft.Stack(
            width=1000,
            height=500,
            controls=[
                ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.MOVE,
                    on_pan_update=on_pan_update,
                    left=200,
                    top=200,
                    content=ft.Container(bgcolor=ft.Colors.PINK, width=50, height=50),
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
