import random

import flet as ft


def main(page: ft.Page):
    def on_pan_update(event: ft.DragUpdateEvent[ft.GestureDetector]):
        container.top = max(0.0, container.top + event.delta_y)
        container.left = max(0.0, container.left + event.delta_x)
        container.update()

    gesture_detector = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.BASIC,
        drag_interval=50,
        on_pan_update=on_pan_update,
    )
    container = ft.Container(
        content=gesture_detector,
        bgcolor=ft.Colors.AMBER,
        width=150,
        height=150,
        left=0,
        top=0,
    )

    def handle_button_click(e: ft.Event[ft.Button]):
        gesture_detector.mouse_cursor = random.choice(list(ft.MouseCursor))
        text.value = f"Mouse Cursor:  {gesture_detector.mouse_cursor}"
        page.update()

    page.add(
        ft.Stack(controls=[container], width=1000, height=500),
        ft.Button("Change mouse Cursor", on_click=handle_button_click),
        text := ft.Text(f"Mouse Cursor:  {gesture_detector.mouse_cursor}"),
    )


if __name__ == "__main__":
    ft.run(main)
