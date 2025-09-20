from dataclasses import dataclass

import flet as ft


@dataclass
@ft.observable
class Card:
    top: float = 0
    left: float = 0


@ft.component
def App():
    state, _ = ft.use_state(Card())

    def on_pan_update(e: ft.DragUpdateEvent):
        # Just update the state – no manual .update() calls!
        state.top = max(0, state.top + e.local_delta.y)
        state.left = max(0, state.left + e.local_delta.x)

    return ft.GestureDetector(
        on_pan_update=on_pan_update,
        drag_interval=5,
        mouse_cursor=ft.MouseCursor.MOVE,
        content=ft.Stack(
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.GREEN,
                    left=state.left,
                    top=state.top,
                    width=70,
                    height=100,
                ),
            ],
            width=1000,
            height=500,
        ),
    )


ft.run(lambda page: page.render(App))
