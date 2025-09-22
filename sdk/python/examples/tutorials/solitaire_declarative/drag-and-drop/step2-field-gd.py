# Step 2: Place the card into a slot if close enough when dropped, otherwise bounce
# back.

from dataclasses import dataclass, field

import flet as ft


# ---------- Model ----------
@ft.observable
@dataclass
class Card:
    top: float = 0
    left: float = 0
    color: str = ft.Colors.GREEN


@ft.observable
@dataclass
class Slot:
    top: float = 200
    left: float = 0


@ft.observable
@dataclass
class Game:
    cards: list[Card] = field(
        default_factory=lambda: [
            Card(left=0, top=0, color=ft.Colors.GREEN),
            Card(left=100, top=0, color=ft.Colors.RED),
        ]
    )
    slots: list[Slot] = field(
        default_factory=lambda: [
            Slot(left=0, top=200),
            Slot(left=100, top=200),
        ],
    )


# Card visual constants
CARD_W = 70
CARD_H = 100


# ---------- View (pure) ----------
@ft.component
def CardView(card: Card) -> ft.Control:
    # Pure view: just render from state
    return ft.Container(
        bgcolor=card.color,
        left=card.left,
        top=card.top,
        width=CARD_W,
        height=CARD_H,
        border_radius=5,
    )


@ft.component
def SlotView(slot: Slot) -> ft.Control:
    return ft.Container(
        left=slot.left,
        top=slot.top,
        width=CARD_W,
        height=CARD_H,
        border=ft.Border.all(1, ft.Colors.PRIMARY),
        border_radius=5,
    )


# ---------- App ----------
@ft.component
def App():
    state, _ = ft.use_state(Game())
    dragging, set_dragging = ft.use_state(None)  # None or Card being dragged

    def point_in_card(x: float, y: float) -> Card | None:
        for c in state.cards:
            if (c.left <= x <= c.left + CARD_W) and (c.top <= y <= c.top + CARD_H):
                return c
        return None

    def move_to_top(card: Card):
        state.cards.remove(card)
        state.cards.append(card)

    def on_pan_start(e: ft.DragStartEvent):
        # Only start dragging if pointer is inside the card
        # e.local_position.x / e.local_position.y are relative to the GestureDetector
        # content (the Stack)
        grabbed = point_in_card(e.local_position.x, e.local_position.y)
        set_dragging(grabbed)
        if grabbed is not None:
            move_to_top(grabbed)

    def on_pan_update(e: ft.DragUpdateEvent):
        if dragging is None:
            return
        c = dragging
        c.left = max(0, c.left + e.local_delta.x)
        c.top = max(0, c.top + e.local_delta.y)

    def on_pan_end(e: ft.DragEndEvent):
        set_dragging(None)

    return ft.GestureDetector(
        on_pan_start=on_pan_start,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        drag_interval=5,
        mouse_cursor=ft.MouseCursor.MOVE,
        content=ft.Stack(
            controls=[SlotView(s) for s in state.slots]
            + [CardView(c) for c in state.cards],
            width=1000,
            height=500,
        ),
    )


ft.run(lambda page: page.render(App))
