# Always derive card position from its home slot.
# Drag uses ephemeral offsets; on drop, change `home` or snap back by clearing offsets.

from dataclasses import dataclass, field
from typing import Optional

import flet as ft


# ---------- Model ----------
@ft.observable
@dataclass
class Card:
    id: str
    color: str = ft.Colors.GREEN
    home: str = "deck"  # "deck" or Slot.id


@ft.observable
@dataclass
class Slot:
    id: str
    left: float
    top: float


@ft.observable
@dataclass
class Game:
    cards: list[Card] = field(
        default_factory=lambda: [
            Card(id="c0", color=ft.Colors.GREEN, home="deck"),
            Card(id="c1", color=ft.Colors.RED, home="waste"),
        ]
    )
    slots: list[Slot] = field(
        default_factory=lambda: [
            Slot(id="deck", left=0, top=0),
            Slot(id="waste", left=100, top=0),
            Slot(id="slot1", left=0, top=200),
            Slot(id="slot2", left=100, top=200),
        ],
    )
    snap_threshold: float = 20  # px


# Card visual constants
CARD_W, CARD_H = 70, 100


# ---------- Helpers ----------
def slot_coords(state: Game, slot_id: str) -> tuple[float, float]:
    for s in state.slots:
        if s.id == slot_id:
            return s.left, s.top
    return (0.0, 0.0)


def hit_test_slot(x: float, y: float, state: Game) -> Optional[str]:
    for s in state.slots:
        if s.left <= x <= s.left + CARD_W and s.top <= y <= s.top + CARD_H:
            return s.id
    return None


def nearest_slot(x: float, y: float, state: Game) -> Optional[str]:
    best, best_d2 = None, 1e18
    for s in state.slots:
        dx, dy = x - s.left, y - s.top
        d2 = dx * dx + dy * dy
        if d2 < best_d2:
            best, best_d2 = s.id, d2
    return best if (best_d2**0.5) <= state.snap_threshold else None


# ---------- Views ----------
@ft.component
def CardView(card: Card, dragging_id, drag_dx, drag_dy) -> ft.Control:
    # Base position is ALWAYS derived from card.home
    base_x, base_y = slot_coords(App._game, card.home)  # App._game is set in App()

    # If this is the active drag, apply transient offsets; otherwise render at base
    x = base_x + (drag_dx if dragging_id == card.id else 0)
    y = base_y + (drag_dy if dragging_id == card.id else 0)

    return ft.Container(
        key=card.id,  # stable identity
        left=x,
        top=y,
        width=CARD_W,
        height=CARD_H,
        bgcolor=card.color,
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
        content=ft.Text(slot.id, size=10, color=ft.Colors.PRIMARY),
    )


# ---------- App ----------
@ft.component
def App():
    state, _ = ft.use_state(Game())
    # expose state to CardView for slot lookup (simple way to avoid prop-drilling)
    App._game = state  # type: ignore[attr-defined]

    # Drag gesture state (ephemeral)
    dragging_id, set_dragging_id = ft.use_state(None)  # card.id or None
    drag_dx, set_drag_dx = ft.use_state(0.0)  # transient x offset
    drag_dy, set_drag_dy = ft.use_state(0.0)  # transient y offset

    def card_at(x: float, y: float) -> Optional[Card]:
        # Hit test uses derived positions from home
        for c in state.cards:
            bx, by = slot_coords(state, c.home)
            if bx <= x <= bx + CARD_W and by <= y <= by + CARD_H:
                return c
        return None

    def on_pan_start(e: ft.DragStartEvent):
        grabbed = card_at(e.local_position.x, e.local_position.y)
        if grabbed:
            set_dragging_id(grabbed.id)
            set_drag_dx(0.0)
            set_drag_dy(0.0)

    def on_pan_update(e: ft.DragUpdateEvent):
        if not dragging_id:
            return
        set_drag_dx(drag_dx + e.local_delta.x)
        set_drag_dy(drag_dy + e.local_delta.y)

    def on_pan_end(e: ft.DragEndEvent):
        if not dragging_id:
            return
        # Compute drop point relative to the card's base (home) position
        card = next(c for c in state.cards if c.id == dragging_id)
        base_x, base_y = slot_coords(state, card.home)
        drop_x, drop_y = base_x + drag_dx, base_y + drag_dy

        # Prefer direct hit; otherwise nearest within threshold
        sid = hit_test_slot(drop_x, drop_y, state) or nearest_slot(
            drop_x, drop_y, state
        )
        if sid:
            card.home = sid  # commit logical placement
        # else: keep existing home → bounce back automatically

        # Clear transient drag offsets
        set_drag_dx(0.0)
        set_drag_dy(0.0)
        set_dragging_id(None)

    # Draw dragged card last (on top) without reordering the model
    cards = list(state.cards)
    if dragging_id:
        cards.sort(key=lambda c: c.id != dragging_id)

    return ft.GestureDetector(
        on_pan_start=on_pan_start,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        drag_interval=5,
        mouse_cursor=ft.MouseCursor.MOVE,
        content=ft.Stack(
            width=1000,
            height=500,
            controls=[
                *map(SlotView, state.slots),
                *[CardView(c, dragging_id, drag_dx, drag_dy) for c in cards],
            ],
        ),
    )


ft.run(lambda page: page.render(App))
