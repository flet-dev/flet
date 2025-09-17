from dataclasses import dataclass

import flet as ft


@dataclass
@ft.observable
class CardState:
    top: float = 0
    left: float = 0


@ft.component
def App():
    state, _ = ft.use_state(CardState())

    def on_pan_update(e: ft.DragUpdateEvent):
        # Just update the state – no manual .update() calls!
        state.top = max(0, state.top + e.local_delta.y)
        state.left = max(0, state.left + e.local_delta.x)

    return ft.Stack(
        controls=[
            ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.MOVE,
                drag_interval=5,
                on_pan_update=on_pan_update,
                left=state.left,
                top=state.top,
                content=ft.Container(
                    bgcolor=ft.Colors.GREEN,
                    width=70,
                    height=100,
                ),
            )
        ],
        width=1000,
        height=500,
    )


ft.run(lambda page: page.render(App))
