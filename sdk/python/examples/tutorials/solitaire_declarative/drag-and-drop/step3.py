from dataclasses import dataclass, field

import flet as ft


@dataclass
@ft.observable
class Card:
    id: str
    left: float
    top: float
    color: str
    home: str = "deck"  # "deck" or "slot"


@dataclass
@ft.observable
class GameState:
    slot_left: float = 200
    slot_top: float = 0
    snap_threshold: float = 20
    cards: list[Card] = field(
        default_factory=lambda: [
            Card(id="card1", left=0, top=0, color=ft.Colors.GREEN),
            Card(id="card2", left=100, top=0, color=ft.Colors.YELLOW),
        ]
    )

    def bring_to_top(self, card: Card):
        self.cards.remove(card)
        self.cards.append(card)


@ft.component
def CardView(card: Card, state: GameState, key=None) -> ft.Control:
    drag_start_pos, set_drag_start_pos = ft.use_state((card.left, card.top))

    def on_pan_start(e: ft.DragStartEvent):
        state.bring_to_top(card)
        print("drag start", card.id, card.left, card.top, card.color)
        set_drag_start_pos((card.left, card.top))

    def on_pan_update(e: ft.DragUpdateEvent):
        print("drag update", card.id, card.left, card.top, card.color)
        card.left = max(0, card.left + e.local_delta.x)
        card.top = max(0, card.top + e.local_delta.y)

    def on_pan_end(e: ft.DragEndEvent):
        print("drag end", card.id, card.left, card.top, card.color)
        near_x = abs(card.left - state.slot_left) < state.snap_threshold
        near_y = abs(card.top - state.slot_top) < state.snap_threshold
        if near_x and near_y:
            card.left = state.slot_left
            card.top = state.slot_top
        else:
            card.left = drag_start_pos[0]
            card.top = drag_start_pos[1]

    return ft.GestureDetector(
        key=card.id,
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
            *[CardView(c, state, key=c.id) for c in state.cards],
        ],
    )


ft.run(lambda page: page.render(App))
