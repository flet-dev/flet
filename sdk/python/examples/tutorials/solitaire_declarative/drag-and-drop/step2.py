from dataclasses import dataclass

import flet as ft


@dataclass
@ft.observable
class GameState:
    # card position
    card_left: float = 0
    card_top: float = 0

    # slot position
    slot_left: float = 200
    slot_top: float = 0

    # remember where the drag started (to bounce back)
    drag_start_left: float = 0
    drag_start_top: float = 0

    # snap threshold in px
    snap_threshold: float = 20


@ft.component
def App():
    s, _ = ft.use_state(GameState())

    def on_pan_start(e: ft.DragStartEvent):
        # capture where the card was when the drag started
        s.drag_start_left = s.card_left
        s.drag_start_top = s.card_top

    def on_pan_update(e: ft.DragUpdateEvent):
        # move by delta (no control mutation)
        s.card_left = max(0, s.card_left + e.local_delta.x)
        s.card_top = max(0, s.card_top + e.local_delta.y)

    def on_pan_end(e: ft.DragEndEvent):
        # snap to slot if close enough, otherwise bounce back
        near_x = abs(s.card_left - s.slot_left) < s.snap_threshold
        near_y = abs(s.card_top - s.slot_top) < s.snap_threshold
        if near_x and near_y:
            s.card_left = s.slot_left
            s.card_top = s.slot_top
        else:
            s.card_left = s.drag_start_left
            s.card_top = s.drag_start_top

    return ft.Stack(
        width=1000,
        height=500,
        controls=[
            # drop slot (purely a function of state)
            ft.Container(
                left=s.slot_left,
                top=s.slot_top,
                width=70,
                height=100,
                border=ft.Border.all(1, ft.Colors.BLACK45),
                border_radius=5,
            ),
            # draggable card
            ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.MOVE,
                drag_interval=5,
                on_pan_start=on_pan_start,
                on_pan_update=on_pan_update,
                on_pan_end=on_pan_end,
                left=s.card_left,
                top=s.card_top,
                content=ft.Container(
                    width=70,
                    height=100,
                    bgcolor=ft.Colors.GREEN,
                    border_radius=5,
                ),
            ),
        ],
    )


ft.run(lambda page: page.render(App))
