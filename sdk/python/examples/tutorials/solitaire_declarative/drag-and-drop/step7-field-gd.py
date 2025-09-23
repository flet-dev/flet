# Step 7: Refactor calculations to be more readable and maintainable.

from dataclasses import dataclass, field
from typing import Optional

import flet as ft


# ---------- Model ----------
@ft.observable
@dataclass
class Slot:
    id: str
    top: float
    left: float
    cards: list["Card"] = field(default_factory=list)
    stacking: bool = False  # whether cards in this slot stack with offset


@ft.observable
@dataclass
class Card:
    color: str
    top: float = 0
    left: float = 0
    home: Optional[Slot] = None  # <-- reference to a Slot, not a string


@ft.observable
@dataclass
class Game:
    cards: list[Card] = field(
        default_factory=lambda: [
            Card(color=ft.Colors.GREEN),  # positions will be set in __post_init__
            Card(color=ft.Colors.RED),
            Card(color=ft.Colors.BLUE),
            Card(color=ft.Colors.YELLOW),
        ]
    )
    slots: list[Slot] = field(
        default_factory=lambda: [
            Slot(left=0, top=0, id="deck"),
            Slot(left=100, top=0, id="waste"),
            Slot(left=200, top=0, id="foundation1"),
            Slot(left=300, top=0, id="foundation2"),
            Slot(left=0, top=200, id="slot1", stacking=True),
            Slot(left=100, top=200, id="slot2", stacking=True),
            Slot(left=200, top=200, id="slot3", stacking=True),
        ],
    )
    # snap_threshold: float = 20  # px

    def __post_init__(self):
        """Initialize homes & coordinates: card1 -> deck, card2 -> waste."""

        # Set initial homes and positions
        # self.cards[0].home = self.slots[0]
        # self.cards[0].left, self.cards[0].top = self.slots[0].left, self.slots[0].top
        # self.cards[1].home = self.slots[1]
        # self.cards[1].left, self.cards[1].top = self.slots[1].left, self.slots[1].top
        for card in self.cards:
            card.home = self.slots[0]
            card.left, card.top = self.slots[0].left, self.slots[0].top

        # Add cards to slots' card lists
        self.slots[0].cards = self.cards.copy()
        print("deck has cards:", len(self.slots[0].cards))


# Card visual constants
CARD_W = 70
CARD_H = 100
SNAP_THRESHOLD = 20  # px
OFFSET_Y = 20  # px


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
    state, _ = ft.use_state(lambda: Game())
    dragging, set_dragging = ft.use_state(None)  # None or Card being dragged
    start_x, set_start_x = ft.use_state(0)  # initial x of the card being dragged
    start_y, set_start_y = ft.use_state(0)  # initial y of the card being dragged

    print("Current cards in deck:", len(state.slots[0].cards))

    def point_in_card(x: float, y: float) -> Optional[Card]:
        # Check topmost first so you can grab the card on top
        for c in reversed(state.cards):
            if (
                (c.left <= x <= c.left + CARD_W)
                and (c.top <= y <= c.top + CARD_H)
                and (
                    c.home.cards.index(c) == len(c.home.cards) - 1
                )  # is topmost in its slot
            ):
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
            set_start_x(grabbed.left)
            set_start_y(grabbed.top)

    def on_pan_update(e: ft.DragUpdateEvent):
        if dragging is None:
            return
        dragging.left = max(0, dragging.left + e.local_delta.x)
        dragging.top = max(0, dragging.top + e.local_delta.y)

    def on_pan_end(_: ft.DragEndEvent):
        if dragging is None:
            return

        # Try to snap to a nearby slot; otherwise bounce back to dragging.home
        # with offset if stacking
        snapped = False
        for s in state.slots:
            if s != dragging.home:
                offset = (
                    (len(s.cards) - 1) * OFFSET_Y
                    if s.stacking and len(s.cards) > 0
                    else 0
                )
                near_x = abs(dragging.left - s.left) < SNAP_THRESHOLD
                near_y = abs(dragging.top - (s.top + offset)) < SNAP_THRESHOLD
                if near_x and near_y:
                    dragging.left, dragging.top = (
                        s.left,
                        s.top + OFFSET_Y * len(s.cards) if s.stacking else s.top,
                    )
                    dragging.home.cards.remove(
                        dragging
                    )  # Remove card from previous slot's pile
                    dragging.home = s  # <-- update to the Slot object
                    s.cards.append(dragging)  # Add card to the slot's pile
                    snapped = True
                    break

        if not snapped:
            dragging.left, dragging.top = start_x, start_y

        set_dragging(None)
        print("dropped", dragging)
        print(
            "slot now has cards:", len(dragging.home.cards) if dragging.home else None
        )

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
