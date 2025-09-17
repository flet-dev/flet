from dataclasses import dataclass, field

import flet as ft


@dataclass
@ft.observable
class CardState:
    left: float
    top: float
    color: str
    drag_start_left: float = 0
    drag_start_top: float = 0


@dataclass
@ft.observable
class GameState:
    slot_left: float = 200
    slot_top: float = 0
    snap_threshold: float = 20
    cards: list[CardState] = field(
        default_factory=lambda: [
            CardState(left=0, top=0, color=ft.Colors.GREEN),
            CardState(left=100, top=0, color=ft.Colors.YELLOW),
        ]
    )

    def bring_to_top(self, card: CardState):
        self.cards.remove(card)
        self.cards.append(card)


@ft.component
def CardView(card: CardState, state: GameState) -> ft.Control:
    def on_pan_start(e: ft.DragStartEvent):
        # state.bring_to_top(card)
        card.drag_start_left = card.left
        card.drag_start_top = card.top

    def on_pan_update(e: ft.DragUpdateEvent):
        card.left = max(0, card.left + e.local_delta.x)
        card.top = max(0, card.top + e.local_delta.y)

    def on_pan_end(e: ft.DragEndEvent):
        near_x = abs(card.left - state.slot_left) < state.snap_threshold
        near_y = abs(card.top - state.slot_top) < state.snap_threshold
        if near_x and near_y:
            card.left = state.slot_left
            card.top = state.slot_top
        else:
            card.left = card.drag_start_left
            card.top = card.drag_start_top

    return ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=on_pan_start,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        left=card.left,
        top=card.top,
        content=ft.Container(
            bgcolor=card.color,
            width=70,
            height=100,
            border_radius=5,
        ),
    )


@ft.component
def App():
    state, _ = ft.use_state(GameState())

    return ft.Stack(
        width=1000,
        height=500,
        controls=[
            # Slot
            ft.Container(
                left=state.slot_left,
                top=state.slot_top,
                width=70,
                height=100,
                border=ft.Border.all(1, ft.Colors.BLACK45),
                border_radius=5,
            ),
            # Cards (order in list = z-order)
            *[CardView(c, state) for c in state.cards],
        ],
    )


ft.run(lambda page: page.render(App))
