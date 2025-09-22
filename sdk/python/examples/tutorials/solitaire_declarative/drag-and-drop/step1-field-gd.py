from dataclasses import dataclass, field

import flet as ft


# ---------- Model ----------
@ft.observable
@dataclass
class Card:
    top: float = 0
    left: float = 0


@ft.observable
@dataclass
class Game:
    cards: list[Card] = field(
        default_factory=lambda: [Card(left=0, top=0), Card(left=100, top=0)]
    )


# Card visual constants
CARD_W = 70
CARD_H = 100


# ---------- View (pure) ----------
@ft.component
def CardView(card: Card) -> ft.Control:
    # Pure view: just render from state
    return ft.Container(
        bgcolor=ft.Colors.GREEN,
        left=card.left,
        top=card.top,
        width=CARD_W,
        height=CARD_H,
        border_radius=5,
    )


# ---------- App ----------
@ft.component
def App():
    state, _ = ft.use_state(Game())
    dragging, set_dragging = ft.use_state(False)

    def point_in_card(x: float, y: float) -> bool:
        c = state.cards[0]
        return (c.left <= x <= c.left + CARD_W) and (c.top <= y <= c.top + CARD_H)

    def on_pan_start(e: ft.DragStartEvent):
        # Only start dragging if pointer is inside the card
        # e.local_x / e.local_y are relative to the GestureDetector content (the Stack)
        set_dragging(point_in_card(e.local_position.x, e.local_position.y))

    def on_pan_update(e: ft.DragUpdateEvent):
        if not dragging:
            return
        c = state.cards[0]
        c.left = max(0, c.left + e.local_delta.x)
        c.top = max(0, c.top + e.local_delta.y)

    def on_pan_end(e: ft.DragEndEvent):
        set_dragging(False)

    return ft.GestureDetector(
        on_pan_start=on_pan_start,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        drag_interval=5,
        mouse_cursor=ft.MouseCursor.MOVE,
        content=ft.Stack(
            controls=[
                CardView(state.cards[0]),
                CardView(state.cards[1]),  # depends directly on Card observable
            ],
            width=1000,
            height=500,
        ),
    )


ft.run(lambda page: page.render(App))
