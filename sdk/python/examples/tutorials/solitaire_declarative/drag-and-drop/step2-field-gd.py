from dataclasses import dataclass, field

import flet as ft


# ---------- Model ----------
@ft.observable
@dataclass
class Card:
    top: float = 0
    left: float = 0
    color: str = ft.Colors.GREEN


@dataclass
@ft.observable
class Game:
    cards: list[Card] = field(
        default_factory=lambda: [
            Card(left=0, top=0, color=ft.Colors.GREEN),
            Card(left=100, top=0, color=ft.Colors.RED),
        ],
    )


# ---------- View (pure) ----------
@ft.component
def CardView(card: Card) -> ft.Control:
    # Pure view: no event handlers here, just render the card from state
    return ft.Container(
        bgcolor=card.color,
        left=card.left,
        top=card.top,
        width=70,
        height=100,
        border_radius=5,
    )


# ---------- App ----------
@ft.component
def App():
    state, _ = ft.use_state(Game())

    def on_pan_update(e: ft.DragUpdateEvent):
        # Mutate nested observable; CardView is subscribed to Card, so it re-renders
        state.cards[0].top = max(0, state.cards[0].top + e.local_delta.y)
        state.cards[0].left = max(0, state.cards[0].left + e.local_delta.x)

    return ft.GestureDetector(
        on_pan_update=on_pan_update,
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
