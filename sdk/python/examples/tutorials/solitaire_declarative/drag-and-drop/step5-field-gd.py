# Step 5: Slot has piles of Cards. When a Card is dropped into a Slot, it becomes part
# of that Slot's pile (Slot.cards).

from dataclasses import dataclass, field
from typing import Optional

import flet as ft


# ---------- Model ----------
@ft.observable
@dataclass
class Slot:
    id: str = "slot1"
    top: float = 200
    left: float = 0
    cards: list["Card"] = field(default_factory=list)


@ft.observable
@dataclass
class Card:
    top: float = 0
    left: float = 0
    color: str = ft.Colors.GREEN
    home: Optional[Slot] = None  # <-- reference to a Slot, not a string


@ft.observable
@dataclass
class Game:
    cards: list[Card] = field(
        default_factory=lambda: [
            Card(color=ft.Colors.GREEN),  # positions will be set in __post_init__
            Card(color=ft.Colors.RED),
        ]
    )
    slots: list[Slot] = field(
        default_factory=lambda: [
            Slot(left=0, top=0, id="deck"),
            Slot(left=100, top=0, id="waste"),
            Slot(left=0, top=200, id="slot1"),
            Slot(left=100, top=200, id="slot2"),
        ],
    )
    snap_threshold: float = 20  # px

    def __post_init__(self):
        """Initialize homes & coordinates: card1 -> deck, card2 -> waste."""

        # Set initial homes and positions
        self.cards[0].home = self.slots[0]
        self.cards[0].left, self.cards[0].top = self.slots[0].left, self.slots[0].top
        self.cards[1].home = self.slots[1]
        self.cards[1].left, self.cards[1].top = self.slots[1].left, self.slots[1].top

        # Add cards to slots' card lists
        self.slots[0].cards.append(self.cards[0])
        self.slots[1].cards.append(self.cards[1])


# Card visual constants
CARD_W = 70
CARD_H = 100


# ---------- View (pure) ----------
@ft.component
def CardView(card: Card) -> ft.Control:
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
        content=ft.Text(slot.id, size=10, color=ft.Colors.BLACK45),
    )


# ---------- App ----------
@ft.component
def App():
    state, _ = ft.use_state(Game())
    dragging, set_dragging = ft.use_state(None)  # None or Card

    def point_in_card(x: float, y: float) -> Optional[Card]:
        # Check topmost first so you can grab the card on top
        for c in reversed(state.cards):
            if (c.left <= x <= c.left + CARD_W) and (c.top <= y <= c.top + CARD_H):
                return c
        return None

    def move_to_top(card: Card):
        state.cards.remove(card)
        state.cards.append(card)

    def on_pan_start(e: ft.DragStartEvent):
        grabbed = point_in_card(e.local_position.x, e.local_position.y)
        print("grabbed", grabbed)
        set_dragging(grabbed)
        if grabbed is not None:
            move_to_top(grabbed)

    def on_pan_update(e: ft.DragUpdateEvent):
        if dragging is None:
            return
        c = dragging
        print("moving", c)
        c.left = max(0, c.left + e.local_delta.x)
        c.top = max(0, c.top + e.local_delta.y)

    def on_pan_end(_: ft.DragEndEvent):
        c = dragging
        if c is None:
            return

        # Try to snap to a nearby slot; otherwise bounce back to c.home
        snapped = False
        for s in state.slots:
            near_x = abs(c.left - s.left) < state.snap_threshold
            near_y = abs(c.top - s.top) < state.snap_threshold
            if near_x and near_y:
                c.left, c.top = s.left, s.top
                c.home.cards.remove(c)  # Remove card from previous slot's pile
                c.home = s  # <-- update to the Slot object
                s.cards.append(c)  # Add card to the slot's pile
                snapped = True
                break

        if not snapped and c.home is not None:
            c.left, c.top = c.home.left, c.home.top

        set_dragging(None)
        print("dropped", c)
        print("slot now has cards:", len(c.home.cards) if c.home else None)

    return ft.GestureDetector(
        on_pan_start=on_pan_start,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        drag_interval=5,
        mouse_cursor=ft.MouseCursor.MOVE,
        content=ft.Stack(
            controls=[
                *(SlotView(s) for s in state.slots),
                *(CardView(c) for c in state.cards),
            ],
            width=1000,
            height=500,
        ),
    )


ft.run(lambda page: page.render(App))
